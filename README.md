# Multivariate Polynomial Interpreter

This code provides an environment to manipulate and differentiate multivariate polynomials.


## Supported Operations

As of 6/28/2024, supported operations are:
* '+' : addition
* '-' : subtraction
* '*' : multiplication
* '/' : division
* '&' : differentiation

<!-- USAGE EXAMPLES -->
## Usage
* Commands are typed in the terminal beside the 'calc>' prompt and will execute when you press 'enter.'
The output prints to a new line.
```
calc> (1+x)*(1-x)
1 - x^2
```
* If the output is a fraction, the terminal will print the numerator, a new line of dashes, then a new line with the denominator.
```
calc> x/y
x
-
y
```
* A functional derivitive is performed on the polynomial immediately to the right of an '&' operator.
  In the output, '(&x)' represents the variation of function x.
```
calc> &(x/y)
(&x)y - (&y)x
-------------
     y^2
```

## A Word
The ultimate goal of this project is to construct a symbolic riemannian geometry engine capable of computing the fundamental tensors and Christoffel symbols associated with a given metric. If you
have anything you would like to contribute, feel free to message me on instagram (@wheesman), linkdin (www.linkedin.com/in/luis-cuevas-73634a1b1), or on here (if github has a message feature.)


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Big shoutout to Ruslan Spivak for the tutorial on building interpreters. A lot of this code comes from their blog post, https://ruslanspivak.com/lsbasi-part1/.
