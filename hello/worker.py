from __future__ import division

import re

import sympy

ABOUT_TEXT = """ MyCalc - Utility to help you solve mathematics problems
This bot is created by anakarwin@gmail.com.
Send me suggestion to support this bot or just line me id: anakarwin.
This bot is created using python programming language,
using library called sympy (http://www.sympy.org/en/index.html).
All available commands are store in their website, try it your self.
Believe me, everyone can code. Learn how to code in http://code.org.
You can create your own program. If you wanna share or ask anything about programming, please tell me.

--------
MyCalc version 0.1.0
"""
COMMANDS_HELP = {
    "diff": """ diff(expr) - return derivative of expr
ex:
diff(cos(x))
>>  result:
    -sin(x)
""",
    "factor": """ factor(expr) - return factor of expr
ex:
factor(x^2 - 2*x - 8)
>>> result:
    (x - 4)*(x + 2)
""",
    "integrate": """ integrate(expr) - return integral of expr
ex:
integrate(sin(x))
>>> result:
    -cos(x)
""",
    "series": """ series(expr) - return taylor series of expr
ex:
series(sin(x))
>>> result:
    x - x^3/6 + x^5/120 + O(x^6)
""",
    "expand_tri": """ expand_trig(expr) - expand trigonometry of expr
ex:
expand_tri(sin(2**x))
>>> result:
    2*sin(x)*cos(x)

expand_tri(sin(x + y))
>>> result:
    sin(x)*cos(y) + sin(y)*cos(x)
""",
    "sqrt": """ sqrt(expr) - square root of expr
ex:
sqrt(1/100)
>>> result:
    1/10
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

[CHEAT] using .evalf() in the end to get the result
ex:
log(1/4, 2).evalf()
>>> result:
    -2.00000000000
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
    "expand": """ expand(expr) - expand polynomial from expr
ex:
expand((x + 1)^2)
>>> result:
    x^2 + 2*x + 1
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
integrate(expr) - integral of expr
limit(expr, base, target) - limit of base to target from expr
log(expr) - natural logarithm of expr (base 'e')
log(expr, b) - logarithm of expr with base 'b'
series(expr) - taylor series of expr
solve(expr) - solve equations of expr

Type 'help <function>' to show more details about function.

available trigonometry: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, sec, csc, cot, asec, acsc, acot
commons function: abs, deg, factorial, rad, sqrt
commons constant: inf, oo, pi

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
Type 'help matrix' to know how to use matrix
Type 'about' of you have a bit of curiosity.
"""


def exec_command(command_str):
    if 'help' in command_str:
        temp = re.split('\s+', command_str.strip())
        if len(temp) == 1:
            return DEFAULT_HELP
        else:
            if COMMANDS_HELP.has_key(temp[1]):
                return COMMANDS_HELP[temp[1]]
            else:
                return 'help for function {} currently not available.'.format(temp[1])

    elif 'about' in command_str:
        return ABOUT_TEXT
    elif 'plot' in command_str:
        return """ We currently not support plot view """
    elif 'source' in command_str:
        return """ You cannot see the source of code via Line """
    else:
        if 'matrix' in command_str:
            return _parse(re.sub('matrix', 'Matrix', command_str))
        return _parse(command_str)


def _parse(expr_str):
    try:
        expr = sympy.sympify(expr_str)
        return _print_expr(expr)
    except sympy.SympifyError as e:
        print(e)
        return 'Please input right expression'
    except TypeError as e:
        print(e)
        return 'Type error'


def _print_expr(expr):
    try:
        res_str = _convert_xor(str(expr))
        simp_str = _convert_xor(str(expr.simplify()))
        eval_str = _convert_xor(str(expr.evalf()))
        return_string = 'result:\n{}'.format(res_str)
        if res_str != eval_str:
            return_string  += '\n\nevaluated result:\n{}'.format(eval_str)
        if res_str != simp_str and eval_str != simp_str:
            return_string += '\n\nsimplified result:\n{}'.format(simp_str)
        return return_string
    except AttributeError as e:
        print(e)
        res_str = _convert_xor(str(expr))
        return 'result:\n{}'.format(res_str)
    except Exception as e:
        print(e)
        return 'Oops something wrong'


def _convert_xor(expr_str):
    return re.sub('\*\*', '^', expr_str)
