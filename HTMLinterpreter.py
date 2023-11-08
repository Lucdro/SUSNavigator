import re
#
TOKENSDESCRIPTION = {
    ('word-element',1),
    ('tagStart-element',2),
    ('tagEnd-element',3),
    ('javascript-element',4),
}
def GetTokenDescription(value: int) -> str:
    for description in TOKENSDESCRIPTION:
        if description[1] == value:
            return description[0] 
    return -1
def GetTokenValue(name: str) -> int:
    for description in TOKENSDESCRIPTION:
        if description[0] == name:
            return description[1] 
    return -1
    
#   Other tags will be converted to div
RECOGNIZEDTAGS = {
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
}
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
    tokenList = []

    def __init__(self , html: str) -> None:
        self.inputStream = html.strip()
        self.GenerateTokenList()
        
    def GenerateTokenList(self) -> None:
        index = 0
        tokenDescWord = GetTokenValue('word-element')
        tokenDescTagStart = GetTokenValue('tagStart-element')
        tokenDescTagEnd = GetTokenValue('tagEnd-element')
        
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
                tokenName = re.search(r'</?[a-zA-Z0-9_]+',token).group()
                tokenName += '>'
                props = Token.GetProps(token)
                self.tokenList.append((tokenType,tokenName,props))
                index += 1
                continue
            #search the next tag to end the word
            index +=1
            while(index < len(self.inputStream)):
                    if self.inputStream[index] == '<':
                        break
                    token += self.inputStream[index]
                    index += 1
            self.tokenList.append((tokenDescWord,token,''))
    
    def AddToken(index: int, element :str):
        pass

    def RemoveToken(index: int):
        pass
    
    def PrintList(self) -> None:
        for token in self.tokenList:
            print(f'\nType: {GetTokenDescription(token[0])}\nName: {token[1]}\nProps: {token[2]}')

class Token:
    def GetProps(tag: str) -> dict:
        propsList = re.findall(r'\s+[a-zA-Z0-9_]+=[\"|\']\s*[a-zA-Z0-9_;:]*[\"|\']',tag)
        propsDict = {}
        for prop in propsList:
            prop = prop.strip()
            name = re.search(r'[a-zA-Z0-9_]+=[\"|\']',prop).group()
            value = re.search(r'=[\"|\'][a-zA-Z0-9_:;]+[\"|\']',prop).group()
            if name != None:
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
