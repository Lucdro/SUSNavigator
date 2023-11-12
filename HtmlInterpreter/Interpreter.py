from HtmlInterpreter.DomCreator import DomCreator
from HtmlInterpreter.TreeConstructor import TreeConstructor
from HtmlInterpreter.Tokenizer import Tokenizer
from HtmlInterpreter.DomCreator import DomCreator
from HtmlInterpreter.Tree import Tree
from typing import Any, Self

class Interpreter:
    def Parse(self, html: str) -> DomCreator:
        treeConstructor = TreeConstructor()

        tokenizer = Tokenizer(html, treeConstructor)
        tokenizer.GenerateAllTokens()
        
        domCreator = DomCreator(treeConstructor.GetTree())
        domObj = domCreator.CreateDOM()
        return domCreator

    # def __SteppedParse(self, html) -> None:
    #     treeConstructor = TreeConstructor()
    #     tokenizer = Tokenizer(html, treeConstructor)
    #     token = {}
    #     while(token != None):
    #         inp = input()
    #         treeConstructor.PrintCurrentTree()
    #         token = tokenizer.GenerateNextToken()

    #     treeConstructor.PrintTree()