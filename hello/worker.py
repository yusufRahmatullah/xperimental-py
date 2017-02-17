from __future__ import division

import re
import sympy

from constants import *


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
        return 'We currently not support plot view'
    elif 'source' in command_str:
        return 'You cannot see the source of code via Line'
    else:
        if 'matrix' in command_str:
            clean_expr = re.sub('matrix\*\(', 'matrix(', command_str)
            return _parse(re.sub('matrix', 'Matrix', clean_expr))
        elif 'simplify' in command_str:
            clean_expr = re.sub('simplify\*', 'simplify', command_str)
            return _parse(clean_expr)
        elif 'simplify_logic' in command_str:
            logic_expr = sympy.sympify(command_str)
            return _print_expr(_logic_to_str(logic_expr))
        elif 'inverse_function' in command_str:
            # assume user enter inverse_function(expr)
            if 'x' not in command_str:
                return 'Please use x as variable'
            clean_str = re.sub('inverse_function\s?\(', '', command_str)[:-1] # clear the function name
            temp = _parse('solve(({}) - y, x)'.format(clean_str))
            return temp.replace('y', 'x')
        elif 'fog' in command_str:
            # assume user enter fog(f, g) to execute f(g(x)) or fog(f, g, v) to execute f(g(x)) with x=v
            clean_str = re.sub('fog\s?\(', '', command_str)[:-1] # clear the fog()
            params = re.split('\,\s?', clean_str) # this must be 2 or 3 params
            if len(params) < 2 and len(params) > 3:
                return 'Wrong format. Usage: fog(f, g) for f(g(x)) or fog(f, g, v) for f(g(x)) with x=v'
            else:
                try:
                    x = first_symbol = re.findall('[x-z]', clean_str)[0]    # find first symbol, maybe x, y, or z
                except IndexError:
                    return 'Use x, y, or z for valid variable'
                g = sympy.sympify(params[1])
                fog = sympy.sympify(re.sub(x, '({})'.format(g), params[0]))
                if len(params) == 2:
                    return _print_expr(fog)
                else:
                    value = float(params[2]) if '.' in params[2] else int(params[2])
                    return _print_expr(fog.subs(sympy.Symbol(x), value))
        elif 'solve' in command_str and 'solve_univariate_inequality' not in command_str and \
            ('>' in command_str or '<' in command_str or '>=' in command_str or '<=' in command_str):
            # assume user enter solve(expr)
            expr_str = re.sub('solve\s?\(', '', command_str)
            expr_str = expr_str[:-1]
            try:
                first_symbol = re.findall('[x-z]', expr_str)[0]
            except IndexError:
                return 'Use x, y, or z for valid variable'
            return _parse('solve_univariate_inequality({}, {})'.format(expr_str, first_symbol))
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
        eval_expr = expr.evalf()
        simp_expr = expr.simplify()
        expand_expr = sympy.expand(expr)
        expand_trig_expr = sympy.expand_trig(expr)
        factor_expr = sympy.factor(expr)
        
        res_str = _convert_xor(str(expr))
        return_string = 'result:\n{}'.format(res_str)
        if expr != eval_expr and None != eval_expr:
            eval_str = _convert_xor(str(eval_expr))
            return_string  += '\n\nalternative (eval with float):\n{}'.format(eval_str)
        if expr != simp_expr and None != simp_expr:
            simp_str = _convert_xor(str(simp_expr))
            return_string += '\n\nalternative (simplified):\n{}'.format(simp_str)
        if expr != expand_expr and None != expand_expr:
            expand_str = _convert_xor(str(expand_expr))
            return_string += '\n\nalternative (expanded):\n{}'.format(expand_str)
        elif expr != expand_trig_expr and None != expand_trig_expr:
            expand_trig_str = _convert_xor(str(expand_trig_expr))
            return_string += '\n\nalternative (trigonometry expanded):\n{}'.format(expand_trig_str)
        elif expr != factor_expr and None != factor_expr:
            factor_str = _convert_xor(str(factor_expr))
            return_string += '\n\nalternative (factor):\n{}'.format(factor_str)
        return return_string
    except AttributeError as e:
        print(e)
        res_str = _convert_xor(str(expr))
        return 'result:\n{}'.format(res_str)
    except Exception as e:
        print(e)
        return 'Oops something wrong'


def _convert_xor(expr_str):
    clean_expr = re.sub('\*\*', '^', expr_str)
    clean_expr = re.sub('([\d\)x-z])\*([x-z\(])', r'\g<1>\g<2>', clean_expr)
    clean_expr = re.sub('([\d\)x-z])\*sqrt', r'\g<1>' + 'sqrt', clean_expr)
    return clean_expr


def _logic_to_str(expr):
    if isinstance(expr, sympy.Symbol):
        return str(expr)
    elif isinstance(expr, sympy.And):
        arr = []
        for arg in expr.args:
            arr.append(_logic_to_str(arg))
        return '({})'.format(' & '.join(arr))
    elif isinstance(expr, sympy.Or):
        arr = []
        for arg in expr.args:
            arr.append(_logic_to_str(arg))
        return '({})'.format(' | '.join(arr))
    elif isinstance(expr, sympy.Implies):
        arr = []
        for arg in expr.args:
            arr.append(_logic_to_str(arg))
        return '({})'.format(' >> '.join(arr))
    elif isinstance(expr, sympy.Not):
        return '~{}'.format(_logic_to_str(expr.args[0]))
