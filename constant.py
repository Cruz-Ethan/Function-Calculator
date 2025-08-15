from __future__ import annotations
import math

class Constant:
    def __init__(self, val: str | float) -> None:
        self.num: float
        match val:
            case 'p':
                self.num = math.pi
            case 'e':
                self.num = math.e
            case _:
                self.num = float(val)
    
    def __str__(self) -> str:
        return str(int(self.num)) if self.num.is_integer() else str(round(self.num, 3))

    def str_helper(self) -> str:
        return str(self)
    
    def diff(self, var: str = 'x', times: int = 1):
        return Constant('0') if times else self.copy()

    def diff_eval(self, vars: tuple[float] | float | dict) -> float:
        return 0.0

    def eval(self, vars: tuple[float] | float | dict) -> float:
        return self.num
    
    def copy(self) -> Constant:
        return Constant(self.num)
    
    def __add__(self, other: Constant):
        from function import Function
        
        if isinstance(other, Constant):
            return Constant(self.num + other.num)
        return Function('+', [self.copy(), other.copy()])
    
    def __sub__(self, other: Constant):
        from function import Function
        
        if isinstance(other, Constant):
            return Constant(self.num - other.num)
        return Function('-', [self.copy(), other.copy()])
    
    def __mul__(self, other: Constant):
        from function import Function

        if isinstance(other, Constant):
            return Constant(self.num * other.num)
        return Function('*', [self.copy(), other.copy()])
    
    def __truediv__(self, other: Constant):
        from function import Function
        
        if isinstance(other, Constant):
            return Constant(self.num / other.num)
        return Function('/', [self.copy(), other.copy()])
    
    def __pow__(self, other: Constant):
        from function import Function
        
        if isinstance(other, Constant):
            return Constant(self.num ** other.num)
        return Function('^', [self.copy(), other.copy()])

    def __neg__(self) -> Constant:
        return Constant(-self.num)
    
    def simplify(self) -> Constant:
        return self.copy()

    def simplify_helper(self) -> Constant:
        return self.copy()
    
    def reorder(self) -> None:
        pass

    def is_simplified(self) -> bool:
        return True

    def __eq__(self, other: Constant) -> bool:
        return isinstance(other, Constant) and self.num == other.num
    
    def __lt__(self, other: Constant) -> bool:
        return not isinstance(other, Constant) or self.num < other.num
    
    def __hash__(self) -> int:
        return hash(self.num)