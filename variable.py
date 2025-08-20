from __future__ import annotations
from constant import Constant

class Variable:
    def __init__(self, var: str) -> None:
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
        return self.var

    def str_helper(self) -> str:
        return self.var

    def diff(self, var: str = 'x', times: int = 1) -> Constant | Variable:
        if times == 0: return self.copy()
        return Constant('1').diff(times - 1) if self.var == var else Variable(f'(d{self.var}/d{var})').diff(times - 1)

    def diff_eval(self, vars: tuple[float] | float | dict) -> float:
        return 1.0

    def eval(self, vars: tuple[float] | float | dict) -> float:
        if isinstance(vars, dict): return vars[self.var]
        return vars if isinstance(vars, float | int) else vars[self.index]
    
    def copy(self) -> Variable:
        return Variable(self.var)
    
    def __add__(self, other):
        from function import Function
        return Function('+', [self.copy(), other.copy()])
    
    def __sub__(self, other):
        from function import Function
        return Function('-', [self.copy(), other.copy()])
    
    def __mul__(self, other):
        from function import Function
        return Function('*', [self.copy(), other.copy()])
    
    def __truediv__(self, other):
        from function import Function
        return Function('/', [self.copy(), other.copy()])
    
    def __pow__(self, other):
        from function import Function
        return Function('^', [self.copy(), other.copy()])

    def __neg__(self):
        from function import Function
        return Function('*', [Constant('-1'), self.copy()])
    
    def __eq__(self, other: Variable) -> bool:
        return isinstance(other, Variable) and self.var == other.var

    def __lt__(self, other: Variable) -> bool:
        if isinstance(other, Constant):
            return False
        return not isinstance(other, Variable) or self.var < other.var