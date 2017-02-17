ABOUT_TEXT = """ MyCalc - Utility to help you solve mathematics problems
This bot is created by anakarwin@gmail.com.
Send me suggestion to support this bot or just line me id: anakarwin.
This bot is created using python programming language,
using library called sympy (http://www.sympy.org/en/index.html).
All available commands are store in their website, try it your self.
Believe me, everyone can code. Learn how to code in http://code.org.
You can create your own program. If you wanna share or ask anything about programming, please tell me.

--------
MyCalc version 0.2.0
"""

COMMANDS_HELP = {
    "diff": """ diff(expr) - return derivative of expr
ex:
diff(cos(x))
>>  result:
    -sin(x)
""",
    "expand": """ expand(expr) - expand polynomial from expr
ex:
expand((x + 1)^2)
>>> result:
    x^2 + 2*x + 1
""",
    "expand_trig": """ expand_trig(expr) - expand trigonometry of expr
ex:
expand_tri(sin(2**x))
>>> result:
    2*sin(x)*cos(x)

expand_tri(sin(x + y))
>>> result:
    sin(x)*cos(y) + sin(y)*cos(x)
""",
    "factor": """ factor(expr) - return factor of expr
ex:
factor(x^2 - 2*x - 8)
>>> result:
    (x - 4)*(x + 2)
""",
    "fog": """ fog(f, g) - return f(g(x)).
Use 'fog(f, g, v)' to change x=v
ex:
fog(x^2 - 4*x + 6, 2*x + 3)
>>> result:
    4*x^2 + 4*x + 3

fog(x^2 - 4*x + 6, 2*x + 3, 6)
>>> result:
    171
""",
    "integrate": """ integrate(expr) - return integral of expr
ex:
integrate(sin(x))
>>> result:
    -cos(x)
""",
    "inverse_function": """ inverse_func(f) - return inverse of funtion f
ex:
inverse_func(x + 1)
>>> result:
    x - 1
""",
    "limit": """ limit(expr, base, target) - limit of base to target from expr
using double o (oo) as infinity
ex:
limit(1/x, x, 0)
>>> result:
    oo

[CHEAT] using forth parameter '+' or '-' to evaluate limit one sided
ex:
limit(1/x, x, 0, '-')
>>> result:
    -oo
""",
    "log": """ log(expr) - natural logarithm of expr (base 'e')
log(expr, b) - logarithm of expr with base 'b'
log(expr, b) execute as log(expr) / log(b)
ex:
log(exp(1))
>>> result:
    1

log(4, 2)
>>> result:
    2

log(1/4, 2)
>>> result:
    -1.38629436111989/log(2)
""",
    "series": """ series(expr) - return taylor series of expr
ex:
series(sin(x))
>>> result:
    x - x^3/6 + x^5/120 + O(x^6)
""",
    "simplify_logic": """ simplify_logic(log_expr) - simplify logical expression in log_expr
use & for conjuntion
use | for disjunction
use ~ for negation
use << or >> for implication
ex:
simplify_logic(p>>q)
>>> result:
    (q | ~p)

simplify_logic(p | ~(q & r))
>>> result:
    (p | ~q | ~r)

simplify_logic(~((p<<q) & (p>>q)))
>>> result:
    ((p & ~q) | (q & ~p))
""",
    "sqrt": """ sqrt(expr) - square root of expr
ex:
sqrt(1/100)
>>> result:
    1/10
""",
    "solve": """ solve(expr) - solve equations of expr
returns array of solution
ex:
solve(x^2 + 2*x + 1)
>>> result:
    [-1]
""",
    "abs": """ abs(expr) - absolute of expr
ex:
abs(sin(-pi/2))
>>> result:
    1
""",
    "matrix": """ Matrix can be used by passing matrices
ex:
create matrix with 2 row 1 column
| 1 |
| 2 |

Matrix([1, 2])
>>> result:
Matrix([1, 2])

--------------
create matrix with 1 row 2 column
| 1 2 |

Matrix([[1, 2]])
>>> result:
Matrix([[1, 2]])

--------------
multiply matrix 2x1 with 1x2
| 1 | * | 1 2 |
| 2 |

| 1 2 |
| 2 4 |

Matrix([1,2]) * Matrix([[1,2]])
>>> result:
    Matrix([[1,2], [2,4]])

--------------
determinant - add .det() as suffix
Matrix([[1,2], [2,3]])
>>> result:
    -1

--------------
transpose - add .T as suffix
Matrix([1,2], [3,4])
>>> result:
    Matrix([[1, 3], [2, 4]])
"""
}

DEFAULT_HELP = """ MyCalc - @ist0487t
Utility to help you solve mathematics problems

You can compute simple math as '1+1' or more complex math using functions.
These is available function:

diff(expr) - derivative of expr
expand(expr) - expand polynomial from expr
expand_trig(expr) - expand trigonometry of expr
factor(expr) - factor of expr (polynomial)
fog(f, g) - return f(g(x)). use 'fog(f, g, v)' to change x=v
integrate(expr) - integral of expr
inverse_function(f) - return inverse of function f
limit(expr, base, target) - limit of base to target from expr
log(expr) - natural logarithm of expr (base 'e')
log(expr, b) - logarithm of expr with base 'b'
series(expr) - taylor series of expr
simplify_logic(log_expr) - simplify logical expression in log_expr
solve(expr) - solve equations of expr
matrix(nums) - create matrix object. see 'help matrix'

Type 'help <function>' to show more details about function.

available trigonometry: sin, cos, tan, asin, acos, atan, sec, csc, cot, asec, acsc, acot
hyperbolic function: sinh, cosh, tanh
commons function: abs, deg, factorial, rad, sqrt
commons constant: oo, pi

notes: expr using mathematical logic
using 2*x instead of 2x or
using 2*(x^2+x) instead of 2(x^2+x)
expr can be stacked, ex:
integrate(sqrt(1/x))

Cheat:
Try add .evalf() as a suffix (on the end of expression)
    ex: log(1/4, 2).evalf()
Try add .rewrite(func) as a suffix (on the end of expression)
    ex: tan(x).rewrite(sin)
Type 'about' of you have a bit of curiosity.
"""
