from __future__ import annotations
from constant import Constant

class Variable:
    def __init__(self, var: str) -> None:
        '''
        Creates a new Variable.

        Args:
            var (str): The name of the variable.
        '''
        self.index: int
        self.var: str = var
        match var:
            case 'x':
                self.index = 0
            case 'y':
                self.index = 1
            case 'z':
                self.index = 2
            case 'w':
                self.index = 3
            case 'v':
                self.index = 4
    
    def __str__(self) -> str:
        '''
        Converts the Variable to a readable string.

        Returns:
            str: A string representing the Variable.
        '''
        return self.var

    def str_helper(self) -> str:
        '''
        A helper function used to simplify Function strings.

        Returns:
            str: A string representing the Variable.
        '''
        return self.var

    def diff(self, var: str = 'x', times: int = 1) -> Constant | Variable:
        '''
        Differentiates the Variable.

        Args:
            var (str): The differentiating variable.
            times (int): The number of times to differentiate the Variable.
        
        Returns:
            Constant: The differentiated Variable.
        '''
        if times == 0: return self.copy()
        return Constant('1').diff(times - 1) if self.var == var else Variable(f'(d{self.var}/d{var})').diff(times - 1)

    def diff_eval(self, vars: tuple[float] | float | dict) -> float:
        '''
        Evaluates the derivative of the Variable.

        Args:
            vars (tuple[float] | float | dict): The values of the variables.

        Returns:
            float: The derivative of the Variable.
        '''
        return 1.0

    def eval(self, vars: tuple[float] | float | dict) -> float:
        '''
        Evaluates the Variable.

        Args:
            vars (tuple[float] | float | dict): The values of the variables.

        Returns:
            float: The evaluation of the Variable.
        '''
        if isinstance(vars, dict): return vars[self.var]
        return vars if isinstance(vars, float | int) else vars[self.index]
    
    def copy(self) -> Variable:
        '''
        Creates a copy of the Variable.

        Returns:
            Variable: The copy of the Variable.
        '''
        return Variable(self.var)
    
    def __add__(self, other):
        '''
        Adds a Variable and a Function, Constant, or another Variable.

        Args:
            other (Constant | Variable | Function): The value to be added.
        
        Returns:
            Function: The sum of the two values.
        '''
        from function import Function
        return Function('+', [self.copy(), other.copy()])
    
    def __sub__(self, other):
        '''
        Subtracts a Variable and a Function, Constant, or another Variable.

        Args:
            other (Constant | Variable | Function): The value to be subtracted.
        
        Returns:
            Function: The difference of the two values.
        '''
        from function import Function
        return Function('-', [self.copy(), other.copy()])
    
    def __mul__(self, other):
        '''
        Multiplies a Variable and a Function, Constant, or another Variable.

        Args:
            other (Constant | Variable | Function): The value to be multiplied.
        
        Returns:
            Function: The product of the two values.
        '''
        from function import Function
        return Function('*', [self.copy(), other.copy()])
    
    def __truediv__(self, other):
        '''
        Divides a Variable and a Function, Constant, or another Variable.

        Args:
            other (Constant | Variable | Function): The value to be divided.
        
        Returns:
            Function: The quotient of the two values.
        '''
        from function import Function
        return Function('/', [self.copy(), other.copy()])
    
    def __pow__(self, other):
        '''
        Raises a Variable to the power of a Function, Constant, or another Variable.

        Args:
            other (Constant | Variable | Function): The exponent.
        
        Returns:
            Function: The power of the two values.
        '''
        from function import Function
        return Function('^', [self.copy(), other.copy()])

    def __neg__(self):
        '''
        Creates a negated version of the Variable.
        
        Returns:
            Function: The negated Variable.
        '''
        from function import Function
        return Function('*', [Constant('-1'), self.copy()])
    
    def __eq__(self, other: Variable) -> bool:
        '''
        Checks if two Variables are equal.

        Args:
            other (Variable): The Variable to be compared against.

        Returns:
            bool: If the two Variables are equal.
        '''
        return isinstance(other, Variable) and self.var == other.var

    def __lt__(self, other: Variable) -> bool:
        '''
        Checks if one Variable is less than another.

        Args:
            other (Variable): The Variable to be compared against.

        Returns:
            bool: If the Variable is less than other.
        '''
        if isinstance(other, Constant):
            return False
        return not isinstance(other, Variable) or self.var < other.var