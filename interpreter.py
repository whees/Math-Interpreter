# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
from math import gcd
PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, FRAC, DERIV = (
    'PLUS', 'MINUS', 'MUL','DIV', 'LPAREN', 'RPAREN', 'EOF', 'FRAC', 'DERIV'
)



def isvalid(key):
    if len(key) != 2:
        return False
    
    if len(key[0]) != len(key[1]):
        return False
    
    for chars in key[0]:
        if type(chars) != str:
            return False
    
    for nums in key[1]:
        if type(nums) != int and type(nums) != float:
            return False
    
    return True

def sort(key):
    order = sorted(range(len(key[0])), key=lambda k: key[0][k])
    charsaslist = []
    numsaslist = []
    
    for i in order:
        charsaslist += [key[0][i]]
        numsaslist += [key[1][i]]
        
    return (tuple(charsaslist),tuple(numsaslist))

def prod(key):
    ret = Poly()
    
    for i in range(len(key[0])):
        newcharsaslist = [f'&{key[0][i]}']
        newnumsaslist = [1]
        
        for j in range(len(key[0])):
            if j == i:
                newcharsaslist += [key[0][j]]
                newnumsaslist += [key[1][j] - 1]
            else:
                newcharsaslist += [key[0][j]]
                newnumsaslist += [key[1][j]]
                
        newkey = (tuple(newcharsaslist), tuple(newnumsaslist))
        ret = ret + Poly({newkey:key[1][i]})
        
    return ret
        

    
class Poly:
    def __init__(self, terms = None):
        self.terms = terms if terms != None else {}
        self.validate()
        self.annihilate()
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
                newkey = sort([list(selfkey[0]) + list(oppkey[0]),list(selfkey[1]) + list(oppkey[1])])
                
                if newkey in terms.keys():
                    terms[newkey] += self.terms[selfkey] * opp.terms[oppkey]
                else:
                    terms[newkey] = self.terms[selfkey] * opp.terms[oppkey]
                    
        return Poly(terms)
    
    def __str__(self):
        ret = ''
        for n,key in enumerate(self.terms.keys()):
            coeff = int(self.terms[key]) if int(self.terms[key] % 1*1000) == 0 else self.terms[key]
            if n > 0:
                ret += ' + ' if coeff >= 0 else ' - '
                ret += str(abs(coeff)) if abs(self.terms[key]) != 1 or len(key[0]) == 0 else ''

            else:
                ret += '' if coeff >= 0 else '-'
                ret += str(abs(coeff)) 

            for i in range(len(key[0])):
                if key[0][i][0] != '&':
                    if key[1][i] == 1:
                        ret += f'{key[0][i]}'
                    elif key[1][i] != 0:
                        ret += f'{key[0][i]}^{key[1][i]}'
                else:
                    if key[1][i] == 1:
                        ret += f'({key[0][i]})'
                    elif key[1][i] != 0:
                        ret += f'({key[0][i]})^{key[1][i]}'
                    
            
                
        return ret if ret!= '' else '0'
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self,opp):
        if opp == None:
            return False
        
        for key,value in self.terms.items():
            if (key,value) not in opp.terms.items():
                return False
            
        for key,value in opp.terms.items():
            if (key,value) not in self.terms.items():
                return False
        
        return True
        
    def validate(self):
        for key in self.terms.keys():
            if not isvalid(key):
                raise Exception(f'invalid key: {key}')
                
    def annihilate(self):
        copyterms = self.terms.copy()
        
        for key in copyterms.keys():
            newcharslist = []
            newnumslist = []
            
            for i in range(len(key[0])):
                if key[0][i] not in newcharslist:
                    newcharslist += [key[0][i]]
                    newnumslist += [key[1][i]]
                else:
                    j = newcharslist.index(key[0][i])
                    newnumslist[j] += key[1][i]
                    
            newkey = sort([newcharslist,newnumslist])
            if newkey != key:
                self.terms.pop(key)
                self.terms[newkey] = copyterms[key]
         
    def trim(self):
        copyterms = self.terms.copy()
        
        for key in copyterms.keys():
            newcharslist = []
            newnumslist = []
            
            for i in range(len(key[0])):
                if key[1][i] != 0:
                    newcharslist += [key[0][i]]
                    newnumslist += [key[1][i]]
                
            newkey = sort((tuple(newcharslist),tuple(newnumslist)))
            if newkey != key or copyterms[key] == 0:
                self.terms.pop(key)
                if copyterms[key] != 0:
                    self.terms[newkey] = copyterms[key]
                    
    def derive(self):
        ret = Poly()
        
        for key in self.terms.keys():
            ret = ret + prod(key) * Poly({((),()):self.terms[key]})
            
        return ret
    
    def hasfactor(self):
        rfacs = []
        rpwrs = []
        keyslist = list(self.terms.keys())
        if len(keyslist) < 1:
            return rfacs,rpwrs
        
        
        chars = keyslist[0][0]
        nums = keyslist[0][1]
        
        for j in range(len(chars)):
            n = 1
            cpow = nums[j]
            for i in range(1,len(keyslist)):
                if chars[j] in keyslist[i][0]:
                    n += 1
                    ind = keyslist[i][0].index(chars[j])
                    if abs(keyslist[i][1][ind]) < abs(cpow):
                        cpow = keyslist[i][1][ind]
                    continue
                else:
                    break
            if n == len(keyslist):
                rfacs += [chars[j]]
                rpwrs += [cpow]
            
        return rfacs,rpwrs
    
    def factor(self,charnum):
        char,num = charnum
        copyterms = self.terms.copy()
        
        for key in copyterms.keys():
            newcharslist = []
            newnumslist = []
            
            if char in key[0]:
                for i in range(len(key[0])):
                    newcharslist += [key[0][i]]
                    newnumslist += [key[1][i] - num] if key[0][i] == char else [key[1][i]]
                
                newkey = (tuple(newcharslist),tuple(newnumslist))
                self.terms.pop(key)
                self.terms[newkey] = copyterms[key]
                
            else:
                raise Exception(f'bad factor: {char}')
             
        self.validate()
        self.annihilate()
        self.trim()
                
                
        
        

class Frac:
    def __init__(self,num = None, den = None):
        self.num = num if num != None else Poly()
        self.den = den if den != None else Poly()
        self.annihilate()
        
    def __add__(self,opp):
        num = self.num * opp.den + opp.num * self.den
        den = self.den * opp.den
        
        return Frac(num,den)
    
    def __sub__(self,opp):
        num = self.num * opp.den - opp.num * self.den
        den = self.den * opp.den
        
        return Frac(num,den)
    
    def __mul__(self,opp):
        num = self.num * opp.num
        den = self.den * opp.den
        
        return Frac(num,den)
    
    def __truediv__(self,opp):
        num = self.num * opp.den
        den = self.den * opp.num
        
        return Frac(num,den)
    
    def __str__(self):
        strnum = str(self.num)
        strden = str(self.den) 
        lenbar = max([len(strnum),len(strden)])
        strbar = '-' * lenbar
        dencush = (lenbar - len(strden)) // 2 * ' '
        numcush = (lenbar - len(strnum)) // 2 * ' '
        ret = numcush + strnum 
        if strden != '1':
            ret += '\n' + strbar + '\n' + dencush + strden
        
        return ret
        
    def derive(self):
        num = self.den * self.num.derive() - self.den.derive() * self.num
        den = self.den * self.den
        
        return Frac(num,den)
    
    def annihilate(self):
        numslist = []
        dofactor = True
        
        for key in self.num.terms.keys():
            coeff = round(self.num.terms[key],3)
            if coeff % 1 * 1000 == 0:
                numslist += [round(self.num.terms[key])]
            else:
                dofactor = False
                break
            
        if dofactor:
            for key in self.den.terms.keys():
                coeff = round(self.den.terms[key],3)
                if coeff % 1 * 1000 == 0:
                    numslist += [round(self.den.terms[key])]
                else:
                    dofactor = False
                    break
            
        if dofactor:
             div = gcd(*numslist)
        
        for key in self.num.terms.keys():
            self.num.terms[key] /= div
            
        for key in self.den.terms.keys():
            self.den.terms[key] /= div
            
        numfacs,numpwrs = self.num.hasfactor()
        denfacs,denpwrs = self.den.hasfactor()
        
        for i in range(len(numfacs)):
            if numfacs[i] in denfacs:
                ind = denfacs.index(numfacs[i])
                mpwr = min(denpwrs[ind],numpwrs[i])
                
                self.num.factor((numfacs[i],mpwr))
                self.den.factor((numfacs[i],mpwr))
                
   
        if self.num.terms == self.den.terms:
            self.num = Poly({((),()):1})
            self.den = Poly({((),()):1})
        


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
        
        
        return Frac(Poly({((),()):int(result)}),Poly({((),()):1}))
    
    def variable(self):
        num = Poly({((self.current_char,),(1,)):1})
        den = Poly({((),()):1})
        self.advance()
        return Frac(num,den)

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
                return Token(FRAC, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            if self.current_char.isalpha():
                return Token(FRAC, self.variable())
            
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
        
        
        if token.type == FRAC:
            self.eat(FRAC)
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

        while self.current_token.type in (MUL,DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
                
            if token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()

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