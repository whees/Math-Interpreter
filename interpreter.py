# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
PLUS, MINUS, MUL, LPAREN, RPAREN, EOF, POLY, DERIV = (
    'PLUS', 'MINUS', 'MUL', 'LPAREN', 'RPAREN', 'EOF', 'POLY', 'DERIV'
)


def sort(key):        
    return tuple(sorted(list(key),reverse = True))

def chain(key):
    ret = Poly()
    
    for string in key:
        if string[0] == '/':
            newterm = divide(list(key) + [f'&{string[1:]}',f'/{string[1:]}'])
            ret = ret + Poly({newterm:-1})
        else:
            newterm = divide(list(key) + [f'&{string}',f'/{string}'])
            ret = ret + Poly({newterm:1})
           
    return ret

def divide(key):
    keyaslist = list(key)
    
    for string in key:
        if string[0] == '/':
            if string[1:] in keyaslist:
                keyaslist.remove(string)
                keyaslist.remove(string[1:])
                
    return sort(keyaslist)
    
class Poly:
    def __init__(self, terms = None):        
        self.terms = {} if terms == None or type(terms) != dict else terms
        self.trim()
        
    def __add__(self,opp):
        terms = {}
        
        for key in self.terms.keys():
            if key in opp.terms.keys():
                terms[key] = self.terms[key] + opp.terms[key]
            else: 
                terms[key] = self.terms[key]
                
        for key in opp.terms.keys():
            if key not in self.terms.keys():
                terms[key] = opp.terms[key]
                
        return Poly(terms)
    
    def __sub__(self,opp):
        terms = {}
        
        for key in self.terms.keys():
            if key in opp.terms.keys():
                terms[key] = self.terms[key] - opp.terms[key]
            else: 
                terms[key] = self.terms[key]
                
        for key in opp.terms.keys():
            if key not in self.terms.keys():
                terms[key] = - opp.terms[key]
                
        return Poly(terms)

    def __mul__(self,opp):
        terms = {}
        
        for selfkey in self.terms.keys():
            for oppkey in opp.terms.keys():
                newkey = sort(list(selfkey) + list(oppkey))
                
                if newkey in terms.keys():
                    terms[newkey] += self.terms[selfkey] * opp.terms[oppkey]
                else:
                    terms[newkey] = self.terms[selfkey] * opp.terms[oppkey]
                    
        return Poly(terms)
    
    def __str__(self):
        ret = ''
        for n,key in enumerate(self.terms.keys()):
            if n > 0:
                ret += str(abs(self.terms[key])) if abs(self.terms[key]) != 1 else ''
            else:
                ret += str(self.terms[key]) if abs(self.terms[key]) != 1 else ''
            
            for string in key:
                for c,char in enumerate(string):
                    if char != '&':
                        ret += char
                    else:
                        ret += f'({string[c:]})'
                        break
                
            if n < len(self.terms.keys()) - 1:
                ret += ' + ' if self.terms[list(self.terms.keys())[n+1]] >= 0 else ' - '
            
            
            
        return ret

    def __repr__(self):
        return self.__str__()
    
    def trim(self):
        keys = self.terms.copy().keys()
        
        for key in keys:
            if self.terms[key] == 0:
                self.terms.pop(key)
    
    def derive(self):
        ret = Poly()
        
        for key in self.terms.keys():
            ret = ret + chain(key)
            
        return ret




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
        return Poly({():int(result)})
    
    def variable(self):
        result = Poly({(self.current_char,):1})
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
            result = self.factor().derive()
            return result
        else:
            self.error()


    def term(self):
        """term : factor ((MUL) factor)*"""
        result = self.factor()

        while self.current_token.type in (MUL,):
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