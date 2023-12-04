import HtmlInterpreter.TokenDescription as TokenDescription
import HtmlInterpreter.Tags as Tags
from HtmlInterpreter.Tree import Tree

class TreeConstructor:
    tokenWord: int = TokenDescription.GetTokenValue('character')
    tokenTagStart: int = TokenDescription.GetTokenValue('start tag')
    tokenTagEnd: int = TokenDescription.GetTokenValue('end tag')
    tokenSelfClsTag: int = TokenDescription.GetTokenValue('self closing tag')
    tokenNoContent: int = TokenDescription.GetTokenValue('no content tag')
    __treeBuffer: list[Tree] = []
    __tree: Tree = Tree('root', 0)
    __currentTree: Tree = __tree
    def __init__(self) -> None:
        pass
    
    def AddToken(self, token: tuple[int, str, dict[str, str] | None]) -> None:
        if token[0] == self.tokenTagStart:
            if Tags.CanHaveChild(token[1]):
                self.__treeBuffer.append(self.__currentTree)
                self.__currentTree = self.__currentTree.AppendChild(Tree(token[1],token[0],[],token[2]))
                #self.__currentTree.Print()
            else:
                self.__currentTree.AppendChild(Tree(token[1],token[0],[],token[2]))
                #temp.Print()
        elif token[0] == self.tokenWord:
            self.__currentTree.AppendChild(Tree(token[1],token[0],[],{}))
            #temp.Print()
        elif token[0] == self.tokenTagEnd:
            if self.__currentTree.GetValue()[1:len(self.__currentTree.GetValue())-1] == token[1][2:len(token[1])-1]:
                self.__currentTree = self.__treeBuffer.pop()
                #self.__currentTree.Print()
            else:
                raise SyntaxError(f'Tag:{token[1]} was never opened')
        elif token[0] == self.tokenSelfClsTag:
            self.__currentTree.AppendChild(Tree(token[1],token[0],[],token[2]))
        elif token[0] == self.tokenNoContent:
            self.__currentTree.AppendChild(self.GetNoContentTree(token))
            #temp.Print()
        #self.__currentTree.Print()
    
    def GetNoContentTree(self, token: tuple[int, str, dict[str, str] | None]) -> Tree:
        if token[1] == '<br>':
            return Tree('\n',self.tokenWord,[],{})
        else:
            return Tree('',self.tokenWord,[],{})

    def PrintTree(self) -> None:
        self.__tree.Print()

    def SteppedPrintTree(self) -> None:
        self.__tree.SteppedPrint('')


    def GetTree(self) -> Tree:
        return self.__tree
    
    def PrintCurrentTree(self) -> None:
        self.__currentTree.Print() 