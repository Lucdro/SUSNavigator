from HtmlInterpreter.TreeConstructor import TreeConstructor
from HtmlInterpreter.Tokenizer import Tokenizer
from HtmlInterpreter.Dom import Dom
from HtmlInterpreter.Tree import Tree

class Interpreter:
    def Parse(self, html: str) -> Tree:
        dom = Dom()
        treeConstructor = TreeConstructor()
        tokenizer = Tokenizer(html, treeConstructor)

        tokenizer.GenerateAllTokens()
        
        #tokenizer.PrintList()
        #treeConstructor.SteppedPrintTree()
        #treeConstructor.PrintTree()
    
        #self.__SteppedParse(html)
        return treeConstructor.GetTree()

    def __SteppedParse(self, html) -> None:
        treeConstructor = TreeConstructor()
        tokenizer = Tokenizer(html, treeConstructor)
        token = {}
        while(token != None):
            inp = input()
            treeConstructor.PrintCurrentTree()
            token = tokenizer.GenerateNextToken()

        treeConstructor.PrintTree()