# Multivariate Polynomial Interpreter

This code provides an environment to manipulate and differentiate multivariate polynomials.


## Supported Operations

As of 6/26/2024, supported operations are:
* '+' : addition
* '-' : subtraction
* '*' : multiplication
* '&' : differentiation

<!-- USAGE EXAMPLES -->
## Usage
* Commands are typed in the terminal beside the 'calc>' prompt and are executed upon the press of 'enter.'
```
calc> (x+1)*(x+1)

```
* The interpreter will output an expanded form of any polynomial manipulations performed in the terminal.
```
calc> (x+1)*(x+1)
xx + 2x + 1
```
* A functional derivitive is performed on the polynomial immediatley to the right of an '&' operator.
  In the output, '(&x)' represents the variation of function x.
```
calc> &((x+1)*(x+1))
2x(&x) + 2(&x)
```


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Big shoutout to Ruslan Spivak for the tutorial on building interpreters. A lot of this code comes from their blog post, https://ruslanspivak.com/lsbasi-part1/.
