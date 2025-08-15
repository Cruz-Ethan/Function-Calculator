from parser import Parser
import unittest

class TestParser(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(Parser.parse('x(x+1)'), '(x*(x+1))')
        self.assertEqual(Parser.parse('3x3-4x2+x+9'), '((((3*(x^3))-(4*(x^2)))+x)+9)')
        self.assertEqual(Parser.parse('3x3-4(x2+x+9)'), '((3*(x^3))-(4*(((x^2)+x)+9)))')
        self.assertEqual(Parser.parse('3x3-4(x2+x+9)39'), '((3*(x^3))-(4*((((x^2)+x)+9)^39)))')
        self.assertEqual(Parser.parse('((3*(x^3))-(4*((((x^2)+x)+9)^39)))'), '((3*(x^3))-(4*((((x^2)+x)+9)^39)))')
        self.assertEqual(Parser.parse('x3+x2-9'), '(((x^3)+(x^2))-9)')
        self.assertEqual(Parser.parse('x+41x23-x'), '((x+(41*(x^23)))-x)')
        self.assertEqual(Parser.parse('xyx+1'), '((x*(y*x))+1)')
        self.assertEqual(Parser.parse('x3x+1'), '((x^(3*x))+1)')
        self.assertEqual(Parser.parse('(2x+3)(4x+1)'), '(((2*x)+3)*((4*x)+1))')
        self.assertEqual(Parser.parse('(x3x+1)9'), '(((x^(3*x))+1)^9)')
        self.assertEqual(Parser.parse('x/3x'), '(x/(3*x))')
        self.assertEqual(Parser.parse('x/3x-1'), '((x/(3*x))-1)')
        self.assertEqual(Parser.parse('x/(3x+1)'), '(x/((3*x)+1))')

        self.assertEqual(Parser.parse('3tanx'), '(3*(†x))')
        self.assertEqual(Parser.parse('(sinx)^2 + cos(x^2)'), '(((ßx)^2)+(ç(x^2)))')
        self.assertEqual(Parser.parse('arcsin(sinx + 2)'), '(Í((ßx)+2))')
        self.assertEqual(Parser.parse('arctan(sin(x + 9))'), '(ˇ(ß(x+9)))')
        self.assertEqual(Parser.parse('arccosx arcsinx'), '((Çx)*(Íx))')
        self.assertEqual(Parser.parse('.05x^2 + sqrt(.1x) - 4.5'), '(((0.05*(x^2))+(œ(0.1*x)))-4.5)')

        self.assertEqual(Parser.parse('.05x^2 + .1x - 4.5'), '(((0.05*(x^2))+(0.1*x))-4.5)')
        self.assertEqual(Parser.parse('3.9tan.5'), '(3.9*(†0.5))')
        self.assertEqual(Parser.parse('0.3tan(.5x)'), '(0.3*(†(0.5*x)))')
        self.assertEqual(Parser.parse('.93tan(.5x)'), '(0.93*(†(0.5*x)))')

        self.assertEqual(Parser.parse('3x3-4(x2+x+9)pi'), '((3*(x^3))-(4*((((x^2)+x)+9)^π)))')
        self.assertEqual(Parser.parse('(2x+e)(pix+1)'), '(((2*x)+e)*((π*x)+1))')
        self.assertEqual(Parser.parse('sin(pix)^2 + cos(πx^2)'), '(((ß(π*x))^2)+(ç(π*(x^2))))')
        self.assertEqual(Parser.parse('e^tan(.5pix)'), '(e^(†(0.5*(π*x))))')

        self.assertEqual(Parser.parse('-tanx'), '(-1*(†x))')
        self.assertEqual(Parser.parse('-3x'), '(-3*x)')
        self.assertEqual(Parser.parse('-x'), '(-1*x)')
        self.assertEqual(Parser.parse('-e^x'), '(-1*(e^x))')
        self.assertEqual(Parser.parse('e^-x'), '(e^(-1*x))')
        self.assertEqual(Parser.parse('-e^-x'), '(-1*(e^(-1*x)))')
        self.assertEqual(Parser.parse('(-y-sqrt(y^2-4xz))/2x'), '(((-1*y)-(œ((y^2)-(4*(x*z)))))/(2*x))')

if __name__ == '__main__':
    unittest.main()