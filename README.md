# yexi: Helper for Physics Experiments

## Introduction
`yexi` is a helper for physics experiments. Currently, it is only capable of calculating the result of a measurement with its uncertainty. It is designed to be easy to use and to be able to handle complex calculations.

**Important Note**: This module requires `pytorch` to be installed, which is a huge library. Be sure to have enough space and time to install it.

## Installation
- Clone the repository.
- Install the required packages by running `pip install -r requirements.txt`.
- Copy the `yexi` folder to your project.

## Basic Usage
```python
>>> import yexi
>>> x = yexi.measure(10, 0.1)      # a measured value 10 with tolerance 0.1
Measured Value 10.0 ± 0.095
>>> x.uncertainty                  # get the uncertainty
0.095
>>> y = yexi.measure([5,4.9,5.1], 0.1) # multiple measurements
>>> z = x ** 2 + y - 1
>>> z                              # calculating with measured values
Tensor(104.0)                      # the value is available immediately
>>> yexi.uncertainty(z, [x, y])    # to get the uncertainty, use the uncertainty function with all the measured values
Result: 104.0 ± 1.9185240268707275
Tensor(104.0)
>>> z.uncertainty # Note that the `uncertainty` attribute is available only after calling the `uncertainty` function
1.9185240268707275
```
Note that the default confidence level is 0.95. You can change the confidence level by setting `yexi.uncertainty.confidence` to a value between 0 and 1, which takes effect on all subsequent measurements.
## Advanced Usage
**Factor and Intercept:**
```python
>>> x = yexi.measure(10, 0.1, factor=10, intercept=0.2)
Measured Value 98.0 ± 0.95
>>> y = yexi.measure([5,4.9,5.1], 0.1, factor=10, intercept=0.2)
Measured Value 48.0 ± 2.6595939861949365
```
The value of `x` is calculated as `(10 - 0.2) * 10 = 98`.
**relative uncertainty:**
```python
x = yexi.measure(10, 0.1)
yexi.relative_uncertainty(x) # 0.0095
y = x + 1
yexi.uncertainty(y, [x])
r = yexi.relative_uncertainty(y) # must be called after the `uncertainty` function
print(r) # 0.008636363527991554
```
**Uncertainty contrubution:**
```python
x = measure(10, 0.1)
y = measure(10, 0.1)
z = x ** 2 + y
z = uncertainty(z, [x, y])
print(z.contributions) # tensor([1.9000, 0.0950])
```
The contributions are defined as $\left| \frac{\partial z}{\partial x} u_x \right|$ and $\left| \frac{\partial z}{\partial y} u_y \right|$. They are available only after calling the `uncertainty` function.
**Non-algebraic operations via PyTorch:**
```python
import torch
x = measure(1, 0.1)
r = torch.sin(x)
r = uncertainty(r, [x]) # Result: 0.8414709568023682 ± 0.05132872238755226
```