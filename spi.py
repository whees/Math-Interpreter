(log, PART, VAR, DIF,INT, ADD, SUB, MUL, DIV, LPAREN, RPAREN, ID, ASSIGN,
 SEMI, EOF, LBRACK, RBRACK, show, UNDERSCORE) = (
    'log','PART', 'VAR','DIF','INT', 'ADD', 'SUB', 'MUL', 'DIV', '(', ')', 'ID', 'ASSIGN',
    'SEMI', 'EOF', '{', '}','show','_')
     
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value


    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self,opp):
        return opp.type == self.type and opp.value == self.value

RESERVED_KEYWORDS = {show: Token(show,show),
                     log: Token(log,log)}
WEIGHT_KEYS = {ADD: '*', 
               MUL: '^'}

class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception(f'Invalid character {self.current_char}')

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
        return int(result)
    
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum()):
            result += self.current_char
            self.advance()
        
        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token
    
    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return Token(INT, self.integer())

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == '+':
                self.advance()
                return Token(ADD, '+')

            if self.current_char == '-':
                self.advance()
                return Token(SUB, '-')

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
            
            if self.current_char == '{':
                self.advance()
                return Token(LBRACK, '{')
            
            if self.current_char == '}':
                self.advance()
                return Token(RBRACK, '}')
            
            if self.current_char == '&':
                self.advance()
                return Token(DIF,'&')
            
            if self.current_char == '$' and self.peek() == '_':
                self.advance()
                self.advance()
                return Token(PART,'$')

            self.error()

        return Token(EOF, None)
    
    def reset(self):
        self.pos = 0
        self.current_char = self.text[self.pos]

class AST(object):
    pass

class NoOp(AST):
    pass

class Compound(AST):
    def __init__(self):
        self.children = []
        
class Num(AST):
    def __init__(self,token,weight = 1):
        self.token = token
        self.weight = weight
        
    def __eq__(self,opp):
        return self.token == opp.token
    
    def copy(self):
        return Num(self.token,self.weight)
        
class Id(AST):
    def __init__(self, token, weight = 1):
        self.token = token
        self.weight = weight
        
    def __eq__(self,opp):
        return self.token == opp.token
    
    def copy(self):
        return Id(self.token,self.weight)
        
class Var(AST):
    def __init__(self, token, order = 1, weight = 1):
        self.token = Token(VAR,token.value)
        self.order = order
        self.weight = weight
    
    def __eq__(self,opp):
        return self.token == opp.token
    
    def copy(self):
        return Var(self.token,self.order,self.weight)

class AsOp(AST):
    def __init__(self, token, weight = 1):
        self.token = self.op = token
        self.args = []
        self.weight = weight
        
    def __eq__(self,opp):
        if opp.token != self.token:
            return False
        for arg in self.args:
            if arg not in opp.args:
                return False
        for arg in opp.args:
            if arg not in self.args:
                return False
        return True
    
    def copy(self):
        copy = AsOp(self.token,self.weight)
        copy.args += self.args
        return copy
    
class UnOp(AST):
    def __init__(self, token, arg, weight = 1):
        self.token = self.op = token
        self.arg = arg
        self.weight = weight
        
    def __eq__(self,opp):
        return self.token == opp.token and self.arg == opp.arg
    
    def copy(self):
        return UnOp(self.token,self.arg,self.weight)
    
class BinOp(AST):
    def __init__(self, left, token, right, weight = 1):
        self.token = self.op = token
        self.left = left
        self.right = right
        
    def __eq__(self,opp):
        return self.token == opp.token and self.arg == opp.arg
    
    def copy(self):
        return BinOp(self.left,self.token,self.right)
    
class Assign(AST):
    def __init__(self, left, token, right):
        self.left = left
        self.token = self.op = token
        self.right = right
        
class Show(AST):
    def __init__(self,token,args):
        self.token = self.op = token
        self.args = args
    
def ADDTOKEN():
    return Token(ADD,'+')

def MULTOKEN():
    return Token(MUL,'*')

def DIFTOKEN():
    return Token(DIF,'&')

def NUM(n):
    return Num(Token(INT,n))

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception(f'Invalid syntax at {self.current_token}')
        
    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f'Invalid syntax: Expected {token_type}, got {self.current_token.type}')
            
    def program(self):
       node = self.compound_statement()
       return node
   
    def compound_statement(self):
        nodes = self.statement_list()

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root
    
    def statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()
  
        results = [node]
  
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())
  
        if self.current_token.type == ID:
            self.error()
  
        return results
    
    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == show:
            node = self.show_statement()
        else:
            node = self.empty()
            
        return node
    
    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node
    
    def show_statement(self):
        token = self.current_token
        self.eat(show)
        self.eat(LPAREN)
        args = self.variable()
        node = Show(token, args)
        self.eat(RPAREN)
        return node
    
    def variable(self):
        node = Id(self.current_token)
        self.eat(ID)
        return node
   
    def empty(self):
        return NoOp()

    def factor(self):
        token = self.current_token
     
        if token.type == INT:
            self.eat(INT)
            return Num(token)
        elif token.type == ID:
            node = self.variable()
            return node
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == DIF:
            self.eat(DIF)
            node = self.expr()
            return UnOp(token,node)
        elif token.type == log:
            self.eat(log)
            self.eat(LPAREN)
            node = UnOp(token,self.expr())
            self.eat(RPAREN)
            return node
        elif token.type == PART:
            self.eat(PART)
            left = self.variable()
            self.eat(LPAREN)
            right = self.expr()
            self.eat(RPAREN)
            node = BinOp(left,token,right)
            return node

    def term(self):
        node = self.factor()
        
        while self.current_token.type in (MUL,DIV):
            token = self.current_token
            newnode = AsOp(MULTOKEN())
            newnode.args += [node]
            
            if token.type == MUL:
                self.eat(MUL)
                newnode.args += [self.factor()]
            elif token.type == DIV:
                self.eat(DIV)
                divnode = AsOp(MULTOKEN(),weight = -1)
                divnode.args += [self.factor()]
                newnode.args += [divnode]
            
            node = newnode
                
        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (ADD,SUB):
            token = self.current_token
            newnode = AsOp(ADDTOKEN())
            newnode.args += [node]
            
            
            if token.type == ADD:
                self.eat(ADD)
                newnode.args += [self.term()]
            elif token.type == SUB:
                self.eat(SUB)
                minnode = AsOp(ADDTOKEN(),weight = -1)
                minnode.args += [self.term()]
                newnode.args += [minnode]
                
            node = newnode
                
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node
    


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
        
class FunctionalDeriver(NodeVisitor):
    def __init__(self,tree):
        self.tree = tree
    
    def visit_Num(self,node):
        return NUM(0)
    
    def visit_Var(self,node):
        return Var(node.token,node.order + 1,node.weight)
        
    def visit_AsOp(self,node):
        if node.token.type == ADD:
            newnode = AsOp(node.token, weight = node.weight)
            for arg in node.args:
                newnode.args += [self.visit(arg)]
            return newnode
        elif node.token.type == MUL:
            newnode = AsOp(ADDTOKEN(),weight = node.weight)
            for i,arg in enumerate(node.args):
                coeff = [node.args[j] for j in range(len(node.args)) if i!=j]
                argcopy = arg.copy()
                mulnode = AsOp(node.token,arg.weight)
                argcopy.weight -= 1                
                coeff += [argcopy]
                coeff += [self.visit(arg)]                
                mulnode.args += coeff
                newnode.args += [mulnode]
            
                
            return newnode
        return node
    
    def visit_UnOp(self,node):
        if node.token.type == log:
            newnode = AsOp(MULTOKEN(),weight=node.weight)
            argcopy = node.arg.copy()
            argcopy.weight = -1
            newnode.args += [argcopy]
            newnode.args += [self.visit(node.arg)]
            return newnode
        else:
            raise Exception(f'cannot differentiate unop of type {node.token.type}')
        
    def visit_Id(self,node):
        return Var(node.token)
        
    def derive(self):
        return self.visit(self.tree)
    
class PartialDeriver(NodeVisitor):
    def __init__(self,left,right):
        self.right = right
        self.left = left
    
    def visit_Num(self,node):
        return NUM(0)
        
    def visit_AsOp(self,node):
        if node.token.type == ADD:
            newnode = AsOp(node.token, weight = node.weight)
            for arg in node.args:
                newnode.args += [self.visit(arg)]
            return newnode
        elif node.token.type == MUL:
            newnode = AsOp(ADDTOKEN(),weight = node.weight)
            for i,arg in enumerate(node.args):
                coeff = [node.args[j] for j in range(len(node.args)) if i!=j]
                argcopy = arg.copy()
                mulnode = AsOp(node.token,arg.weight)
                argcopy.weight -= 1
                coeff += [argcopy]
                coeff += [self.visit(arg)]
                mulnode.args += coeff
                newnode.args += [mulnode]
            return newnode
        return node
    
    def visit_UnOp(self,node):
        if node.token.type == log:
            newnode = AsOp(MULTOKEN(),weight=node.weight)
            argcopy = node.arg.copy()
            argcopy.weight = -1
            newnode.args += [argcopy]
            newnode.args += [self.visit(node.arg)]
            return newnode
        else:
            raise Exception(f'cannot differentiate unop of type {node.token.type}')
        
    def visit_Id(self,node):
        if node == self.left:
            return NUM(1)
                
        return NUM(0)
        
    def derive(self):
        return self.visit(self.right)

class Interpreter(NodeVisitor):
    GLOBAL_SCOPE = {}
    def __init__(self):
        pass
    
    def visit_UnOp(self,node):
        if node.token.type == DIF:
            node = self.visit(FunctionalDeriver(node.arg).derive())
            
        return node
    
    def visit_BinOp(self,node):
        if node.token.type == PART:
            node = self.visit(PartialDeriver(node.left,node.right).derive())
            
        return node
    
    def visit_Num(self,node):
        return node
    
    def visit_Var(self,node):
        return node
    
    def visit_Id(self,node):
        var_name = node.token.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is not None:
            node = self.visit(val)
        
        return node
    
    def visit_NoOp(self,node):
        pass
        
    def visit_AsOp(self, node):    
        newnode = AsOp(node.token,node.weight)
               
        for arg in node.args:
            newnode.args += [self.visit(arg)]
        
        newnode = self.chain(newnode)  
        newnode = self.string(newnode)
        newnode = self.combinelike(newnode)
        newnode = self.trim(newnode)
        return newnode
    
    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)
            
    def visit_Assign(self, node):
        var_name = node.left.token.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
        
    def visit_Show(self, node):
        var_name = node.args.token.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(f'{var_name} does not exist in global scope')
        else:
            self.show(self.visit(val))
            
    def show(self,node):              
        string = ''
        
        if isinstance(node,AsOp):
            for i,arg in enumerate(node.args):
                string += str(node.token.value)*int(i>0)+self.arg_string(arg,node.token) 
                string += (WEIGHT_KEYS[node.token.type] + f'({arg.weight})') * int(arg.weight!=1)
        elif isinstance(node,Id):
            string += str(node.token.value) 
        elif isinstance(node,Var):
            string += '&' * node.order + str(node.token.value)
        elif isinstance(node,Num):
            string += str(node.token.value)
            
        print(string)
        
    def arg_string(self,node,token):
        string = ''
        if isinstance(node,Id):
            return '(' + str(node.token.value) + ')'
        elif isinstance(node,Var):
            return   '(' + '&' * node.order + str(node.token.value) + ')'
        elif isinstance(node,Num):
            return str(node.token.value)
        
        if len(node.args) == 0:
            return '('+str(node.token.value) + (WEIGHT_KEYS[token.type] + str(node.weight)) * int(node.weight!=1)+')'
        

        string += '{'
        for i,arg in enumerate(node.args):
            string += str(node.token.value)*int(i>0)+self.arg_string(arg,node.token) 
            string += (WEIGHT_KEYS[node.token.type] + f'({arg.weight})') * int(arg.weight!=1)
            
        string += '}'
        return string
            
    def trim(self,node):
        if not isinstance(node,AsOp):
            return node
        if node.token.type == MUL:
            for arg in node.args:
                if arg.token.value == 0:
                    return NUM(0)
        
        newnode = AsOp(node.token, weight = node.weight)
        for arg in node.args:
            if arg.weight != 0 and (arg.token != NUM(0).token and node.token == ADDTOKEN() or arg.token != NUM(1).token and node.token == MULTOKEN()):
                newnode.args += [arg]
        
        if not len(newnode.args):
            if node.token.type == MUL:
                return NUM(1)
            elif node.token.type == ADD:
                return NUM(0)
                
        return newnode

    def string(self,node):
        if not isinstance(node,AsOp):
            return node
        if node.weight == 1 and len(node.args) == 1 and node.token.type != DIF:
            if node.args[0].weight == 1:
                return node.args[0]
        
        return node              
        
    def combinelike(self,node):
        if not isinstance(node,AsOp):
            return node
        
        newnode = AsOp(node.token,weight=node.weight)
        
        for arg in node.args:
            if arg in newnode.args:
                i = newnode.args.index(arg)
                newnode.args[i].weight += arg.weight
            else:
                newnode.args += [arg]
            
        return newnode
    
    def chain(self,node):
        if not isinstance(node,AsOp):
            return node
        
        newnode = AsOp(node.token,weight=node.weight)
        
        for arg in node.args:
            if arg.token.type == node.token.type and (arg.weight == 1 or len(node.args) == 1):
                for argarg in arg.args:
                    argargcopy = argarg.copy()
                    argargcopy.weight *= arg.weight
                    newnode.args += [argargcopy]
            else:
                newnode.args += [arg]
                
        return newnode
                        
    def interpret(self):
        while True:
            try:
                text = input('> ')
            except EOFError:
                break
            
            if not text:
                continue

            lexer = Lexer(text)
            parser = Parser(lexer)
            tree = parser.parse()
            tree = self.visit(tree)
    
def main():
    interpreter = Interpreter()
    interpreter.interpret()
    
    
if __name__ == '__main__':
    main()