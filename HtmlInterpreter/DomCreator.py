from ast import parse
from turtle import width
from HtmlInterpreter.Tree import Tree
import HtmlInterpreter.TokenDescription as TokenDescription
from typing import Any, Self
import re

class DomCreator:
    __defaultProps: dict[str, dict[str, str]] = {
        'caracter' : {
            'width':'0',
            'height':'0',
        },
        'root' : {
            'width':'',
            'height':'',
            'color':'f6f6f6',
            'font':'',
            'font-size':'24px',
            'background':'f6f6f6',
            'border':'0',
            'margin':'5%',
            'padding':'0',
        },
        '<div>' : {
            'width':'',
            'height':'',
            'color':'101010',
            'font':'',
            'font-size':'5%',
            'background':'',
            'border':'0',
            'margin':'5%',
            'padding':'0',
        },
        '<h1>' : {
            'width':'',
            'height':'',
            'color':'101010',
            'font':'48px',
            'font-size':'5%',
            'background':'',
            'border':'0',
            'margin':'5%',
            'padding':'0',
        },
        '<h2>' : {
            'width':'',
            'height':'',
            'color':'101010',
            'font':'36px',
            'font-size':'5%',
            'background':'',
            'border':'0',
            'margin':'5%',
            'padding':'0',
        },
        '<h3>' : {
            'width':'',
            'height':'',
            'color':'101010',
            'font':'24px',
            'font-size':'5%',
            'background':'',
            'border':'0',
            'margin':'5%',
            'padding':'0',
        },
        '<h4>' : {
            'width':'',
            'height':'',
            'color':'101010',
            'font':'18px',
            'font-size':'5%',
            'background':'',
            'border':'0',
            'margin':'5%',
            'padding':'0',
        },
        '<h5>' : {
            'width':'',
            'height':'',
            'color':'101010',
            'font':'12px',
            'font-size':'5%',
            'background':'',
            'border':'0',
            'margin':'5%',
            'padding':'0',
        },
        '<h6>' : {
            'width':'',
            'height':'',
            'color':'101010',
            'font':'6px',
            'font-size':'5%',
            'background':'',
            'border':'0',
            'margin':'5%',
            'padding':'0',
        },
        '<p>' : {
            'width':'',
            'height':'',
            'color':'101010',
            'font':'',
            'font-size':'1rem',
            'background':'',
            'border':'',
            'margin':'0',
            'padding':'10',
        },
    }
    __caracterTokenValue: int = TokenDescription.GetTokenValue('character')
    __domObj: dict[str,Any]
    __tree: Tree
    __childsSpacing: str = '   '
    __hierarchySpacing: str = '\t\t'

    def __init__(self, tree: Tree) -> None:
        self.__tree = tree

    def ChangeTree(self, tree: Tree) -> dict[str,Any]:
        self.__tree = tree
        return self.CreateDOM()

    def CreateDOM(self, tree: Tree | None = None) -> dict[str,Any]:
        if tree == None:
            self.__domObj = self.CreateObj(self.__tree)
            return self.__domObj
        
        return self.CreateObj(tree)
    
    def GetDOMObj(self) -> dict[str,Any]:
        return self.__domObj

    def CreateObj(self, tree: Tree, head: bool = False) -> dict[str,Any]:
        treeProps = tree.GetProps()
        #Handle Style
        type = TokenDescription.GetTokenDescription(tree.GetType())
        style = {}
        if tree.GetValue() == '<head>':
            head = True
        if not head:    
            style = self.GetDefaultStyle(tree.GetType(), tree.GetValue())
            treestyle = self.ParseStyle(treeProps.pop('style', ''))
            
            if type == 'character':
                style = {
                'width':f'{len(tree.GetValue())*.7}em',
                'height':f'1em',
                }
            self.UpdateStyle(style,treestyle)
        
        #Handle Childs
        w:str = style.get('width','5').strip(' ') 
        h:str = style.get('height','0').strip(' ')
        childs: list[dict[str,Any]] = []
        for child in tree.GetChilds():
            objChild = self.CreateObj(child, head)
            childs.append(objChild)
            if not head:
                childStyle = objChild.get('style',{})
                if len(w) == 0 :
                    cw:str = childStyle.get('width','0')
                    newW = style.get('width','') 
                    style['width'] = f'{newW};{cw}' 
                if len(h) == 0:
                    ch:str = childStyle.get('height','0')
                    newH = style.get('height','')
                    style['height'] = f'{newH};{ch}' 

        obj:dict[str,Any] = {
            'value' : tree.GetValue(),
            'type' : tree.GetType(),
            'style' : style,
            'childs' : childs,
        }
        src = treeProps.pop('src', '')
        if len(src) > 0:
            obj['src'] = src

        for prop, value in treeProps.items():
            obj[prop] = value

        return obj

    def GetDefaultStyle(self, type: int, value: str) -> dict[str,str]:
        if type == self.__caracterTokenValue:
            return self.__defaultProps['caracter'].copy()
        else:
            return self.__defaultProps.get(value, self.__defaultProps.get('<div>',{})).copy()
            
    
    def ParseStyle(self, style: str) -> dict[str,str]:
        props: list[str] = re.findall(r'[a-zA-Z0-9_]+:[ a-zA-Z0-9_]+',style)
        parsed = {}
        for prop in props:
            temp = prop.split(':')
            parsed[temp[0]] = temp[1]
        return parsed

    def UpdateStyle(self, old: dict[str,str], new: dict[str,str]):
        for prop,value in new.items():
            old[prop] = value

    def PrintDom(self, dom: dict[str,Any] | None = None) -> None:
        if dom == None:
            dom = self.__domObj
        self.__PrintObj(dom, '')
    
    def __PrintObj(self, obj: dict[str,Any], tabs: str) -> None:
        obj = obj.copy()
        objValue: str = obj.pop('value','ValueNotFound')
        objStyle: dict[str, str] = obj.pop('style', {})
        objChilds: list[dict[str,Any]]  = obj.pop('childs',[])
        obj['type'] = TokenDescription.GetTokenDescription(obj.pop('type',-1))
        
        tabs += self.__hierarchySpacing

        style: str = ''
        if  len(objStyle) > 0:
            for key, value  in objStyle.items():
                style += f'\n{tabs}{self.__childsSpacing*2}{key} = {value}'
        else:
            style = f'\n{tabs}{self.__childsSpacing*2}None'

        print(f"{tabs}{objValue}:")
        for prop, value in obj.items():
            print(f"{tabs}{self.__childsSpacing}{prop}: {value}")
        print(f'{tabs}{self.__childsSpacing}style:{style}')

        if objChilds == []:
            print(f"{tabs}{self.__childsSpacing}childs:\n{tabs}{self.__childsSpacing*2}None")
        else:
            print(f"{tabs}{self.__childsSpacing}childs: {len(objChilds)} ->\n")
            for child in objChilds:
                self.__PrintObj(child , tabs)