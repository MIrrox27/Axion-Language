# author https://github.com/MIrrox27/Axion-Language
# AxionParser.py


from axion.AxionASTNodes import *
# from axion.AxionLexer import AxionLexer
from  axion.AxionTokens import AxionTokenType



class AxionParser:

    def __init__(self, lexer, debug=False):
        import builtins
        if not getattr(builtins, '__axion_verified__', False):
            raise RuntimeError("Unauthorized copy of Axion interpreter detected.")

        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.debug = debug
        self.loop_for = False
        self.ERROR = Error("AxionParser")

       # self.builtin_functions = { AxionTokenType.PRINT: "print", AxionTokenType.INPUT: "input" }



            # ----ФУНКЦИИ КЛАССА-----

    def log(self, message):
        if self.debug:
            print(f'[Parser DEBUG]: {message}, line: {self.lexer.line}, position: {self.lexer.position}, current char: "{self.lexer.current_char}"')


    def error(self, message, func):
        self.loop_for = False
        self.ERROR.error(message=f'{message}, line: {self.lexer.line}, position: {self.lexer.position}, current char: "{self.lexer.current_char}"', func=func)

    def eat(self, token_type): # Проверяет, что текущий токен имеет ожидаемый тип
        if self.current_token.type == token_type:
            self.log(f'[eat] received: [{token_type}]')
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Pending {token_type}, received {self.current_token.type}", 'eat') # self.current_token.type - тип токена который мы получили,
            # token_type - токен, который нам нужен



            # -----ВЫРАЖЕНИЯ-----

    def parse_primary(self):  # Парсит первичные выражения. Возвращает узел AST
        token = self.current_token
        #print(f'[parse_primary]: token - {token}')
        # типы данных
        if token.type in (AxionTokenType.INTEGER, AxionTokenType.FLOAT): #
            self.eat(token.type)
            return Literal(token.value)

        elif token.type == AxionTokenType.STRING:
            self.eat(token.type)
            return Literal(token.value)

        elif token.type == AxionTokenType.NONE:
            self.eat(token.type)
            return Literal(None)

        elif token.type == AxionTokenType.BOOL:
            self.eat(token.type)
            return  Literal(token.value)

        elif token.type == AxionTokenType.BLOCK:
            return self.parse_python_block() # здесь сделаю проверки для других языков программирования

        elif token.type == AxionTokenType.LBRACKET:
            return self.parse_list()


        elif token.type == AxionTokenType.IDENTIFIER:
            self.eat(token.type)
            node = Identifier(token.value)

            while self.current_token.type == AxionTokenType.LBRACKET: # Для цепочек доступа, например matrix[0][1]
                self.eat(AxionTokenType.LBRACKET)
                index_expr = self.parse_expression()
                self.eat(AxionTokenType.RBRACKET)
                node = IndexAccess(node, index_expr)



            if self.current_token.type == AxionTokenType.INCREMENT:
                self.eat(AxionTokenType.INCREMENT)
                return UnaryOp(operator=AxionTokenType.POST_INCREMENT, expr=node)

            elif self.current_token.type == AxionTokenType.LPAREN:  # <--- ДОБАВИТЬ ЭТУ СТРОКУ
                return self.parse_call(node)


            elif self.current_token.type == AxionTokenType.DECREMENT:
                self.eat(AxionTokenType.DECREMENT)
                return UnaryOp(operator=AxionTokenType.POST_DECREMENT, expr=node)


            elif self.current_token.type == AxionTokenType.DOT:
                return self.parse_member_access(node)


            return node


        # символы (скобки)
        elif token.type == AxionTokenType.LPAREN:
            self.eat(AxionTokenType.LPAREN) #
            node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            self.eat(AxionTokenType.RPAREN) #
            return node

        elif token.type == AxionTokenType.LBRACE:
            self.eat(AxionTokenType.LBRACE) #
            node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            self.eat(AxionTokenType.RBRACE) #
            return node


        else:
            self.error(f"Received {token.type}", func='parse_primary')



    def parse_unary(self): # обработка унарных операторов, пока только not, потом добавлю ++ и --
        token = self.current_token

        if token.type in (AxionTokenType.NOT,
                        AxionTokenType.INCREMENT,
                        AxionTokenType.DECREMENT,
                        AxionTokenType.MINUS,
                        AxionTokenType.PLUS ):

            self.eat(token.type)
            expr = self.parse_unary()
            return UnaryOp(operator=token.type, expr=expr)

        return self.parse_primary()



    def parse_power(self): # парсит выражения с высшим приоритетом (допустим возведение в степень)
        node = self.parse_unary()

        while self.current_token.type == AxionTokenType.POWER:
            operator_token = self.current_token
            self.eat(AxionTokenType.POWER)
            right = self.parse_power()

            node = BinaryOp(
                left=node,
                operator=operator_token.type,
                right=right
            )
        return node



    def parse_mul_div_mod(self):
        node = self.parse_power()
         #
        while self.current_token.type in (AxionTokenType.MULTIPLY, AxionTokenType.DIVIDE, AxionTokenType.MOD):
            operator_token = self.current_token
            self.eat(operator_token.type)

            right = self.parse_power()

            node = BinaryOp(
                left=node,
                operator=operator_token.type,
                right=right
            )
        return node



    def parse_add_sub(self): # парсит сложение и вычитание
        self.log(f"Start parse_add_sub(), token: {self.current_token}")

        node = self.parse_mul_div_mod()

        self.log(f"Parse 1st parse_term(), node: {node}, token: {self.current_token}")

        while self.current_token.type in (AxionTokenType.PLUS, AxionTokenType.MINUS):
            operator_token = self.current_token
            self.log(f"Operator {operator_token.type}, parse further")

            self.eat(operator_token.type)
            right = self.parse_mul_div_mod()

            self.log(f"Create BinaryOp: {node} {operator_token.type} {right}")
            node = BinaryOp(
                left=node,
                operator=operator_token.type,
                right=right
            )

        self.log(f"End parse_expression(), return: {node}")
        return node



    def parse_comparison(self): # парсинг выражений равенства
        node = self.parse_add_sub()

        comparison_operators = (
            AxionTokenType.GREATER_EQUAL, # >=
            AxionTokenType.LESS_EQUAL, # <=

            AxionTokenType.EQUALS, # ==
            AxionTokenType.NOT_EQUALS, # !=
            AxionTokenType.LESS, # <
            AxionTokenType.GREATER # >
        )
        while self.current_token.type in comparison_operators:
            operator_token = self.current_token
            self.eat(operator_token.type)

            right = self.parse_add_sub()

            node = BinaryOp(
                left=node,
                operator=operator_token.type,
                right=right
            )
        return node



    def parse_logical_and(self): # обработка логического and
        node = self.parse_comparison()
        while self.current_token.type == AxionTokenType.AND:
            op = self.current_token.type
            self.eat(op)
            right = self.parse_comparison()

            node = BinaryOp(left=node, operator=op, right=right)
        return node



    def parse_logical_or(self): # обработка логического or
        node = self.parse_logical_and()
        while self.current_token.type == AxionTokenType.OR:
            op = self.current_token.type
            self.eat(op)
            right = self.parse_logical_and()

            node = BinaryOp(left=node, operator=op, right=right)
        return node



    def parse_assignment(self): # парсинг присвоения
        func = 'parse_assignment'
        node = self.parse_logical_or()

        if self.current_token.type == AxionTokenType.ASSIGN:
            if not isinstance(node, Identifier): # Потом добавим обработку присваивания массивам, спискам словарям и тп.
                self.error("Left side of assignment must be a variable", func)

            operator_token = self.current_token
            self.eat(AxionTokenType.ASSIGN)

            right = self.parse_assignment()
            node = BinaryOp(left=node, operator=operator_token.type, right=right)
        return node



    def parse_expression(self): # главный модуль, сделан для начала парсинга
        return self.parse_assignment()


            # ----- БЛОК -----

    def parse_block(self):
        func = 'parse_block'
        self.eat(AxionTokenType.LBRACE)

        statements = []

        while self.current_token.type != AxionTokenType.RBRACE:
            if self.current_token == AxionTokenType.EOF:
                self.error("Block not closed, pending '}'", func)

            stmt = self.parse_statement()
            statements.append(stmt)

        self.eat(AxionTokenType.RBRACE)
        return Block(statements=statements)



    def parse_python_block(self):
        func = 'parse_python_block'
        self.eat(AxionTokenType.BLOCK)

        if self.current_token.type != AxionTokenType.PYTHON:
            self.error("Expected language name after 'block'", func)
        self.eat(AxionTokenType.PYTHON)


        outputs = [] # Парсим выходные переменные
        if self.current_token.type == AxionTokenType.ARROW:
            self.eat(AxionTokenType.ARROW)
            while True:
                if self.current_token.type != AxionTokenType.IDENTIFIER:
                    self.error("Expected variable name after '->'", func)
                var_name = self.current_token.value
                self.eat(AxionTokenType.IDENTIFIER)
                outputs.append(var_name)
                if self.current_token.type == AxionTokenType.COMMA:
                    self.eat(AxionTokenType.COMMA)
                    continue
                else:
                    break

        if self.current_token.type != AxionTokenType.CODE_BLOCK:
            self.error("Expected '{$' to start Python code block", func)

        code = self.current_token.value
        self.eat(AxionTokenType.CODE_BLOCK)

        if self.current_token.type == AxionTokenType.SEMICOLON:
            self.eat(AxionTokenType.SEMICOLON)

        inputs = []
        return PythonBlock(code, inputs, outputs)




            # -----ПЕРЕМЕННЫЕ-----

    def parse_var_declaration(self, loop:bool = False): # парсит объявление переменной
        func = 'parse_var_declaration'
        keyword_token = self.current_token
        self.eat(keyword_token.type)

        if self.current_token.type != AxionTokenType.IDENTIFIER:    # получаем имя переменной
            self.error(f'After {keyword_token.type} pending main value', func=func)

        name = self.current_token.value
        self.eat(AxionTokenType.IDENTIFIER)

        value = None
        if self.current_token.type == AxionTokenType.ASSIGN: # проверяем наличие присваивания значения, если есть то парсим его
            self.eat(AxionTokenType.ASSIGN)
            value = self.parse_expression()

        if keyword_token.type == AxionTokenType.VAL and value is None:
            self.error(f"Const '{name}' must have a main value", func=func)

        if self.current_token.type == AxionTokenType.SEMICOLON and not loop:
            self.eat(AxionTokenType.SEMICOLON)

        return  VarDeclaration(keyword_token.type, name=name, value=value)



            # ----- КОЛЛЕКЦИИ -----

    def parse_list(self):
        self.eat(AxionTokenType.LBRACKET)
        elements = []

        if self.current_token.type != AxionTokenType.RBRACKET:

            while True:
                elem = self.parse_expression()
                elements.append(elem)

                if self.current_token.type == AxionTokenType.COMMA:
                    self.eat(AxionTokenType.COMMA)
                    continue

                elif self.current_token.type == AxionTokenType.RBRACKET:
                    break

                else:
                    self.error("Expected ',' or ']' in list", 'parse_list')

        self.eat(AxionTokenType.RBRACKET)
        return ListNode(elements)






            # ----ПРОВЕРКИ-----

    def parse_if_statement(self): # парсинг if/elif/else
        self.eat(AxionTokenType.IF) # съедаем if

        if self.current_token.type == AxionTokenType.LPAREN: # если есть скобки парсим выражение внутри них
            self.eat(AxionTokenType.LPAREN)
            condition = self.parse_expression()
            self.eat(AxionTokenType.RPAREN)
        else:
            condition = self.parse_expression()

        than_branch = self.parse_block()

        elif_branches = []
        while self.current_token.type == AxionTokenType.ELIF:
            self.eat(AxionTokenType.ELIF)

            if self.current_token.type == AxionTokenType.LPAREN:
                self.eat(AxionTokenType.LPAREN)
                elif_condition = self.parse_expression()
                self.eat(AxionTokenType.RPAREN)
            else:
                elif_condition = self.parse_expression()

            elif_block = self.parse_block()
            elif_branches.append(ElifClause(elif_condition, elif_block))

        else_branch = None
        if self.current_token.type == AxionTokenType.ELSE:
            self.eat(AxionTokenType.ELSE)
            else_branch = self.parse_block()

        return IFStmt(
            condition=condition,
            than_branch=than_branch,
            elif_branches=elif_branches,
            else_branch=else_branch
        )



            # -----ЦИКЛЫ-----

    def parse_while_statement(self):
        func = 'parse_while_statement'
        self.eat(AxionTokenType.WHILE)

        if self.current_token.type == AxionTokenType.LPAREN:
            self.eat(AxionTokenType.LPAREN)
            condition = self.parse_expression()
            self.eat(AxionTokenType.RPAREN)
        else:
            self.error(f'where is "(" ?', func)

        body = self.parse_block()
        return WhileStmt(condition=condition, body=body)



    def parse_do_statement(self):
        func = 'parse_do_statement'
        self.eat(AxionTokenType.DO)

        if self.current_token.type == AxionTokenType.LPAREN:
            self.eat(AxionTokenType.LPAREN)
            condition = self.parse_expression()
            self.eat(AxionTokenType.RPAREN)
        else:
            self.error(f'where is "(" ?', func)

        body = self.parse_block()
        return DoStmt(condition=condition, body=body)



    def parse_for_statement(self):
        func = 'parse_for_statement'
        self.eat(AxionTokenType.FOR)
        if self.current_token.type == AxionTokenType.LPAREN:
            self.loop_for = True

            self.eat(AxionTokenType.LPAREN) # тк у нас все условия цикла находятся в скобках

            # До первого ";"
            if self.current_token.type == AxionTokenType.SEMICOLON:
                initializer = None
            elif self.current_token.type == AxionTokenType.VAR:
                initializer = self.parse_var_declaration(loop=True)
            elif self.current_token.type == AxionTokenType.VAL:
                return self.error("you can't use constants in loop", func)
            else:
                initializer = self.parse_expression()
            self.eat(AxionTokenType.SEMICOLON)

                # После первого ";", до второго ";"
            if self.current_token.type == AxionTokenType.SEMICOLON:
                condition = None
            else:
                condition = self.parse_expression()
            self.eat(AxionTokenType.SEMICOLON)


                #
            if self.current_token.type == AxionTokenType.RPAREN:
                increment = None
            else:
                increment = self.parse_expression()
            self.eat(AxionTokenType.RPAREN)


            body  = self.parse_block()
            self.loop_for = False
            return ForStmt(initializer=initializer, condition=condition, increment=increment, body=body)

        else:
            return self.error("Where is '(' after 'for'?", func)



    def parse_foreach_statement(self):
        func = 'parse_foreach_statement'
        self.eat(AxionTokenType.FOREACH)

        if self.current_token.type == AxionTokenType.LPAREN:
            self.eat(AxionTokenType.LPAREN)

            if self.current_token.type == AxionTokenType.VAR:
                self.eat(AxionTokenType.VAR)

            elif self.current_token.type == AxionTokenType.VAL:
                self.error("you can't use 'val' in this loop", func)


            if self.current_token.type != AxionTokenType.IDENTIFIER:
                self.error("After the loop a variable is expected", func)

            var_name = self.current_token.value
            self.eat(AxionTokenType.IDENTIFIER)

            if self.current_token.type != AxionTokenType.IN:
                self.error("After the variable expected 'in'", func)
            self.eat(AxionTokenType.IN)

        else:
            self.error(f'where is "(" ?', func)

        iterable = self.parse_expression()
        self.eat(AxionTokenType.RPAREN)
        body = self.parse_block()

        return ForeachStmt(Identifier(var_name), iterable=iterable, body=body)



            # -----ФУНКЦИИ-----

    def parse_call(self, callee):  # парсинг вызова функций
        self.eat(AxionTokenType.LPAREN)

        arguments = []

        if self.current_token.type != AxionTokenType.RPAREN:
            while True:
                arg = self.parse_expression()  # парсим выражение (аргумент)
                arguments.append(arg)

                if self.current_token.type == AxionTokenType.COMMA:  # если запятая (после аргумента), то продолжаем
                    self.eat(AxionTokenType.COMMA)
                    continue

                elif self.current_token.type == AxionTokenType.RPAREN:
                    break

                else:
                    self.error(message="Expected ',' or ')' after argument", func='parse_call')

        self.eat(AxionTokenType.RPAREN)
        return CallExpr(callee, arguments)



            # -----МОДУЛИ И ИХ ИМПОРТЫ-----

    def parse_import_statement(self): #
        self.eat(AxionTokenType.IMPORT)

        if self.current_token.type != AxionTokenType.IDENTIFIER:
            self.error(f"Expected module name '{self.current_token.type}' after 'import'", func='parse_import_statement')

        module_name = self.current_token.value
        self.eat(AxionTokenType.IDENTIFIER)

        if self.current_token.type == AxionTokenType.SEMICOLON:
            self.eat(AxionTokenType.SEMICOLON)

        return ImportStmt(module_name)



    def parse_member_access(self, obj): # Парсит доступ к члену объекта
        self.eat(AxionTokenType.DOT)

        if self.current_token.type != AxionTokenType.IDENTIFIER:
            self.error("Expected member name after '.'", func="parse_member_access")

        member_name = self.current_token.value
        self.eat(AxionTokenType.IDENTIFIER)

        node = MemberAccess(obj, member_name)
        if self.current_token.type == AxionTokenType.LPAREN:
            return self.parse_call(node)

        return node



            # -----ФУНКЦИИ-----

    def parse_fun_declaration(self): # парсинг функции
        func = "parse_fun_declaration"

        self.eat(AxionTokenType.FUN)

        if self.current_token.type != AxionTokenType.IDENTIFIER:
            self.error("Expected function name after 'fun'", func)

        name = self.current_token.value
        self.eat(AxionTokenType.IDENTIFIER)

        if self.current_token.type != AxionTokenType.LPAREN:
            self.error("Expected '(' after function name", func)

        self.eat(AxionTokenType.LPAREN)

        parameters = []
        if self.current_token.type != AxionTokenType.RPAREN:
            while True:
                if self.current_token.type != AxionTokenType.IDENTIFIER:
                    self.error("Expected parameter name", func)

                param_name = self.current_token.value
                self.eat(AxionTokenType.IDENTIFIER)
                parameters.append(param_name)

                if self.current_token.type == AxionTokenType.COMMA:
                    self.eat(AxionTokenType.COMMA)
                    continue

                elif self.current_token.type == AxionTokenType.RPAREN:
                    break

                else:
                    self.error("Expected ',' or ')' after parameter", func)


        self.eat(AxionTokenType.RPAREN)
        body = self.parse_block()
        return FunDeclaration(name=name, parameters=parameters, body=body)


    def parse_return_statement(self): # парсинг return
        self.eat(AxionTokenType.RETURN)

        value = None

        if self.current_token.type != AxionTokenType.SEMICOLON:
            value = self.parse_expression()

        if self.current_token.type == AxionTokenType.SEMICOLON: # точка с запятой обязательна
            self.eat(AxionTokenType.SEMICOLON)
        else:
            self.error("Expected ';' after return statement", 'parse_return_statement')

        return ReturnStmt(value=value)




    def parse_statement(self):
        token = self.current_token


        if token.type == AxionTokenType.SEMICOLON:
            self.eat(AxionTokenType.SEMICOLON)
            return EmtpyStmt

        elif token.type == AxionTokenType.EOF:
            return EmtpyStmt

        elif token.type == AxionTokenType.IMPORT:
            return self.parse_import_statement()

        elif token.type == AxionTokenType.LBRACE:
            return self.parse_block() # функция, которая будет парсить блоки кода, у нас они находятся в {}

        elif token.type in (AxionTokenType.VAL, AxionTokenType.VAR):
            return self.parse_var_declaration()

        elif token.type == AxionTokenType.IF:
            return self.parse_if_statement()

        elif token.type == AxionTokenType.WHILE:
            return self.parse_while_statement()

        elif token.type == AxionTokenType.FOR:
            return self.parse_for_statement()

        elif token.type == AxionTokenType.FOREACH:
            return self.parse_foreach_statement()

        elif token.type == AxionTokenType.DO:
            return self.parse_do_statement()

        elif token.type == AxionTokenType.FUN:
            return self.parse_fun_declaration()

        elif token.type == AxionTokenType.RETURN:
            return self.parse_return_statement()

        # тут будут другие проверки действий
        else:
            expr = self.parse_expression()

            if self.current_token.type == AxionTokenType.SEMICOLON:
                self.eat(AxionTokenType.SEMICOLON)
            return ExpressionStmt(expr)

