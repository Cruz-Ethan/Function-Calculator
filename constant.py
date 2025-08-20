from __future__ import annotations
import math

class Constant:
    def __init__(self, val: str | float) -> None:
        '''
        Creates a new Constant.

        Args:
            val (str | float): The value of the Constant. 'p' for pi and 'e' for Euler's number.
        '''
        self.num: float
        match val:
            case 'p':
                self.num = math.pi
            case 'e':
                self.num = math.e
            case _:
                self.num = float(val)
    
    def __str__(self) -> str:
        '''
        Converts the Constant to a readable string.

        Returns:
            A string representing the Constant.
        '''
        return str(int(self.num)) if self.num.is_integer() else str(round(self.num, 3))

    def str_helper(self) -> str:
        '''
        A helper function used to simplify Function strings.

        Returns:
            A string representing the Constant.
        '''
        return str(self)
    
    def diff(self, var: str = 'x', times: int = 1) -> Constant:
        '''
        Differentiates the Constant.

        Args:
            var (str): The differentiating variable.
            times (int): The number of times to differentiate the Constant.
        
        Returns:
            Constant: The differentiated Constant.
        '''
        return Constant('0') if times else self.copy()

    def diff_eval(self, vars: tuple[float] | float | dict) -> float:
        '''
        Evaluates the derivative of the Constant.

        Args:
            vars (tuple[float] | float | dict): The values of the variables.

        Returns:
            float: The derivative of the Constant.
        '''
        return 0.0

    def eval(self, vars: tuple[float] | float | dict) -> float:
        '''
        Evaluates the Constant.

        Args:
            vars (tuple[float] | float | dict): The values of the variables.

        Returns:
            float: The evaluation of the Constant.
        '''
        return self.num
    
    def copy(self) -> Constant:
        '''
        Creates a copy of the Constant.

        Returns:
            The copy of the Constant.
        '''
        return Constant(self.num)
    
    def __add__(self, other: Constant):
        '''
        Adds a Constant and a Function, Variable, or another Constant.

        Args:
            other (Constant | Variable | Function): The value to be added.
        
        Returns:
            Constant | Function: The sum of the two values.
        '''
        from function import Function
        
        if isinstance(other, Constant):
            return Constant(self.num + other.num)
        return Function('+', [self.copy(), other.copy()])
    
    def __sub__(self, other: Constant):
        '''
        Subtracts a Constant and a Function, Variable, or another Constant.

        Args:
            other (Constant | Variable | Function): The value to be subtracted.
        
        Returns:
            Constant | Function: The difference of the two values.
        '''
        from function import Function
        
        if isinstance(other, Constant):
            return Constant(self.num - other.num)
        return Function('-', [self.copy(), other.copy()])
    
    def __mul__(self, other: Constant):
        '''
        Multiplies a Constant and a Function, Variable, or another Constant.

        Args:
            other (Constant | Variable | Function): The value to be multiplied.
        
        Returns:
            Constant | Function: The product of the two values.
        '''
        from function import Function

        if isinstance(other, Constant):
            return Constant(self.num * other.num)
        return Function('*', [self.copy(), other.copy()])
    
    def __truediv__(self, other: Constant):
        '''
        Divides a Constant and a Function, Variable, or another Constant.

        Args:
            other (Constant | Variable | Function): The value to be divided.
        
        Returns:
            Constant | Function: The quotient of the two values.
        '''
        from function import Function
        
        if isinstance(other, Constant):
            return Constant(self.num / other.num)
        return Function('/', [self.copy(), other.copy()])
    
    def __pow__(self, other: Constant):
        '''
        Raises a Constant to the power of a Function, Variable, or another Constant.

        Args:
            other (Constant | Variable | Function): The exponent.
        
        Returns:
            Constant | Function: The power of the two values.
        '''
        from function import Function
        
        if isinstance(other, Constant):
            return Constant(self.num ** other.num)
        return Function('^', [self.copy(), other.copy()])

    def __neg__(self) -> Constant:
        '''
        Creates a negated version of the Constant.
        
        Returns:
            Constant: The negated Constant.
        '''
        return Constant(-self.num)
    
    def __eq__(self, other: Constant) -> bool:
        '''
        Checks if two Constants are equal.

        Args:
            other (Constant): The Constant to be compared against.

        Returns:
            bool: If the two Constants are equal.
        '''
        return isinstance(other, Constant) and self.num == other.num
    
    def __lt__(self, other: Constant) -> bool:
        '''
        Checks if one Constant is less than another.

        Args:
            other (Constant): The Constant to be compared against.

        Returns:
            bool: If the Constant is less than other.
        '''
        return not isinstance(other, Constant) or self.num < other.num