from __future__ import division

import re

import sympy


def parse(expr_str):
    try:
        expr = sympy.sympify(expr_str)
        return _print_expr(expr)
    except sympy.SympifyError:
        return 'Please input right expression'
    except TypeError:
        return 'Type error'


def _print_expr(expr):
    res = expr.doit()
    res_str = _convert_xor(str(res))
    simp_str = _convert_xor(res.simplify())
    return_string = 'result:\n{}\n\nsimplified result:\n{}'.format(res_str, simp_str)
    return return_string


def _convert_xor(expr_str):
    return re.sub('\*\*', '^', expr_str)
