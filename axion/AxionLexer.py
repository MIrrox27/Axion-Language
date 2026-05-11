# author https://github.com/MIrrox27/Axion-Language
# AxionLexer.py

from axion.AxionTokens import *


class AxionLexer:
    def __init__(self, text: str):
        import builtins
        if not getattr(builtins, '__axion_verified__', False):
            raise RuntimeError("Unauthorized copy of Axion interpreter detected.")

        self.text = text  # сам код который мы передаем в наш интерпритатор
        self.position = 0  # позиция "курсора" в тексте порядковый номер символа
        self.line = 1  # линия (строка в которой мы находимся) (по типу координаты Y)
        self.current_char = self.text[
            0] if self.text else None  # символ, который мы сейчас обрабатываем. Т. е если символ text не равен None то мы присваиваем self.current_char значение этого символа, иначе self.current_char = None


        self.num_of_code_blocks = 0
        self.code_blocks = []

        self.KEYWORDS = {  # ключевые слова
            'import': AxionTokenType.IMPORT,

            'if': AxionTokenType.IF,
            'elif': AxionTokenType.ELIF,
            'else': AxionTokenType.ELSE,

            'while': AxionTokenType.WHILE,
            'do': AxionTokenType.DO,
            'for': AxionTokenType.FOR,
            'foreach': AxionTokenType.FOREACH,

            'var': AxionTokenType.VAR,
            'val': AxionTokenType.VAL,

            'True': AxionTokenType.BOOL,
            'False': AxionTokenType.BOOL,

            'class': AxionTokenType.CLASS,
            'enum': AxionTokenType.ENUM,

            #'script': AxionTokenType.SCRIPT,
            #'config': AxionTokenType.CONFIG,

            'block': AxionTokenType.BLOCK,
            'python': AxionTokenType.PYTHON,

            'is': AxionTokenType.IS,
            'in': AxionTokenType.IN,
            'and': AxionTokenType.AND,
            'or': AxionTokenType.OR,
            'None': AxionTokenType.NONE,
            'not': AxionTokenType.NOT,

            'fun': AxionTokenType.FUN,
            'return': AxionTokenType.RETURN
        }


    def error(self, message: str):
        raise Exception(f'[Lexer Error] in {self.line}: {message}')

    def advance(self):  # функция, которая двигает вперед наш курсор
        if self.current_char == "\n":
            self.line += 1  # если current_char равен символу перехода строки, то мы опускаемся вниз
        self.position += 1  # так как мы прошли символ перехода строки, надо переместиться на новый символ

        if self.position >= len(self.text):  # если наша позиция в тексе выходит за его рамки (текста)
            self.current_char = None  # то символ который мы обрабатываем равен None
        else:
            self.current_char = self.text[self.position]  # иначе self.символ_для_обработки = self.код[позиция_в_коде]



    def retreat(self):  # функция, которая двигает вперед наш курсор
        if self.current_char == "\n":
            self.line -= 1  # если current_char равен символу перехода строки, то мы опускаемся вниз
        self.position -= 1  # так как мы прошли символ перехода строки, надо переместиться на новый символ

        if self.position >= len(self.text):  # если наша позиция в тексе выходит за его рамки (текста)
            self.current_char = None  # то символ который мы обрабатываем равен None
        else:
            self.current_char = self.text[self.position]  # иначе self.символ_для_обработки = self.код[позиция_в_коде]

    def peekPosition(self, lookhead: int = 1):
        peek_position = self.position + lookhead
        if peek_position >= len(self.text):
            return None
        return self.text[peek_position]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():  # пока символ который мы проверяем НЕ равен None и это же символ равен пробелу
            self.advance()  # то мы двигаемся вперед

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':  # пока символ который мы проверяем НЕ равен None и находится на той же строке+
            self.advance()
        if self.current_char == '\n':
            self.advance()

    def read_code_block(self):
        result = []
        while self.current_char is not None:

            #print(f"DEBUG read_code_block: current_char={repr(self.current_char)}")

            if self.current_char == '$' and self.peekPosition() == '}':
                self.advance()
                self.advance()
                break
            result.append(self.current_char)
            self.advance()
        return ''.join(result)




    def read_string_single_quotes(self):
        self.advance()  # пропускаем первую кавычку (пример -> "строка")
        result = ''

        while self.current_char is not None and (
                self.current_char != "'"):  # цикл идет пока проверяемый символ != None и != "'"
            result += self.current_char
            self.advance()  # двигаемся вперед

        if self.current_char != "'":  # проверяем, что строка закрыта
            self.error("second quotation mark not found")

        self.advance()  # пропускаем закрывающую кавычку
        return AxionTokenType.STRING, result


    def read_identifier(self):
        result = ''
        if self.current_char.isdigit():
            self.error("[read_identifier] the name cannot start with a number")
        while self.current_char is not None and (
                self.current_char.isalpha() or self.current_char == '_' or self.current_char.isdigit()):  # первый символ - буква или подчеркивание
            result += self.current_char
            self.advance()
        return result


    def read_string_double_quotes(self):
        self.advance() # пропускаем первую кавычку (пример -> "строка")
        result = ''

        while self.current_char is not None and (self.current_char != '"'): # цикл идет пока проверяемый символ != None и != '"'
            result += self.current_char
            self.advance() # двигаемся вперед

        if self.current_char != '"': # проверяем, что строка закрыта
            self.error("second quotation mark not found")

        self.advance() # пропускаем закрывающую кавычку
        return AxionTokenType.STRING, result



    def read_number(self):
        result = ''
        has_dot = False

        if self.current_char == '.':
            # Проверяем следующий символ - если цифра, то это float
            if self.peekPosition() and self.peekPosition().isdigit():
                has_dot = True
                result = '0.'  # Добавляем ведущий ноль
                #print(result)
                self.advance()  # Пропускаем точку

        while self.current_char is not None:

            if self.current_char == '.': #
                if has_dot == True: #
                    self.error("Two dots in number!") # если точка встречается повторно, выводим ошибку
                has_dot = True
                result += '.'

            elif self.current_char.isdigit(): # если символ число
                result += self.current_char # добавляем его к нашему результату (возвращаемому значению)

            else:
                break # если проверяемый символ не точка и не число, то выходим

            self.advance() # двигаемся вперед

        # Проверяем, что число не состоит из одной точки
        if result == '' or result == '0.':
            self.error("Неверный формат числа")

        if has_dot:
            return AxionTokenType.FLOAT, float(result) # если точка есть, возвращаем float
        else:
            return AxionTokenType.INTEGER, int(result) # если точки нет, возвращаем int



    def get_next_token(self, debug: bool=False):
        while self.current_char is not None:  # пока символ который мы проверяем не равен None
            if debug == True:
                print(f"DEBUG: current_char={repr(self.current_char)}, pos={self.position}")


            if self.current_char.isspace():  # если символ который мы проверяем равен пробелу
                self.skip_whitespace()  # то мы пропускаем пробелы
                continue



            if self.current_char is not None and (self.current_char.isdigit() or
                    (self.current_char == '.' and self.peekPosition() and self.peekPosition().isdigit())): # Числа
                token_type, value = self.read_number()
                return AxionToken(token_type, value, self.line)



            # -- операторы и разделители --

            if self.current_char == '+':
                self.advance()
                if self.current_char == '+':
                    self.advance()
                    return AxionToken(AxionTokenType.INCREMENT, line=self.line)
                else:
                    return AxionToken(AxionTokenType.PLUS, line=self.line)


            if self.current_char == '-':
                self.advance()

                if self.current_char == '-':
                    self.advance()
                    return AxionToken(AxionTokenType.DECREMENT, line=self.line)

                if self.current_char == '>':
                    self.advance()
                    return AxionToken(AxionTokenType.ARROW, line=self.line)

                return AxionToken(AxionTokenType.MINUS, line=self.line)


            if self.current_char == '*':
                self.advance()

                if self.current_char == '*':
                    self.advance()
                    return AxionToken(AxionTokenType.POWER, line=self.line)
                else:
                    return AxionToken(AxionTokenType.MULTIPLY, line=self.line)


            if self.current_char == '/':
                self.advance()

                if self.current_char == '/':  # Комментарий //
                    self.skip_comment()
                    continue
                else:
                    return AxionToken(AxionTokenType.DIVIDE, line=self.line)


            if self.current_char == '=':
                self.advance()

                if self.current_char == '=':
                    self.advance()
                    return AxionToken(AxionTokenType.EQUALS, line=self.line)

                return AxionToken(AxionTokenType.ASSIGN, line=self.line)


            if self.current_char == '&':
                self.advance()

                if self.current_char == '&':
                    self.advance()
                    return AxionToken(AxionTokenType.AND)

                self.error('[get_next_token] Where is the second "&" ?')


            if self.current_char == '|':
                self.advance()

                if self.current_char == '|':
                    self.advance()
                    return AxionToken(AxionTokenType.OR)

                self.error('[get_next_token] Where is the second "|" ?')


            if self.current_char == '!':
                self.advance()

                if self.current_char == '=':
                    self.advance()
                    return AxionToken(AxionTokenType.NOT_EQUALS)

                return AxionToken(AxionTokenType.NOT)


            if self.current_char == '<':
                self.advance()

                if self.current_char == '=':
                    self.advance()
                    return AxionToken(AxionTokenType.LESS_EQUAL, line=self.line)


                return AxionToken(AxionTokenType.LESS, line=self.line)


            if self.current_char == '>':
                self.advance()

                if self.current_char == '=':
                    self.advance()
                    return AxionToken(AxionTokenType.GREATER_EQUAL, line=self.line)

                return AxionToken(AxionTokenType.GREATER, line=self.line)


            if self.current_char == '{':
                self.advance()
                if self.current_char == '$':
                    self.advance()
                    code = self.read_code_block()
                    return AxionToken(AxionTokenType.CODE_BLOCK, value=code, line=self.line)

                return AxionToken(AxionTokenType.LBRACE, line=self.line)

            if self.current_char == '}':
                self.advance()
                return AxionToken(AxionTokenType.RBRACE, line=self.line)


            if self.current_char == ';':
                self.advance()
                return AxionToken(AxionTokenType.SEMICOLON, line=self.line)

            if self.current_char == ':':
                self.advance()
                return AxionToken(AxionTokenType.COLON, line=self.line)

            if self.current_char == '%':
                self.advance()
                return  AxionToken(AxionTokenType.MOD, line=self.line)

            if self.current_char == '(':
                self.advance()
                return AxionToken(AxionTokenType.LPAREN, line=self.line)

            if self.current_char == ')':
                self.advance()
                return AxionToken(AxionTokenType.RPAREN, line=self.line)

            if self.current_char == '[':
                self.advance()
                return AxionToken(AxionTokenType.LBRACKET, line=self.line)

            if self.current_char == ']':
                self.advance()
                return AxionToken(AxionTokenType.RBRACKET, line=self.line)

            if self.current_char == ';':
                self.advance()
                return AxionToken(AxionTokenType.SEMICOLON, line=self.line)

            if self.current_char == ',':
                self.advance()
                return AxionToken(AxionTokenType.COMMA, line=self.line)

            if self.current_char == '.':
                self.advance()
                return AxionToken(AxionTokenType.DOT, line=self.line)

            if self.current_char == '"': #
                token_type, value = self.read_string_double_quotes()
                return AxionToken(token_type, value, self.line)

            if self.current_char == "'": #
                token_type, value = self.read_string_single_quotes()
                return AxionToken(token_type, value, self.line)


            if self.current_char == "#":  # если символ который мы проверяем равен символу комментария (я сделал 2 символа комментариев)
                self.skip_comment()  # то мы вызываем функцию для пропуска коммментов
                continue # continue начинает цикл заново с нового символа. Это гарантирует, что после пропуска пробелов/комментариев мы обработаем следующий значимый символ


            if self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'):
                identifier = self.read_identifier()

                if identifier in self.KEYWORDS: # ищем ключевое слово
                    token_type = self.KEYWORDS[identifier]


                    # Для булевых значений возвращаем их значение
                    if token_type == AxionTokenType.BOOL:
                        bool_value = (identifier == 'True')
                        return AxionToken(token_type, bool_value, self.line)
                    return AxionToken(token_type, identifier, self.line)

                # Обычный идентификатор (если ничего не нашли возвращаем их название)
                return AxionToken(AxionTokenType.IDENTIFIER, identifier, self.line)

            else:
                self.error(f"Unexpected character: {repr(self.current_char)} (code {ord(self.current_char)})")


        return AxionToken(AxionTokenType.EOF, line=self.line)



if __name__ == '__main__':
    code = """
        block python {$
        a = 1
        print(a)
    $}
    
    
    """

    lexer = AxionLexer(code)
    tokens = []