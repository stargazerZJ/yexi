# yexi: Helper for Physics Experiments

## Introduction
`yexi` is a helper for physics experiments. Currently, it is only capable of calculating the result of a measurement with its uncertainty. It is designed to be easy to use and to be able to handle complex calculations.

**Important Note**: This module requires `pytorch` to be installed, which is a huge library. Be sure to have enough space and time to install it.

## Installation
- Clone the repository and copy the `yexi` folder to your project.

## Usage
```python
>>> import yexi
>>> x = yexi.measure(10, 0.1)		# a measured value 10 with tolerance 0.1
>>> x
10.0 ± 0.095
>>> def f(x, y):
...     return x**2 + y
...
>>> y = 5
>>> yexi.calc(f, x, y)				# calculate the result of f(x, y), with uncertainty
105.0 ± 1.899999976158142
>>> yexi.measure([1,0.9,1.1],0.05)	# multiple measurements
1.0 ± 0.25291431694161404
```
Note that the default confidence level is 0.95. You can change the confidence level by setting `yexi.uncertainty.confidence` to a value between 0 and 1, which takes effect on all subsequent measurements.