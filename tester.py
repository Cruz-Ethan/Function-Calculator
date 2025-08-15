from parser import Parser
from function import Function
from variable import Variable
from constant import Constant
import math

if __name__ == '__main__':
    # print(Parser.parse('arcsin(sinx+2)'))
    # print(Parser.parse('(arcsin(x))'))
    # print(Parser.parse('.05x^2 + .1x - 4.5'))
    # print(Parser.parse('pix^2'))
    # print(Parser.parse('arcsin(sinx + 2)'))
    # print('ß'.isalpha())
    # print(Parser.parse('cosx + isinx'))
    # print(Parser.parse('sin(x)'))
    # print(Parser.parse('(x3)(x^(-8))'))

    # my_fun: Function = Function.generate_function('(x^2)(x+3)')
    # print(my_fun.diff(times=2))
    
    '''
    fun2: Function = Function.generate_function('(2x2-7x+4)(3x2+5x+7)')
    print(fun2)
    fun2 = fun2.simplify()
    print(fun2)
    '''

    '''
    fun3: Function = Function.generate_function('x7')
    fun4: Function = Function.generate_function('y^-8')
    print(fun3 < fun4)
    '''

    x: float = 100
    fun: Function = Function.generate_function('arctanx')
    print(fun.newton_raphson(x))