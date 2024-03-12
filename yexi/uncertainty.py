import numpy as np
import scipy.stats
import torch

confidence = 0.95

def measure(value, tolerance=0, factor=1, intercept=0):
	"""Measure a value with uncertainty, returning a torch.Tensor with an extra uncertainty attribute."""
	systematic_error = tolerance * confidence	# assuming the data is uniformly distributed within the tolerance

	if isinstance(value, (list, np.ndarray)):
		ME = margin_of_error(np.array(value))
		mean_value = (np.mean(value) - intercept) * factor
		uncertainty = np.sqrt(ME**2 + systematic_error**2) * factor
	else:
		mean_value = (value - intercept) * factor
		uncertainty = systematic_error * factor

	# Create a Tensor object and attach the uncertainty as an attribute
	result_tensor = torch.tensor(mean_value, dtype=torch.float, requires_grad=True)
	setattr(result_tensor, 'uncertainty', uncertainty)

	print(f'Measured Value {mean_value} ± {uncertainty}')
	return result_tensor

def margin_of_error(value):
	"""Calculate Margin of Error (the uncertainty associated with random error), using the t-distribution."""
	return scipy.stats.t.ppf((1 + confidence) / 2, len(value) - 1) * np.std(value, ddof=1) / np.sqrt(len(value))

def uncertainty(result, inputs):
	"""Calculate the uncertainty of a result based on the uncertainties of its inputs."""
	if not all(hasattr(input, 'uncertainty') for input in inputs if isinstance(input, torch.Tensor)):
		raise ValueError("All inputs must have an 'uncertainty' attribute.")

	derivatives = []
	for input in inputs:
		if isinstance(input, torch.Tensor) and hasattr(input, 'uncertainty'):
			input.requires_grad_(True)
			derivative = torch.autograd.grad(outputs=result, inputs=input, retain_graph=True)[0]
			derivatives.append(input.uncertainty * derivative)

	derivatives = torch.tensor(derivatives)
	total_uncertainty = torch.sqrt(torch.sum(derivatives ** 2))
	setattr(result, 'uncertainty', total_uncertainty.item())
	setattr(result, 'contributions', derivatives)

	print(f'Result: {result.item()} ± {total_uncertainty.item()}')
	return result

def relative_uncertainty(value : torch.Tensor):
	"""Calculate the relative uncertainty of a value."""
	if not hasattr(value, 'uncertainty'):
		raise ValueError("The input must have an 'uncertainty' attribute. Call the `uncertainty` function first.")
	return value.uncertainty / value.item()

if __name__ == "__main__":

	def repr(value : torch.Tensor):
		'''Return a string representation of a measured value'''
		if not hasattr(value, 'uncertainty'):
			return str(value.item())
		return f"{value.item()} ± {value.uncertainty}"

	# Test the measure function
	print("Testing the measure function")
	x = measure(10, 0.1)
	y = measure([5,4.9,5.1], 0.1)
	z = 1
	print(x)
	print(x.uncertainty)
	print(repr(x))

	# Test the uncertainty function
	print("Testing the uncertainty function")
	r = x ** 2 + y - z
	r = uncertainty(r, [x, y])
	print(repr(r))

	# Test factor and intercept
	print("Testing the factor and intercept")
	x = measure(10, 0.1, factor=0.1, intercept=0.2)
	y = measure([5,4.9,5.1], 0.1, factor=10, intercept=0.2)

	# Test uncertainty contributions
	print("Testing uncertainty contributions")
	x = measure(10, 0.1)
	y = measure(10, 0.1)
	r = x ** 2 + y
	r = uncertainty(r, [x, y])
	print(r.contributions)