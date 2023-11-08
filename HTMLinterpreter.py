import re
#
TOKENSDESCRIPTION = [
    ('DOCTYPE',1),
    ('start tag',2),
    ('end tag',3),
    ('comment',4),
    ('character',5),
    ('end-of-file',6)
]
def GetTokenDescription(value: int) -> str:
    for description in TOKENSDESCRIPTION:
        if description[1] == value:
            return description[0] 
    return ''
def GetTokenValue(name: str) -> int:
    for description in TOKENSDESCRIPTION:
        if description[0] == name:
            return description[1] 
    return -1
    
#   Other tags will be converted to div
RECOGNIZEDTAGS = [
    ('html',True),
    ('head',True),
    ('body',True),
    ('title',True),
    ('p',True),
    ('br',False),
    ('div',True),
    ('h1',True),
    ('h2',True),
    ('h3',True),
    ('h4',True),
    ('h5',True),
    ('h6',True),
    ('span',True),
    ('img',True),
]
def IsRecognizedTag(name: str) -> bool:
    for tag in RECOGNIZEDTAGS:
        if tag[0] == name:
            return True
    return False
def CanHaveChild(name: str) -> bool:
    for tag in RECOGNIZEDTAGS:
        if tag[0] == name:
            return tag[1]
    return False

#   Tokens => dic(tokendescription,token,Dic(props)) => '' if dont have 
class Tokenizer:
    inputStream = ''
    __tokenList = []

    def __init__(self , html: str) -> None:
        self.AlterInput(html)
        
    def AlterInput(self, html: str) -> None:
        self.inputStream = html.strip()
        self.GenerateTokenList()

    def GenerateTokenList(self) -> None:
        index = 0
        tokenDescWord = GetTokenValue('character')
        tokenDescTagStart = GetTokenValue('start tag')
        tokenDescTagEnd = GetTokenValue('end tag')
        self.__tokenList = []
        while(index < len(self.inputStream)):
            c = self.inputStream[index]
            #skip this iteration
            if c == ' ':
                index +=1
                continue
            token = ''
            token += c 
            if c == '<':
                index+=1
                tokenType = tokenDescTagEnd if self.inputStream[index] == '/' else tokenDescTagStart
                #search the > and call it a token
                while(index < len(self.inputStream)):
                    token += self.inputStream[index]
                    if self.inputStream[index] == '>':
                        break
                    index += 1
                tokenName = re.search(r'</?[a-zA-Z0-9_]+',token)
                tokenName = '<' if tokenName == None else tokenName.group()
                tokenName += '>'
                props = self.GetProps(token)
                self.AppendToken((tokenType,tokenName,props))
                index += 1
                continue
            #search the next tag to end the word
            index +=1
            while(index < len(self.inputStream)):
                    if self.inputStream[index] == '<':
                        break
                    token += self.inputStream[index]
                    index += 1
            self.AppendToken((tokenDescWord,token,''))
    
    def AppendToken(self, token: tuple) -> None:
        self.__tokenList.append(token)

    def AddToken(self, index: int, token: tuple) -> None:
        self.__tokenList.insert(index, token)

    def RemoveToken(self, index: int) -> None:
        self.__tokenList.pop(index)
    
    def PrintList(self) -> None:
        for token in self.__tokenList:
            print(f'\nType: {GetTokenDescription(token[0])}\nName: {token[1]}\nProps: {token[2]}')

    def GetProps(self, tag: str) -> dict[str,str]:
        propsList = re.findall(r'\s+[a-zA-Z0-9_]+=[\"|\']\s*[a-zA-Z0-9_;:]*[\"|\']',tag)
        propsDict = {}
        for prop in propsList:
            name = re.search(r'[a-zA-Z0-9_]+=[\"|\']',prop)
            name = '' if name == None else name.group()
            value = re.search(r'=[\"|\'][a-zA-Z0-9_:;]+[\"|\']',prop)
            value = '' if value == None else value.group()
            if name != '':
                name = name[0:len(name)-2]
                value = '' if value == None else value[2:len(value)-1]
                propsDict[name] = value
        return propsDict
    
    
def TreeConstruction(tokenList: list):
    pass

def CreateDOM(html):
    pass

def Parse(html: str):
    tokens = []
    tokenizer = Tokenizer(html)
    tokenizer.PrintList()
