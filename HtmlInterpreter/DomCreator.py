from ast import parse
from HtmlInterpreter.Tree import Tree
import HtmlInterpreter.TokenDescription as TokenDescription
from typing import Any, Self
import re

class DomCreator:
    __defaultProps: dict[str, dict[str, str]] = {
        'caracter' : {
        },
        'root' : {
            'width':'auto',
            'height':'auto',
            'color':'000000',
            'font-size':'16px',
            'background':'ffffff',
            'border':'5px',
            'margin':'5px',
        },
        '<div>' : {
            'width':'auto',
            'height':'auto',
            'color':'000000',
            'font-size':'16px',
            'background':'ffffff',
            'border':'5px',
            'margin':'5px',
        },
    }
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

    def CreateObj(self, tree: Tree) -> dict[str,Any]:
        treeProps = tree.GetProps()
        #Handle Style
        style = self.GetDefaultStyle(tree.GetType(), tree.GetValue())
        treestyle = self.ParseStyle(treeProps.get('style', ''))
        self.UpdateStyle(style,treestyle)

        #Handle Childs
        childs: list[dict[str,Any]] = []
        for child in tree.GetChilds():
            childs.append(self.CreateObj(child))

        obj:dict[str,Any] = {
            'value' : tree.GetValue(),
            'type' : tree.GetType(),
            'style' : style,
            'childs' : childs,
            'src' : treeProps.get('src', ''),
        }

        return obj

    def GetDefaultStyle(self, type: int, value: str) -> dict[str,str]:
        if type == TokenDescription.GetTokenValue('caracter'):
            return self.__defaultProps['caracter']
        else:
            return self.__defaultProps.get(value, self.__defaultProps.get('<div>',{}))
            
    
    def ParseStyle(self, style: str) -> dict[str,str]:
        props: list[str] = re.findall(r'[a-zA-Z0-9_]+:[a-zA-Z0-9_]+',style)
        parsed = {}
        for prop in props:
            temp = prop.split(':')
            parsed[temp[0]] = temp[1]
        return parsed

    def UpdateStyle(self, old: dict[str,str], new: dict[str,str]):
        for prop in old.keys():
            temp = new.get(prop)
            if temp != None:
                old[prop] = temp

    def PrintDom(self, dom: dict[str,Any] | None = None) -> None:
        if dom == None:
            dom = self.__domObj
        self.__PrintObj(dom, '')
    
    def __PrintObj(self, obj: dict[str,Any], tabs: str) -> None:
        objValue: str = obj.get('value','ValueNotFound')
        objStyle: dict[str, str] = obj.get('style', {})
        objChilds: list[dict[str,Any]]  = obj.get('childs',[])

        tabs += self.__hierarchySpacing

        style: str = ''
        if  len(objStyle) > 0:
            for key, value  in objStyle.items():
                style += f'\n{tabs}{self.__childsSpacing*2}{key} = {value}'
        else:
            style = f'\n{tabs}{self.__childsSpacing*2}None'

        print(f"{tabs}{objValue}:\n{tabs}{self.__childsSpacing}style:{style}")
        
        if objChilds == []:
            print(f"{tabs}{self.__childsSpacing}childs:\n{tabs}{self.__childsSpacing*2}None")
        else:
            print(f"{tabs}{self.__childsSpacing}childs:{len(objChilds)}\n")
            for child in objChilds:
                self.__PrintObj(child , tabs)
