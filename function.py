from __future__ import annotations
from variable import Variable
from constant import Constant
import math

class Function:
    def __init__(self, operation: str, functions: list[Function]) -> None:
        '''
        Creates a new Function.

        Args:
            operation (str): The function's operation.
            functions (list[Function]): The functions combined using the operation.
        '''
        self.functions: list[Function] = functions
        self.operation: str = operation

    def __str__(self) -> str:
        '''
        Converts the Function to a readable string.

        Returns:
            str: A string representing the Function.
        '''
        return self.str_helper(False)

    def str_helper(self, put_parenthesees=True) -> str:
        '''
        A helper function used to simplify Function strings.

        Args:
            put_parenthesees (bool): If parenthesees will be added around the entire function (for recursion purposes).

        Returns:
            str: A string representing the Function.
        '''
        from simplifier import Simplifier
        res: str = ''
        if self.operation == '*' and Simplifier.is_simplified(self):
            if self.functions[0] == Constant('-1'):
                res = f'(-{"".join([fun.str_helper() for index, fun in enumerate(self.functions) if index > 0])})'
            else:
                res = f'({"".join([fun.str_helper() for fun in self.functions])})'
        elif self.operation == '*':
            res = f'({"*".join([fun.str_helper() for fun in self.functions])})'
        elif self.operation == '+' and Simplifier.is_simplified(self):
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

    def diff(self, var: str = 'x', times: int = 1) -> Function:
        '''
        Differentiates the Function.

        Args:
            var (str): The differentiating variable.
            times (int): The number of times to differentiate the Function.
        
        Returns:
            Function: The differentiated Function.
        '''
        from simplifier import Simplifier
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
            res = Simplifier.simplify(res)
        return res

    def diff_eval(self, vars: tuple[float] | float | dict) -> float:
        '''
        Evaluates the derivative of the Function.

        Args:
            vars (tuple[float] | float | dict): The values of the variables.

        Returns:
            float: The derivative of the Function.
        '''
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
    
    def eval(self, vars: tuple[float] | float | dict) -> float:
        '''
        Evaluates the Function.

        Args:
            vars (tuple[float] | float | dict): The values of the variables.

        Returns:
            float: The evaluation of the Function.
        '''
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

    def newton_raphson(self, guess: float) -> float:
        '''
        Finds a zero of the function.

        Args:
            guess (float): The starting value to check.

        Raises:
            ValueError: If the guess passed to the function creates a loop.

        Returns:
            float: A zero of the function or the last value before an errror occurred.
        '''
        vals = set()

        try:
            last_guess = guess
            guess -= (self.eval(guess) / self.diff_eval(guess))
            while last_guess != guess:
                last_guess = guess
                guess -= self.eval(guess) / self.diff_eval(guess)
                if guess in vals: raise ValueError()
                vals.add(guess)
        except ValueError:
            print(f'There was a repeated value: {guess}')
        except:
            print(f'A problem has occurred: \nValue: {guess}')
        finally:
            return guess

    def copy(self) -> Function:
        '''
        Creates a copy of the Function.

        Returns:
            Function: The copy of the Function.
        '''
        return Function(self.operation, [fun.copy() for fun in self.functions])
    
    def __add__(self, other: Function | Variable | Constant) -> Function:
        '''
        Adds a Function and a Constant, Variable or another Function.

        Args:
            other (Constant | Variable | Function): The value to be added.
        
        Returns:
            Function: The sum of the two values.
        '''
        return Function('+', [self.copy(), other.copy()])
    
    def __sub__(self, other: Function | Variable | Constant) -> Function:
        '''
        Subtracts a Function and a Constant, Variable or another Function.

        Args:
            other (Constant | Variable | Function): The value to be subtracted.
        
        Returns:
            Function: The difference of the two values.
        '''
        return Function('-', [self.copy(), other.copy()])
    
    def __mul__(self, other: Function | Variable | Constant) -> Function:
        '''
        Multiplies a Function and a Constant, Variable or another Function.

        Args:
            other (Constant | Variable | Function): The value to be multiplied.
        
        Returns:
            Function: The product of the two values.
        '''
        return Function('*', [self.copy(), other.copy()])
    
    def __truediv__(self, other: Function | Variable | Constant) -> Function:
        '''
        Divides a Function and a Constant, Variable or another Function.

        Args:
            other (Constant | Variable | Function): The value to be divided.
        
        Returns:
            Function: The quotient of the two values.
        '''
        return Function('/', [self.copy(), other.copy()])
    
    def __pow__(self, other: Function | Variable | Constant) -> Function:
        '''
        Raises a Function to a power of a Constant, Variable or another Function.

        Args:
            other (Constant | Variable | Function): The exponent.
        
        Returns:
            Function: The power of the two values.
        '''
        return Function('^', [self.copy(), other.copy()])

    def __neg__(self) -> Function:
        '''
        Creates a negated version of the Function.
        
        Returns:
            Function: The negated Function.
        '''
        return Constant('-1') * self

    def __eq__(self, other: Function) -> bool:
        '''
        Checks if two Functions are equal.

        Args:
            other (Function): The Function to be compared against.

        Returns:
            bool: If the two Functions are equal.
        '''
        return isinstance(other, Function) and self.operation == other.operation and self.functions == other.functions
    
    def __lt__(self, other: Function) -> bool:
        '''
        Checks if one Function is less than another.

        Args:
            other (Function): The Function to be compared against.

        Returns:
            bool: If the Function is less than other.
        '''
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
        '''
        Checks if a Function is 'negative'.

        Args:
            fun (Function): The Function to be checked.

        Returns:
            bool: If the Function is negative.
        '''
        if not isinstance(fun, Function): return False
        if fun.operation != '*': return False

        for f in fun.functions:
            if f < Constant('0'):
                return True
        return False