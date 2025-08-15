class Parser:
    @classmethod
    def parse(cls, eq: str) -> str:
        eq = cls.__remove_spaces(eq)
        eq = cls.__add_zero_to_decimals(eq)
        eq = cls.__shorten_const(eq)
        eq = cls.__shorten_func(eq)
        eq = cls.__parse_func(eq)
        eq = cls.__parse_mult_exp_shortcuts(eq)
        eq = cls.__parse_negatives(eq)
        eq = cls.__parse_order_of_operations(eq)
        eq = cls.__remove_extra_parenthesees(eq)
        return eq
    
    @classmethod
    def __remove_spaces(cls, eq: str) -> str:
        return eq.replace(' ', '')

    @classmethod
    def __add_zero_to_decimals(cls, eq: str) -> str:
        index = 0
        while index < len(eq) - 1:
            if eq[index] == '.' and (index == 0 or not cls.__is_num(eq, index - 1)):
                eq = eq[:index] + '0' + eq[index:]
            index += 1
        return eq

    @classmethod
    def __shorten_const(cls, eq: str) -> str:
        return eq.replace('pi', 'π')

    @classmethod
    def __shorten_func(cls, eq: str) -> str:
        eq = eq.replace('sqrt', 'œ')

        eq = eq.replace('arcsinh', 'å')
        eq = eq.replace('arccosh', '‰')
        eq = eq.replace('arctanh', '˝')

        eq = eq.replace('sinh', '˙')
        eq = eq.replace('cosh', '®')
        eq = eq.replace('tanh', '©')

        eq = eq.replace('arcsin', 'Í')
        eq = eq.replace('arccos', 'Ç')
        eq = eq.replace('arctan', 'ˇ')

        eq = eq.replace('sin', 'ß')
        eq = eq.replace('cos', 'ç')
        eq = eq.replace('tan', '†')

        eq = eq.replace('log', 'Ò')
        eq = eq.replace('ln', '¬')
        return eq

    @classmethod
    def __parse_func(cls, eq: str) -> str:
        index = 0
        while index < len(eq) - 1:
            if cls.__is_func(eq, index):
                eq = cls.__add_func_parenthesees(eq, index)
            index += 1
        return eq

    @classmethod
    def __parse_mult_exp_shortcuts(cls, eq: str) -> str:
        index = len(eq) - 1
        while index > 0:
            if eq[index - 1] == ')' and (cls.__is_num(eq, index) or cls.__is_const(eq, index)):
                eq = eq[:index] + '^' + eq[index:]
                eq = cls.__add_parenthesees(eq, index)
                continue
            elif eq[index] == '(' and (cls.__is_num(eq, index - 1) or cls.__is_const(eq, index - 1) or eq[index - 1] == ')' or cls.__is_var(eq, index - 1)):
                eq = eq[:index] + '*' + eq[index:]
                eq = cls.__add_parenthesees(eq, index)
                continue
            elif cls.__is_var(eq, index - 1) and (eq[index] == eq[index - 1] or cls.__is_num(eq, index) or cls.__is_const(eq, index)):
                eq = eq[:index] + '^' + eq[index:]
                eq = cls.__add_parenthesees(eq, index)
                continue
            elif (cls.__is_var(eq, index - 1) or eq[index - 1] == ')' or cls.__is_num(eq, index - 1) or cls.__is_const(eq, index - 1)) and eq[index] == '^':
                eq = cls.__add_parenthesees(eq, index)
            elif cls.__is_var(eq, index) and (cls.__is_num(eq, index - 1) or cls.__is_const(eq, index - 1) or cls.__is_var(eq, index - 1)):
                eq = eq[:index] + '*' + eq[index:]
                start_index = cls.__find_start_index(eq, index - 1)
                eq = cls.__add_parenthesees(eq, index)
                if not (cls.__is_var(eq, start_index - 1) and (eq[start_index + 1] == eq[start_index - 1] or cls.__is_num(eq, start_index + 1) or cls.__is_const(eq, start_index + 1))):
                    continue
                eq = eq[:start_index] + '^' + eq[start_index:]
                eq = cls.__add_parenthesees(eq, start_index)
            index -= 1
            #
            #
            # |
            #e*x
        return eq
    
    @classmethod
    def __parse_negatives(cls, eq: str) -> str:
        index = 0
        while index < len(eq) - 1:
            if cls.__is_negative_sign(eq, index) and not cls.__is_num(eq, index + 1):
                start_index = index + 1
                end_index = cls.__find_end_index(eq, start_index)
                eq = eq[:index] + '(' + eq[index:start_index] + '1*' + eq[start_index:end_index + 1] + ')' + eq[end_index + 1:]
                index += 1
            index += 1
        return eq

    @classmethod
    def __parse_order_of_operations(cls, eq: str) -> str:
        index = 1
        while index < len(eq) - 1:
            if eq[index] == '*' or eq[index] == '/':
                eq = cls.__add_parenthesees(eq, index)
            index += 1
        index = 1
        while index < len(eq) - 1:
            if eq[index] == '+' or (eq[index] == '-' and not cls.__is_negative_sign(eq, index)):
                eq = cls.__add_parenthesees(eq, index)
            index += 1
        return eq

    @classmethod
    def __remove_extra_parenthesees(cls, eq: str) -> str:
        curr_index = eq.find('(')
        while curr_index != -1:
            curr_end_index = cls.__find_end_index(eq, curr_index)
            start_index = curr_index + 1
            end_index = cls.__find_end_index(eq, start_index)
            while eq[curr_index] == '(' and end_index == curr_end_index - 1:
                eq = eq[:curr_index] + eq[start_index:end_index + 1] + eq[curr_end_index + 1:]
                curr_end_index = cls.__find_end_index(eq, curr_index)
                end_index = cls.__find_end_index(eq, start_index)
            curr_index = eq.find('(', curr_index + 1)
        return eq

    @classmethod
    def __add_parenthesees(cls, eq: str, index: int) -> str:
        start_index = cls.__find_start_index(eq, index - 1)
        end_index = cls.__find_end_index(eq, index + 1)
        if start_index > 0 and eq[start_index - 1] == '(' and end_index < len(eq) - 1 and eq[end_index + 1] == ')':
            return eq
        return eq[:start_index] + '(' + eq[start_index:end_index + 1] + ')' + eq[end_index + 1:]

    @classmethod
    def __add_func_parenthesees(cls, eq: str, index: int) -> str:
        start_index = index + 1
        end_index = cls.__find_end_index(eq, start_index)
        if eq[start_index] != '(' and not cls.__is_var(eq, start_index):
            eq = eq[:start_index] + '(' + eq[start_index:end_index + 1] + ')' + eq[end_index + 1:]
            end_index = cls.__find_end_index(eq, start_index)

        if index == 0 or eq[index - 1] != '(' or cls.__find_end_index(eq, index - 1) != end_index + 1:
            eq = eq[:index] + '(' + eq[index:end_index + 1] + ')' + eq[end_index + 1:]
        return eq

    @classmethod
    def __find_start_index(cls, eq: str, end_index: int) -> int:
        if cls.__is_num(eq, end_index):
            while end_index >= 0 and (cls.__is_num(eq, end_index) or eq[end_index] == '.'):
                end_index -= 1
            if end_index >= 0 and cls.__is_negative_sign(eq, end_index):
                end_index -= 1
        elif eq[end_index] == ')':
            count = 1
            end_index -= 1
            while count:
                if eq[end_index] == ')': count += 1
                elif eq[end_index] == '(': count -= 1
                end_index -= 1
        else:
            return end_index
        return end_index + 1
    
    @classmethod
    def __find_end_index(cls, eq: str, start_index: int) -> int:
        if cls.__is_negative_sign(eq, start_index):
            start_index += 1
        if cls.__is_num(eq, start_index):
            while start_index < len(eq) and (cls.__is_num(eq, start_index) or eq[start_index] == '.'):
                start_index += 1
        elif eq[start_index] == '(':
            count = 1
            start_index += 1
            while count:
                if eq[start_index] == '(': count += 1
                elif eq[start_index] == ')': count -= 1
                start_index += 1
        else:
            return start_index
        return start_index - 1
    
    @classmethod
    def __is_num(cls, eq: str, index: int) -> bool:
        return eq[index].isdigit()
    
    @classmethod
    def __is_const(cls, eq: str, index: int) -> bool:
        return eq[index] in 'πe'

    @classmethod
    def __is_var(cls, eq: str, index: int) -> bool:
        return eq[index].lower() in 'qwrtyuiopasdfghjklzxcvbnm' or eq[index] == 'E'

    @classmethod
    def __is_func(cls, eq: str, index: int) -> bool:
        return eq[index] in 'œå‰˝˙®©ÍÇˇßç†Ò¬'

    @classmethod
    def __is_negative_sign(cls, eq: str, index: int) -> bool:
        return eq[index] == '-' and (index == 0 or eq[index - 1] in '+-*/^(')

# Tests
# print(Parser.parse('arcsin(sinx+2)'))
# print(Parser.parse('(arcsin(x))'))
# print(Parser.parse('.05x^2 + .1x - 4.5'))
# print(Parser.parse('pix^2'))
# print(Parser.parse('arcsin(sinx + 2)'))
# print('ß'.isalpha())
# print(Parser.parse('cosx + isinx'))
# print(Parser.parse('sin(x)'))
# print(Parser.parse('(x3)(x^(-8))'))