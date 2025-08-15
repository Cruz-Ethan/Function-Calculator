class Parser:
    @classmethod
    def parse(cls, eq: str) -> str:
        '''
        Adds parenthesees to an equation that makes it easy for a computer to read.

        Args:
            eq (str): The equation.

        Returns:
            str: The new equation.
        '''
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
        '''
        Removes any spaces from an equation if necessary.

        Args:
            eq (str): The equation.

        Returns:
            str: The new equation.
        '''
        return eq.replace(' ', '')

    @classmethod
    def __add_zero_to_decimals(cls, eq: str) -> str:
        '''
        Adds an 0s before decimals in an equation if necessary. \n
        .75 -> 0.75

        Args:
            eq (str): The equation.

        Returns:
            str: The new equation.
        '''
        index = 0
        while index < len(eq) - 1:
            if eq[index] == '.' and (index == 0 or not cls.__is_num(eq, index - 1)):
                eq = eq[:index] + '0' + eq[index:]
            index += 1
        return eq

    @classmethod
    def __shorten_const(cls, eq: str) -> str:
        '''
        Changes any mathematical constants in an equation to something easier for the computer to read.

        Args:
            eq (str): The equation.

        Returns:
            str: The new equation.
        '''
        return eq.replace('pi', 'π')

    @classmethod
    def __shorten_func(cls, eq: str) -> str:
        '''
        Changes conventional function notation in an equation to something easier for the computer to read.

        Args:
            eq (str): The equation.

        Returns:
            str: The new equation.
        '''
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
        '''
        Adds parenthesees to any functions in an equation if necessary.

        Args:
            eq (str): The equation.

        Returns:
            str: The new equation.
        '''
        index = 0
        while index < len(eq) - 1:
            if cls.__is_func(eq, index):
                eq = cls.__add_func_parenthesees(eq, index)
            index += 1
        return eq

    @classmethod
    def __parse_mult_exp_shortcuts(cls, eq: str) -> str:
        '''
        Parses shortcuts involving multiplication and exponentiation in an equation. \n
        2x -> 2*x \n
        x2 -> x^2 \n
        (x+3)(x+2) -> (x+3)*(x+2)

        Args:
            eq (str): The equation.

        Returns:
            str: The new equation.
        '''
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
        return eq
    
    @classmethod
    def __parse_negatives(cls, eq: str) -> str:
        '''
        Changes negative signs in an equation not attached to numbers to multiplication by -1.

        Args:
            eq (str): The equation.

        Returns:
            str: The new equation.
        '''
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
        '''
        Adds parenthesees to an equation to represent PEMDAS.

        Args:
            eq (str): The equation.

        Returns:
            str: The new equation.
        '''
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
        '''
        Removes any unnecessary parenthesees from an equation that can cause problems.

        Args:
            eq (str): The equation.

        Returns:
            str: The new equation.
        '''
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
        '''
        Adds parenthesees to an equation around an operation if necessary.

        Args:
            eq (str): The equation.
            index (int): The index of the operation.

        Returns:
            str: The new equation.
        '''
        start_index = cls.__find_start_index(eq, index - 1)
        end_index = cls.__find_end_index(eq, index + 1)
        if start_index > 0 and eq[start_index - 1] == '(' and end_index < len(eq) - 1 and eq[end_index + 1] == ')':
            return eq
        return eq[:start_index] + '(' + eq[start_index:end_index + 1] + ')' + eq[end_index + 1:]

    @classmethod
    def __add_func_parenthesees(cls, eq: str, index: int) -> str:
        '''
        Adds parenthesees to a function if necessary.

        Args:
            eq (str): The equation.
            index (int): The index of the function.

        Returns:
            str: The new equation.
        '''
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
        '''
        Finds the starting index of a number or parenthesees in an equation.

        Args:
            eq (str): The equation.
            end_index (int): The ending index of the number or parenthesees.

        Returns:
            int: The starting index of the number or parenthesees.
        '''
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
        '''
        Finds the ending index of a number or parenthesees in an equation.

        Args:
            eq (str): The equation.
            start_index (int): The starting index of the number or parenthesees.

        Returns:
            int: The ending index of the number or parenthesees.
        '''
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
        '''
        Determines if a specified character is a digit within the context of an equation.

        Args:
            eq (str): The equation.
            index (int): The index of the specified character in the equation.

        Returns:
            bool: If the specified character is a digit.
        '''
        return eq[index].isdigit()
    
    @classmethod
    def __is_const(cls, eq: str, index: int) -> bool:
        '''
        Determines if a specified character is a mathematical constant within the context of an equation.

        Args:
            eq (str): The equation.
            index (int): The index of the specified character in the equation.

        Returns:
            bool: If the specified character is a mathematical constant.
        '''
        return eq[index] in 'πe'

    @classmethod
    def __is_var(cls, eq: str, index: int) -> bool:
        '''
        Determines if a specified character is a variable within the context of an equation.

        Args:
            eq (str): The equation.
            index (int): The index of the specified character in the equation.

        Returns:
            bool: If the specified character is a variable.
        '''
        return eq[index].lower() in 'qwrtyuiopasdfghjklzxcvbnm' or eq[index] == 'E'

    @classmethod
    def __is_func(cls, eq: str, index: int) -> bool:
        '''
        Determines if a specified character is a function within the context of an equation.

        Args:
            eq (str): The equation.
            index (int): The index of the specified character in the equation.

        Returns:
            bool: If the specified character is a function.
        '''
        return eq[index] in 'œå‰˝˙®©ÍÇˇßç†Ò¬'

    @classmethod
    def __is_negative_sign(cls, eq: str, index: int) -> bool:
        '''
        Determines if a specified character is a negative sign within the context of an equation.

        Args:
            eq (str): The equation.
            index (int): The index of the specified character in the equation.

        Returns:
            bool: If the specified character is a negative sign.
        '''
        return eq[index] == '-' and (index == 0 or eq[index - 1] in '+-*/^(')