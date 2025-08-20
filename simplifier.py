from constant import Constant
from variable import Variable
from function import Function

class Simplifier:
    @classmethod
    def simplify(cls, fun: Function) -> Function:
        res = fun.copy()
        while not cls.is_simplified(res):
            res = cls.__simplify_helper(res)
        cls.__reorder(res)
        return res

    @classmethod
    def is_simplified(cls, fun: Function) -> bool:
        return not isinstance(fun, Function) or fun == cls.__simplify_helper(fun)

    @classmethod
    def __simplify_helper(cls, fun: Function) -> Function:
        if not isinstance(fun, Function): return fun.copy()
        res: Function = Function(fun.operation, [cls.__simplify_helper(child_fun) for child_fun in fun.functions])

        isConstant: bool = True
        for child_fun in res.functions:
            if not isinstance(child_fun, Constant):
                isConstant = False
                break
        if isConstant:
            return Constant(res.eval(None))
        
        match res.operation:
            case '+':
                temp: list[Function] = []

                while res.functions:
                    child_fun = res.functions.pop(0)
                    if isinstance(child_fun, Function) and child_fun.operation == '+':
                        res.functions.extend(child_fun.functions)
                    elif isinstance(child_fun, Function) and child_fun.operation == '-':
                        res.functions.append(child_fun.functions[0])
                        res.functions.append(-child_fun.functions[1])
                    elif child_fun != Constant('0'):
                        temp.append(child_fun)
                res.functions = temp
                
                index = 0
                while index < len(res.functions):
                    other_index = index + 1
                    while other_index < len(res.functions):
                        if res.functions[index] == -res.functions[other_index]:
                            del res.functions[other_index]
                            del res.functions[index]
                            break
                        if cls.__are_like_terms(res.functions[index], res.functions[other_index]):
                            fun1: Function = res.functions.pop(other_index)
                            fun2: Function = res.functions.pop(index)
                            res.functions.append(cls.__combine_like_terms(fun1, fun2))

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
                res = cls.__simplify_helper(res)
            case '*':
                add_funs: list[Function] = []
                index = 0
                while index < len(res.functions):
                    child_fun = res.functions[index]
                    if child_fun == Constant('0'):
                        return Constant('0')
                    if child_fun == Constant('1'):
                        res.functions.pop(index)
                    elif isinstance(child_fun, Function) and child_fun.operation == '*':
                        res.functions.pop(index)
                        res.functions.extend(child_fun.functions)
                    elif isinstance(child_fun, Function) and child_fun.operation == '+':
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
                    res = cls.__distribute(res, cls.__multiply_functions(add_funs))
                    res = Function(res.operation, [cls.__simplify_helper(child_fun) for child_fun in res.functions])

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

                    res.functions[0] = cls.__simplify_helper(fun1)
                    res.functions[1] = cls.__simplify_helper(fun2)
                    fun1 = res.functions[0]
                    fun2 = res.functions[1]
                elif isinstance(fun1, Function) and fun1.operation == '*':
                    if fun2 in fun1.functions:
                        fun1.functions.remove(fun2)
                        return fun1.simplify_helper()
                elif isinstance(fun2, Function) and fun2.operation == '*':
                    if fun1 in fun2.functions:
                        fun2.functions.remove(fun1)
                        return cls.__simplify_helper(Function('/', [Constant('1'), cls.__simplify_helper(fun2)]))

                if isinstance(fun1, Constant) and isinstance(fun2, Constant): return Constant(res.eval(None))
                if fun1 == Constant('0'): return Constant('0')
                if fun2 == Constant('1'): return fun1
                if fun1 == fun2: return Constant('1')
                res = fun1 * (fun2 ** Constant('-1'))
                res = cls.simplify(res)
            case '^':
                if isinstance(res.functions[0], Function) and res.functions[0].operation == '^':
                    res.functions = [cls.__simplify_helper(res.functions[0].functions[0]), cls.__simplify_helper(res.functions[0].functions[1] * res.functions[1])]
                if isinstance(res.functions[0], Function) and res.functions[0].operation == '*':
                    for index in range(len(res.functions[0].functions)):
                        res.functions[0].functions[index] **= res.functions[1]
                    return res.functions[0]

                if res.functions[1] == Constant('0'): return Constant('1')
                if res.functions[1] == Constant('1'): return res.functions[0]
                if res.functions[1] == Constant('0'): return Constant('0')
                if res.functions[0] == Constant('1'): return Constant('1')
        return res    

    @classmethod
    def __reorder(cls, fun: Function) -> None:
        if not isinstance(fun, Function):
            return
        
        for child_fun in fun.functions:
            cls.__reorder(child_fun)
        if fun.operation in '*+':
            fun.functions.sort()

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
                res.append(cls.__simplify_helper(term1 * term2))
        return Function('+', res)

    @classmethod
    def __combine_like_terms(cls, fun1: Function, fun2: Function) -> Function:
        like_term: list[Function] = cls.__get_term(fun1)
        like_term.append(cls.__get_coefficient(fun1) + cls.__get_coefficient(fun2))
        return cls.__simplify_helper(Function('*', like_term))

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
