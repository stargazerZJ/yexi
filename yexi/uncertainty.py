import numpy as np
import scipy.stats
import torch
confidence = 0.95
class Value:
	'''A measured or calculated value, with uncertainty.'''
	def __init__(self, value, uncertainty=0):
		self.value = float(value)
		self.uncertainty = float(uncertainty)

	def __repr__(self) -> str:
		return f'{self.value} ± {self.uncertainty}'

def margin_of_error(value : np.array) -> float:
	'''calculate Margin of Error (the uncertainty associated with random error), using the t-distribution'''
	return scipy.stats.t.ppf((1 + confidence) / 2, len(value) - 1) * np.std(value, ddof=1) / np.sqrt(len(value))

def measure(value : np.array, tolerance=0) -> Value:
	'''measure a value with uncertainty, assuming the data is uniformly distributed within the tolerance'''
	systematic_error = tolerance * confidence
	if hasattr(value, '__len__'):
		ME = margin_of_error(value)
		return Value(np.mean(value), np.sqrt(ME**2 + systematic_error**2))
	else:
		return Value(value, systematic_error)

def calc(f, *args : float | Value) -> Value:
    '''calculate a function with uncertainty, using torch'''
    # Convert all arguments to torch tensors
    values = [torch.tensor(arg.value if isinstance(arg, Value) else float(arg), requires_grad=True) for arg in args]
    uncertainties = [torch.tensor(arg.uncertainty if isinstance(arg, Value) else 0) for arg in args]

    # Calculate the function value
    value : torch.Tensor = f(*values)

    # Calculate the uncertainty using the formula for error propagation
    value.backward()
    uncertainty = torch.sqrt(sum((uncertainty * value.grad)**2 for uncertainty, value in zip(uncertainties, values)))

    return Value(value.detach().numpy(), uncertainty.detach().numpy())