from parser import Parser
from constant import Constant
from variable import Variable
from function import Function
from collections import deque

class FunctionGenerator:
    @classmethod
    def generate_function(cls, eq: str) -> Function:
        '''
        Creates a Function from an equation.

        Args:
            eq (str): The equation.
        
        Returns:
            Function: The Function that represents the equation.
        '''
        operation_stack: list[str] = deque()
        value_stack: list[Function] = deque()
        eq = Parser.parse(eq)
        index = 0

        while index < len(eq):
            if eq[index] in '1234567890πe' or (eq[index] == '-' and (index == 0 or eq[index - 1] in '(+-*/^')):
                start_index = index
                end_index = cls.__find_end_index(eq, start_index + 1 if eq[index] == '-' else start_index)
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

    @classmethod
    def __find_end_index(cls, eq: str, start_index: int) -> int:
        '''
        Finds the ending index of a number in an equation.

        Args:
            eq (str): The equation.
            start_index (int): The starting index of the number.

        Returns:
            int: The ending index of the number.
        '''
        while start_index < len(eq) and (eq[start_index] in '1234567890.pe'):
            start_index += 1
        return start_index