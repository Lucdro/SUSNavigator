from ast import Attribute
from multiprocessing import Value
from operator import index
from HtmlInterpreter.TreeConstructor import TreeConstructor
import HtmlInterpreter.TokenDescription as TokenDescription
import re 

#   Tokens => tuple[int, str, dict[str, str] | None] 
class Tokenizer:
    inputStream: str
    __noContentTags = [
        '<br>',
    ]
    __tokenList: list[tuple[int, str, dict[str, str] | None]] = []
    treeConstructor: TreeConstructor
    tokenWord: int = TokenDescription.GetTokenValue('character')
    tokenTagStart: int = TokenDescription.GetTokenValue('start tag')
    tokenTagEnd: int = TokenDescription.GetTokenValue('end tag')
    selfClosingtag: int  = TokenDescription.GetTokenValue('self closing tag')
    tokenNoContent: int = TokenDescription.GetTokenValue('no content tag')
    index: int = 0

    def __init__(self , html: str, treeConstructor: TreeConstructor) -> None:
        self.inputStream = html.strip()
        self.treeConstructor = treeConstructor

    def GenerateAllTokens(self) -> list[tuple[int, str, dict[str, str] | None]]:
        while(self.GenerateNextToken() != None):
            #print('\n.')
            continue
        # try:
            
        # except AttributeError as er:
        #     print(f'LastToken before broking:{self.__tokenList[-2]}')
        return self.__tokenList

    def GenerateNextToken(self) -> tuple[int, str, dict[str, str] | None] | None:
        if self.index >= len(self.inputStream):
            return None
        #Find the next caracter
        c = self.inputStream[self.index]
        if c.isspace():
            while(c.isspace() and self.index < len(self.inputStream)):
                self.index +=1
                c = self.inputStream[self.index]
        if c.isspace():
            return None
        
        token = c 
        self.index+=1
        if c == '<':
            #Search the > and call it a token if no > is found return None
            completeTag = False
            while(self.index < len(self.inputStream)):
                token += self.inputStream[self.index]
                if self.inputStream[self.index] == '>':
                    completeTag = True
                    break
                self.index += 1
            if not completeTag:
                raise SyntaxError(f'HTML provided has a syntax error at:{self.index}')
            
            tokenName = re.search(r'</?[a-zA-Z0-9_]+',token)
            if tokenName == None:
                raise SyntaxError(f'HTML provided has a syntax error at:{self.index}')
            tokenName =  tokenName.group()
            tokenName += '>'
            tokenType: int
            if tokenName[1] == '/' and not tokenName[len(tokenName)-2] == '/':
                tokenType = self.tokenTagEnd
            elif tokenName[len(tokenName)-2] == '/' and not tokenName[1] == '/':
                tokenType = self.selfClosingtag
            elif tokenName[1] != '/' and not tokenName[len(tokenName)-2] == '/':
                if self.NoContentTag(tokenName):
                    tokenType = self.tokenNoContent
                else: 
                    tokenType = self.tokenTagStart
            else:
                raise SyntaxError(f'HTML provided has a syntax error at:{self.index}')
            props = self.GetProps(token)
            self.index += 1
            return self.AppendToken((tokenType,tokenName,props))

        #Search the next < to end the word
        while(self.index < len(self.inputStream)):
                if self.inputStream[self.index] == '<':
                    break
                token += self.inputStream[self.index]
                self.index += 1
        #Word element has None in dict arg
        return self.AppendToken((self.tokenWord,token,None))
    
    def NoContentTag(self, name:str) -> bool:
        return name in self.__noContentTags

    def AppendToken(self, token: tuple[int, str, dict[str, str] | None]) -> tuple[int, str, dict[str, str] | None] :
        self.__tokenList.append(token)
        self.treeConstructor.AddToken(token)
        return token

    def AddToken(self, index: int, token: tuple[int, str, dict[str, str] | None]) -> None:
        self.__tokenList.insert(index, token)

    def RemoveToken(self, index: int) -> None:
        self.__tokenList.pop(index)
    
    def PrintList(self) -> None:
        for token in self.__tokenList:
            print(f'\nName: {token[1]}\nType: {TokenDescription.GetTokenDescription(token[0])}\nProps: {token[2]}')

    def GetProps(self, tag: str) -> dict[str,str]:
        propsList = re.findall(r'\s+[a-zA-Z0-9_]+=[\"|\'][^[\"|\']*[\"|\']',tag)
        propsDict = {}
        for prop in propsList:
            name = re.search(r'[a-zA-Z0-9_-]+=[\"|\']',prop)
            name = '' if name == None else name.group()
            value = re.search(r'=[\"|\'][ a-zA-Z0-9_:;-]+[\"|\']',prop)
            value = '' if value == None else value.group()
            if name != '':
                name = name[0:len(name)-2]
                value = '' if value == None else value[2:len(value)-1]
                propsDict[name] = value
        return propsDict