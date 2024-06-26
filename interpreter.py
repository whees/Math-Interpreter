# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
PLUS, MINUS, MUL, LPAREN, RPAREN, EOF, POLY, DERIV = (
    'PLUS', 'MINUS', 'MUL', 'LPAREN', 'RPAREN', 'EOF', 'POLY', 'DERIV'
)




class poly:
    def __init__(self, value = 0, vars = None):
        self.value = value
        self.vars = {} if vars == None else vars
        
    def __str__(self):
        string = f'{self.value}' if self.value != 0 else ''
        for key,value in self.vars.items():
            if value != 0 and value**2 != 1:
                sign = '+' if value > 0 else ''
                string += sign + f'{value}{key}'
            elif value**2 == 1:
                sign = '+' if value > 0 else '-'
                string += sign + f'{key}'
        
        if string[0] == '+':
            string = string[1:]
            
        return string

    def __repr__(self):
        return self.__str__()
    
    def __add__(self,opp):
        ret = poly()
        ret.value = opp.value + self.value
        
        for key,value in self.vars.items():
            ret.vars[key] = value
            if key in opp.vars.keys():
                ret.vars[key] += opp.vars[key]
                
        for key,value in opp.vars.items():
            if key not in self.vars.keys():
                ret.vars[key] = opp.vars[key]
                
        ret.simplify()
        return ret
    
    def __sub__(self,opp):
        ret = poly()
        ret.value = self.value - opp.value
        
        for key,value in self.vars.items():
            ret.vars[key] = value
            if key in opp.vars.keys():
                ret.vars[key] -= opp.vars[key]
                
        for key,value in opp.vars.items():
            if key not in self.vars.keys():
                ret.vars[key] = -opp.vars[key]
                
        ret.simplify()
        return ret
    
    def __mul__(self,opp):
        ret = poly()
        ret.value = opp.value * self.value
        
        for key,value in self.vars.items():
            ret.vars[key] = opp.value * value
        
        for key,value in opp.vars.items():
            if key in ret.vars.keys():
                ret.vars[key] += value * self.value
            else:
                ret.vars[key] = value * self.value
            
        for skey,svalue in self.vars.items():
            for okey,ovalue in opp.vars.items():
                keystring = ''.join(sorted(okey + skey))
                if keystring in ret.vars.keys():
                    ret.vars[keystring] += svalue * ovalue
                else:
                    ret.vars[keystring] = self.vars[skey] * opp.vars[okey]
                    
        ret.simplify()
        return ret
            
    def simplify(self):
        keys = self.vars.copy().keys()
        for key in keys:
            if self.vars[key] == 0:
                self.vars.pop(key)
                
    def chain(self,key):
        ret = poly()
        
        
        for x in key:
            rkey = key.replace(x,'',1) + f'(&{x})'
            
            if rkey not in ret.vars.keys():
                ret.vars[rkey] = 1
            else: 
                ret.vars[rkey] += 1
 
        return ret
        
    def deriv(self):
        ret = poly()
        
        for key,value in self.vars.items():
            ret = ret + self.chain(key) * poly(value)
            
        return ret
        
    def copy(self):
        return poly(self.value,self.vars.copy())
    


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, MUL, DIV, or EOF
        self.type = type
        # token value: non-negative integer value, '+', '-', '*', '/', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return poly(int(result))
    
    def variable(self):
        result = poly(0,{self.current_char:1})
        self.advance()
        return result

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(POLY, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            if self.current_char.isalpha():
                return Token(POLY, self.variable())
            
            if self.current_char == '&':
                self.advance()
                return Token(DERIV, '&')
            

            self.error()

        return Token(EOF, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : POLY"""
        token = self.current_token
        
        
        if token.type == POLY:
            self.eat(POLY)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        elif token.type == DERIV:
            self.eat(DERIV)
            result = self.factor().deriv()
            return result
        else:
            self.error()


    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        result = self.factor()

        while self.current_token.type in (MUL):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()