# Command Line Calculus Environment

This code provides an environment to manipulate and differentiate multivariate functions.

## Supported Operations 
|Symbol  |Function                      |
|:-----  |:-------------------------    |
| +      | addition                     |
| -      | subtraction                  |
| *      | multiplication               |
| /      | division                     |
| &      | functional differentiation   |
| $      | partial differentiation      |
| log    | natural logarithm            |
| =      | assignment                   |
| show   | output to console            |

<!-- USAGE EXAMPLES -->
## Usage
* Variables are assigned via the '=' operator. The function immediately to the right of an '=' operator
  will be assigned to the variable immedately to the left of the operator. A variable's assignment is simplified upon          construction.
```
> y=x*x
```
* A variable's assignment can be shown in the console via the 'show' operator. The assignment will be printed
  to the following line.
```
> y=x*x
> show(y)
(x)^(2)
```
*  Unassigned variables will be treated as general functions. Assigned variables will be automatically substituted in           later operations.
```
> y=x*x
> z=y*y
> show(z)
(x)^(4)
```
* Multiple statements on the same line are separeted by a semi-colon. Multi-statement line will be executed from left to       right.
```
> y=x*x; z=y*y
> show(z)
(x)^(4)
```
* Unassigned variables will be treated as general functions. A functional derivitive is performed on the expression            immediately to the right of an '&' operator. In the output, '&[]' represents the variation of function '[]'.
```
> y=&(x*x)
> show(y)
> (x)*(&x)*(2)
```
* A partial derivitive is performed on the expression (in parentheses) immediately to the right of a '$_[]' operator with respect to variable/function '[]'.
```
> y=$_x(x*x)
> show(y)
(x)*(2)
```
* A logarithm of natural base is perormed on the expression (in parentheses) immediately to the right of the 'log' operator.
```
> y=$_x(log(x))
> show(y)
(x)^(-1)
```

## A Word
The ultimate goal of this project is to construct a symbolic riemannian geometry engine capable of computing the fundamental tensors and Christoffel symbols associated with a given metric. If you
have anything you would like to contribute, feel free to message me on instagram (@wheesman), linkdin (www.linkedin.com/in/luis-cuevas-73634a1b1), or on here (if github has a message feature.)


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Big shoutout to Ruslan Spivak for the tutorial on building interpreters. Their blog post at https://ruslanspivak.com/lsbasi-part1/ is super informative.
