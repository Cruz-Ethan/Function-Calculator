from __future__ import annotations
from parser import Parser
from variable import Variable
from constant import Constant
from collections import deque, Counter
import math

class Function:
    def __init__(self, operation: str, functions: Function) -> None:
        self.functions: list[Function] = functions
        self.operation: str = operation

    @classmethod
    def generate_function(cls, eq: str) -> Function:
        operation_stack: list[str] = deque()
        value_stack: list[Function] = deque()
        eq = Parser.parse(eq)
        index = 0

        while index < len(eq):
            if eq[index] in '1234567890πe' or (eq[index] == '-' and (index == 0 or eq[index - 1] in '(+-*/^')):
                start_index = index
                end_index = Function.__find_end_index(eq, start_index + 1 if eq[index] == '-' else start_index)
                value_stack.append(Constant(eq[start_index:end_index]))
                index = end_index
                continue
            elif eq[index] in '+-*/^œå‰˝˙®©ÍÇˇßç†Ò¬':
                translation = {
                    '+': '+',
                    '-': '-',
                    '*': '*',
                    '/': '/',
                    '^': '^',
                    'œ': 'sqrt',
                    'å': 'arcsinh',
                    '‰': 'arcosh',
                    '˝': 'arctanh',
                    '˙': 'sinh',
                    '®': 'cosh',
                    '©': 'tanh',
                    'Í': 'arcsin',
                    'Ç': 'arccos',
                    'ˇ': 'arctan',
                    'ß': 'sin',
                    'ç': 'cos',
                    '†': 'tan',
                    '¬': 'ln',
                    'Ò': 'log'
                }
                operation_stack.append(translation[eq[index]])
            elif eq[index].lower() in 'qwrtyuiopasdfghjklzxcvbnm' or eq[index] == 'E':
                value_stack.append(Variable(eq[index]))
            elif eq[index] == ')':
                fun: Function = value_stack.pop()
                operation: str = operation_stack.pop()
                res_fun: Function
                if operation in '+-*/^':
                    res_fun = Function(operation, [value_stack.pop(), fun])
                else:
                    res_fun = Function(operation, [fun])
                value_stack.append(res_fun)
            index += 1
        return value_stack.pop()

    def eval(self, vars: tuple[float] | float | dict) -> float:
        res: float = float('inf')
        match self.operation:
            case '+':
                res = sum([fun.eval(vars) for fun in self.functions])
            case '-':
                res = self.functions[0].eval(vars) - self.functions[1].eval(vars)
            case '*':
                res = 1
                for fun in self.functions:
                    res *= fun.eval(vars)
            case '/':
                res = self.functions[0].eval(vars) / self.functions[1].eval(vars)
            case '^':
                res = self.functions[0].eval(vars) ** self.functions[1].eval(vars)
            case 'sqrt':
                res = math.sqrt(self.functions[0].eval(vars))
            case 'ln':
                res = math.log(self.functions[0].eval(vars))
            case 'log':
                res = math.log10(self.functions[0].eval(vars))
            case 'sin':
                res = math.sin(self.functions[0].eval(vars))
            case 'cos':
                res = math.cos(self.functions[0].eval(vars))
            case 'tan':
                res = math.tan(self.functions[0].eval(vars))
            case 'arcsin':
                res = math.asin(self.functions[0].eval(vars))
            case 'arccos':
                res = math.acos(self.functions[0].eval(vars))
            case 'arctan':
                res = math.atan(self.functions[0].eval(vars))
            case 'sinh':
                res = math.sinh(self.functions[0].eval(vars))
            case 'cosh':
                res = math.cosh(self.functions[0].eval(vars))
            case 'tanh':
                res = math.tanh(self.functions[0].eval(vars))
            case 'arcsinh':
                res = math.asinh(self.functions[0].eval(vars))
            case 'arccosh':
                res = math.acosh(self.functions[0].eval(vars))
            case 'arctanh':
                res = math.atanh(self.functions[0].eval(vars))
        return res

    def diff_eval(self, vars: tuple[float] | float | dict) -> float:
        res: float = float('inf')
        match self.operation:
            case '+':
                res = sum([fun.diff_eval(vars) for fun in self.functions])
            case '-':
                res = self.functions[0].diff_eval(vars) - self.functions[1].diff_eval(vars)
            case '*':
                res = 0
                for fun in self.functions:
                    product = 1
                    for prod_fun in self.functions:
                        if prod_fun == fun:
                            product *= prod_fun.diff_eval(vars)
                        else:
                            product *= prod_fun.eval(vars)
                    res += product
            case '/':
                res = ((self.functions[0].diff_eval(vars) * self.functions[1].eval(vars)) - (self.functions[0].eval(vars) * self.functions[1].diff_eval(vars))) / (self.functions[1].eval(vars) ** 2)
            case '^':
                if isinstance(self.functions[0], Constant) and isinstance(self.functions[1], Constant):
                    return 0
                if isinstance(self.functions[1], Constant):
                    res = self.eval(vars) * (self.functions[0].diff_eval(vars) * self.functions[1].eval(vars) / self.functions[0].eval(vars))
                elif isinstance(self.functions[0], Constant):
                    res = self.eval(vars) * (self.functions[1].diff_eval(vars) * math.log(self.functions[0].eval(vars)))
                else:
                    res = self.eval(vars) * ((self.functions[0].diff_eval(vars) * self.functions[1].eval(vars) / self.functions[0].eval(vars)) + (self.functions[1].diff_eval(vars) * math.log(self.functions[0].eval(vars))))
            case 'sqrt':
                res = (self.functions[0].diff_eval(vars)) / (2 * math.sqrt(self.functions[0].eval(vars)))
            case 'ln':
                res = (self.functions[0].diff_eval(vars)) / (self.functions[0].eval(vars))
            case 'log':
                res = (self.functions[0].diff_eval(vars)) / (self.functions[0].eval(vars) * math.log(10))
            case 'sin':
                res = self.functions[0].diff_eval(vars) * math.cos(self.functions[0].eval(vars))
            case 'cos':
                res = -self.functions[0].diff_eval(vars) * math.sin(self.functions[0].eval(vars))
            case 'tan':
                res = self.functions[0].diff_eval(vars) / (math.cos(self.functions[0].eval(vars)) ** 2)
            case 'arcsin':
                res = self.functions[0].diff_eval(vars) / math.sqrt(1 - (self.functions[0].eval(vars) ** 2))
            case 'arccos':
                res = -self.functions[0].diff_eval(vars) / math.sqrt(1 - (self.functions[0].eval(vars) ** 2))
            case 'arctan':
                res = self.functions[0].diff_eval(vars) / (1 + (self.functions[0].eval(vars) ** 2))
            case 'sinh':
                res = self.functions[0].diff_eval(vars) * math.cosh(self.functions[0].eval(vars))
            case 'cosh':
                res = self.functions[0].diff_eval(vars) * math.sinh(self.functions[0].eval(vars))
            case 'tanh':
                res = self.functions[0].diff_eval(vars) / (math.cosh(self.functions[0].eval(vars)) ** 2)
            case 'arcsinh':
                res = self.functions[0].diff_eval(vars) / math.sqrt(1 + (self.functions[0].eval(vars) ** 2))
            case 'arccosh':
                res = self.functions[0].diff_eval(vars) / math.sqrt((self.functions[0].eval(vars) ** 2) - 1)
            case 'arctanh':
                res = self.functions[0].diff_eval(vars) / (1 - (self.functions[0].eval(vars) ** 2))
        return res
    
    def newton_raphson(self, guess: float) -> float:
        vals = set()

        try:
            while abs(self.eval(guess)) > 1.0e-13:
                guess -= self.eval(guess) / self.diff_eval(guess)
                if guess in vals: raise ValueError()
                vals.add(guess)
        except ValueError:
            print(f'There was a repeated value: {guess}')
        except:
            print(f'A problem has occurred: \nValue: {guess}')
        finally:
            return guess

    def diff(self, var: str = 'x', times: int = 1) -> Function:
        res: Function = self.copy()

        for _ in range(times):
            if not isinstance(res, Function):
                res = res.diff()
                continue
            match res.operation:
                case '+':
                    for index in range(0, len(res.functions)):
                        res.functions[index] = res.functions[index].diff(var)
                case '-':
                    res = res.functions[0].diff(var) - res.functions[1].diff(var)
                case '*':
                    res_arr = []
                    for fun in res.functions:
                        prod_arr = []
                        for prod_fun in res.functions:
                            if prod_fun == fun:
                                prod_arr.append(prod_fun.diff(var))
                            else:
                                prod_arr.append(prod_fun.copy())
                        res_arr.append(Function('*', prod_arr))
                    res = Function('+', res_arr)
                case '/':
                    if isinstance(res.functions[0], Constant):
                        res = -res.functions[0] * res.functions[1].diff(var) / (res.functions[1] ** Constant('2'))
                    elif isinstance(res.functions[1], Constant):
                        res = res.functions[0].diff(var) / res.functions[1]
                    else:
                        res = ((res.functions[0].diff(var) * res.functions[1]) - (res.functions[0] * res.functions[1].diff(var))) / (res.functions[1] ** Constant('2'))
                case '^':
                    if isinstance(res.functions[0], Constant):
                        res = res * res.functions[1].diff(var) * Constant(math.log(res.functions[0].num))
                    elif isinstance(res.functions[1], Constant):
                        res = res.functions[0].diff(var) * res.functions[1] * (res.functions[0] ** Constant(res.functions[1].num - 1))
                    else:
                        res = res * ((res.functions[0].diff(var) * res.functions[1] / res.functions[0]) + (res.functions[1].diff(var) * Function('ln', [res.functions[0]])))
                case 'sqrt':
                    res = (res.functions[0].diff(var)) / (Constant('2') * res)
                case 'ln':
                    res = res.functions[0].diff(var) / res.functions[0]
                case 'log':
                    res = res.functions[0].diff(var) / (res.functions[0] * Constant(math.log(10)))
                case 'sin':
                    res = res.functions[0].diff(var) * Function('cos', [res.functions[0]])
                case 'cos':
                    res = -res.functions[0].diff(var) * Function('sin', [res.functions[0]])
                case 'tan':
                    res = res.functions[0].diff(var) / (Function('cos', [res.functions[0]]) ** Constant('2'))
                case 'arcsin':
                    res = res.functions[0].diff(var) / Function('sqrt', [Constant('1') - (res.functions[0] ** Constant('2'))])
                case 'arccos':
                    res = -res.functions[0].diff(var) / Function('sqrt', [Constant('1') - (res.functions[0] ** Constant('2'))])
                case 'arctan':
                    res = res.functions[0].diff(var) / (Constant('1') + (res.functions[0] ** Constant('2')))
                case 'sinh':
                    res = res.functions[0].diff(var) * Function('cosh', [res.functions[0]])
                case 'cosh':
                    res = res.functions[0].diff(var) * Function('sinh', [res.functions[0]])
                case 'tanh':
                    res = res.functions[0].diff(var) / (Function('cosh', [res.functions[0]]) ** Constant('2'))
                case 'arcsinh':
                    res = res.functions[0].diff(var) / Function('sqrt', [Constant('1') + (res.functions[0] ** Constant('2'))])
                case 'arccosh':
                    res = res.functions[0].diff(var) / Function('sqrt', [(res.functions[0] ** Constant('2')) - Constant('1')])
                case 'arctanh':
                    res = res.functions[0].diff(var) / (Constant('1') - (res.functions[0] ** Constant('2')))
            res = res.simplify()
        return res

    def __str__(self) -> str:
        return self.str_helper(False)

    def str_helper(self, put_parenthesees=True) -> str:
        res: str = ''
        if self.operation == '*' and self.is_simplified():
            if self.functions[0] == Constant('-1'):
                res = f'(-{"".join([fun.str_helper() for index, fun in enumerate(self.functions) if index > 0])})'
            else:
                res = f'({"".join([fun.str_helper() for fun in self.functions])})'
        elif self.operation == '*':
            res = f'({"*".join([fun.str_helper() for fun in self.functions])})'
        elif self.operation == '+' and self.is_simplified():
            res = '(' + self.functions[0].str_helper()
            for index in range(1, len(self.functions)):
                if not Function.__is_negative(self.functions[index]):
                    res += '+'
                if self.functions[index].str_helper()[0] == '(' and self.functions[index].str_helper()[-1] == ')':
                    res += self.functions[index].str_helper()[1:-1]
                else:
                    res += self.functions[index].str_helper()
            res += ')'
        elif self.operation == '+':
            res = f'({self.operation.join([fun.str_helper() for fun in self.functions])})'
        elif self.operation in '-/^':
            res = f'({self.functions[0].str_helper()}{self.operation}{self.functions[1].str_helper()})'
        else:
            res = f'({self.operation}{self.functions[0].str_helper()})'
        return res if put_parenthesees else res[1:-1]

    def __add__(self, other: Function | Variable | Constant) -> Function:
        return Function('+', [self.copy(), other.copy()])
    
    def __sub__(self, other: Function | Variable | Constant) -> Function:
        return Function('-', [self.copy(), other.copy()])
    
    def __mul__(self, other: Function | Variable | Constant) -> Function:
        return Function('*', [self.copy(), other.copy()])
    
    def __truediv__(self, other: Function | Variable | Constant) -> Function:
        return Function('/', [self.copy(), other.copy()])
    
    def __pow__(self, other: Function | Variable | Constant) -> Function:
        return Function('^', [self.copy(), other.copy()])

    def __neg__(self) -> Function:
        return Constant('-1') * self

    def __eq__(self, other: Function) -> bool:
        return isinstance(other, Function) and self.operation == other.operation and self.functions == other.functions
    
    def __lt__(self, other: Function) -> bool:
        if not isinstance(other, Function):
            return False
        if self == other:
            return False
        if self.operation != other.operation:
            return self.operation < other.operation
        
        if self.operation == '*':
            term_self = [fun.copy() for fun in self.functions if not isinstance(fun, Constant)] if self.operation == '*' else self.functions
            term_other = [fun.copy() for fun in other.functions if not isinstance(fun, Constant)] if other.operation == '*' else other.functions

            if len(term_self) != len(term_other):
                return len(term_self) < len(term_other)
            for index in range(len(term_self)-1, -1, -1):
                if term_self[index] != term_other[index]:
                    return term_self[index] < term_other[index]
            return Function.__get_coefficient(self) < Function.__get_coefficient(other)
        
        if len(self.functions) != len(other.functions):
            return len(self.functions) < len(other.functions)
        for index in range(len(self.functions)):
            if self.functions[index] != other.functions[index]:
                return self.functions[index] < other.functions[index]
        return False

    @classmethod
    def __is_negative(cls, fun: Function) -> bool:
        if not isinstance(fun, Function): return False
        if fun.operation != '*': return False

        for f in fun.functions:
            if f < Constant('0'):
                return True
        return False

    def simplify(self) -> Function:
        res = self.copy()
        while not res.is_simplified():
            res = res.simplify_helper()
        res.reorder()
        return res

    def reorder(self) -> None:
        for fun in self.functions:
            fun.reorder()
        if self.operation in '*+':
            self.functions.sort()

    def simplify_helper(self) -> Function:
        res: Function = Function(self.operation, [fun.simplify_helper() for fun in self.functions])

        isConstant: bool = True
        for fun in self.functions:
            if not isinstance(fun, Constant):
                isConstant = False
                break
        if isConstant:
            return Constant(res.eval(None))
        
        match res.operation:
            case '+':
                temp: list[Function] = []

                while res.functions:
                    fun = res.functions.pop(0)
                    if isinstance(fun, Function) and fun.operation == '+':
                        res.functions.extend(fun.functions)
                    elif isinstance(fun, Function) and fun.operation == '-':
                        res.functions.append(fun.functions[0])
                        res.functions.append(-fun.functions[1])
                    elif fun != Constant('0'):
                        temp.append(fun)
                res.functions = temp
                
                index = 0
                while index < len(res.functions):
                    other_index = index + 1
                    while other_index < len(res.functions):
                        if res.functions[index] == -res.functions[other_index]:
                            del res.functions[other_index]
                            del res.functions[index]
                            break
                        if Function.__are_like_terms(res.functions[index], res.functions[other_index]):
                            fun1: Function = res.functions.pop(other_index)
                            fun2: Function = res.functions.pop(index)
                            res.functions.append(Function.__combine_like_terms(fun1, fun2))

                        other_index += 1
                    else:
                        index += 1

                if not res.functions: return Constant('0')
                if len(res.functions) == 1: return res.functions[0]
            case '-':
                if res.functions[0] == Constant('0'): return -res.functions[1]
                if res.functions[1] == Constant('0'): return res.functions[0]
                if res.functions[0] == res.functions[1]: return Constant('0')
                res.operation = '+'
                res.functions[1] = -res.functions[1]
                res = res.simplify_helper()
            case '*':
                add_funs: list[Function] = []
                index = 0
                while index < len(res.functions):
                    fun = res.functions[index]
                    if fun == Constant('0'):
                        return Constant('0')
                    if fun == Constant('1'):
                        res.functions.pop(index)
                    elif isinstance(fun, Function) and fun.operation == '*':
                        res.functions.pop(index)
                        res.functions.extend(fun.functions)
                    elif isinstance(fun, Function) and fun.operation == '+':
                        add_funs.append(res.functions.pop(index))
                    else:
                        index += 1
                
                index = 0
                while index < len(res.functions):
                    other_index = index + 1
                    while other_index < len(res.functions):
                        if isinstance(res.functions[index], Constant) and isinstance(res.functions[other_index], Constant):
                            res.functions[index] *= res.functions.pop(other_index)
                        elif res.functions[index] == res.functions[other_index]:
                            res.functions[index] = Function('^', [res.functions.pop(other_index), Constant('2')])
                        elif isinstance(res.functions[other_index], Function) and res.functions[other_index].operation == '^' and res.functions[other_index].functions[0] == res.functions[index]:
                            res.functions[index] = res.functions.pop(other_index)
                            res.functions[index].functions[1] += Constant('1')
                        elif isinstance(res.functions[index], Function) and res.functions[index].operation == '^' and res.functions[index].functions[0] == res.functions[other_index]:
                            res.functions.pop(other_index)
                            res.functions[index].functions[1] += Constant('1')
                        elif isinstance(res.functions[index], Function) and res.functions[index].operation == '^' and isinstance(res.functions[other_index], Function) and res.functions[other_index].operation == '^' and res.functions[index].functions[0] == res.functions[other_index].functions[0]:
                            res.functions[index].functions[1] += res.functions[other_index].functions[1]
                            res.functions.pop(other_index)
                        else:
                            other_index += 1
                    
                    if res.functions[index] == Constant('1'):
                        res.functions.pop(index)

                    index += 1

                
                if not res.functions: res = Constant('1')
                elif len(res.functions) == 1: res = res.functions[0]

                if add_funs:
                    res = Function.__distribute(res, Function.__multiply_functions(add_funs))
                    res = Function(res.operation, [fun.simplify_helper() for fun in res.functions])

                if isinstance(res, Function) and res.operation == '*':
                    if not res.functions: return Constant('1')
                    if len(res.functions) == 1: return res.functions[0]
            case '/':
                fun1: Function = res.functions[0]
                fun2: Function = res.functions[1]

                if isinstance(fun1, Function) and fun1.operation in '+-':
                    for index in range(len(fun1.functions)):
                        fun1.functions[index] /= fun2
                    return fun1
                if isinstance(fun1, Function) and fun1.operation == '/' and isinstance(fun2, Function) and fun2.operation == '/':
                    res = (fun1.functions[0] * fun2.functions[1]) / (fun1.functions[1] * fun2.functions[0])
                    return res
                elif isinstance(fun1, Function) and fun1.operation == '/':
                    res = (fun1.functions[0]) / (fun1.functions[1] * fun2)
                    return res
                elif isinstance(fun2, Function) and fun2.operation == '/':
                    res = (fun1 * fun2.functions[1]) / (fun2.functions[0])
                    return res

                if isinstance(fun1, Function) and fun1.operation == '*' and isinstance(fun2, Function) and fun2.operation == '*':
                    index = 0
                    while index < len(fun1.functions):
                        for other_index in range(len(fun2.functions)):
                            if fun1.functions[index] == fun2.functions[other_index]:
                                del fun1.functions[index]
                                del fun2.functions[other_index]
                                break
                        else:
                            index += 1

                    res.functions[0] = fun1.simplify_helper()
                    res.functions[1] = fun2.simplify_helper()
                    fun1 = res.functions[0]
                    fun2 = res.functions[1]
                elif isinstance(fun1, Function) and fun1.operation == '*':
                    if fun2 in fun1.functions:
                        fun1.functions.remove(fun2)
                        return fun1.simplify_helper()
                elif isinstance(fun2, Function) and fun2.operation == '*':
                    if fun1 in fun2.functions:
                        fun2.functions.remove(fun1)
                        return Function('/', [Constant('1'), fun2.simplify_helper()]).simplify_helper()

                if isinstance(fun1, Constant) and isinstance(fun2, Constant): return Constant(res.eval(None))
                if fun1 == Constant('0'): return Constant('0')
                if fun2 == Constant('1'): return fun1
                if fun1 == fun2: return Constant('1')
                res = fun1 * (fun2 ** Constant('-1'))
                res = res.simplify()
            case '^':
                if isinstance(res.functions[0], Function) and res.functions[0].operation == '^':
                    res.functions = [res.functions[0].functions[0].simplify_helper(), (res.functions[0].functions[1] * res.functions[1]).simplify_helper()]
                if isinstance(res.functions[0], Function) and res.functions[0].operation == '*':
                    for index in range(len(res.functions[0].functions)):
                        res.functions[0].functions[index] **= res.functions[1]
                    return res.functions[0]

                if res.functions[1] == Constant('0'): return Constant('1')
                if res.functions[1] == Constant('1'): return res.functions[0]
                if res.functions[1] == Constant('0'): return Constant('0')
                if res.functions[0] == Constant('1'): return Constant('1')
        return res    

    def is_simplified(self) -> bool:
        return self == self.simplify_helper()

    @classmethod
    def __distribute(cls, fun1: Function, fun2: Function) -> Function:
        if not isinstance(fun2, Function) or not fun2.operation == '+':
            return fun1 * fun2

        fun2 = fun2.copy()
        if isinstance(fun1, Function) and fun1.operation == '*':
            for index in range(len(fun2.functions)):
                fun = fun1.copy()
                fun.functions.append(fun2.functions[index])
                fun2.functions[index].functions = fun.functions
        else:
            for index in range(len(fun2.functions)):
                fun2.functions[index] = Function('*', [fun1.copy(), fun2.functions[index]])
        return fun2.copy()

    @classmethod
    def __multiply_functions(cls, funs: list[Function]) -> Function:
        if not funs:
            return Constant('1')
        while len(funs) > 1:
            fun1 = funs.pop()
            fun2 = funs.pop()
            funs.append(cls.__multiply(fun1, fun2))
        return funs[0]
    
    @classmethod
    def __multiply(cls, fun1: Function, fun2: Function) -> Function:
        res: list[Function] = []
        for term1 in fun1.functions:
            for term2 in fun2.functions:
                res.append((term1 * term2).simplify_helper())
        return Function('+', res)

    @classmethod
    def __combine_like_terms(cls, fun1: Function, fun2: Function) -> Function:
        like_term: list[Function] = cls.__get_term(fun1)
        like_term.append(cls.__get_coefficient(fun1) + cls.__get_coefficient(fun2))
        return Function('*', like_term).simplify_helper()

    @classmethod
    def __are_like_terms(cls, fun1: Function, fun2: Function) -> bool:
        return cls.__get_term(fun1) == cls.__get_term(fun2)
    
    @classmethod
    def __get_coefficient(cls, term: Function) -> Constant:
        if isinstance(term, Constant):
            return term.copy()
        if isinstance(term, Function) and term.operation == '*':
            for fun in term.functions:
                if isinstance(fun, Constant):
                    return fun
        return Constant('1')
    
    @classmethod
    def __get_term(cls, term: Function) -> list[Function]:
        if isinstance(term, Constant):
            return [Constant('1')]
        if isinstance(term, Variable):
            return [term.copy()]
        if term.operation == '*':
            return sorted([fun.copy() for fun in term.functions if not isinstance(fun, Constant)])
        return term.copy()

    @classmethod
    def __find_end_index(cls, eq: str, start_index: int) -> int:
        while start_index < len(eq) and (eq[start_index] in '1234567890.pe'):
            start_index += 1
        return start_index

    def copy(self) -> Function:
        return Function(self.operation, [fun.copy() for fun in self.functions])