from typing import Self

class Tree:
    __root: str
    __type: int
    __props: dict[str,str] | None
    __childs: list[Self]
    __childsSpacing: str = '   '
    __hierarchySpacing: str = '\t\t'
    def __init__(self, value: str, type: int, childs: list[Self] = [], props: dict[str,str] | None = None) -> None:
        self.__root = value
        self.__type = type
        self.__props = props
        self.__childs = childs

    def AppendChild(self, child: Self) -> Self:
        self.__childs.append(child)
        return child
    
    def GetType(self) -> int:
        return self.__type

    def GetChilds(self) -> list[Self]:
        return self.__childs
    
    def GetProps(self) -> dict[str,str]:
        return self.__props if self.__props != None else {} 

    def Print(self, tabs: str = '') -> None:
        tabs += self.__hierarchySpacing

        props: str = ''
        if self.__props != None and len(self.__props) > 0:
            for key, value  in self.__props.items():
                props += f'\n{tabs}{self.__childsSpacing*2}{key} = {value}'
        else:
            props = f'\n{tabs}{self.__childsSpacing*2}None'

        print(f"{tabs}{self.__root}:\n{tabs}{self.__childsSpacing}props:{props}")
        
        if self.__childs == []:
            print(f"{tabs}{self.__childsSpacing}childs:\n{tabs}{self.__childsSpacing*2}None")
        else:
            print(f"{tabs}{self.__childsSpacing}childs:{len(self.__childs)}\n")
            for child in self.__childs:
                child.Print(tabs)

    def GetDeep(self, deep: int = 0) -> int:
        if self.__childs == []:
             return deep
        deepsest: int = deep
        for child in self.__childs:
            childdeep = child.GetDeep(deep+1)
            deepsest = deepsest if deepsest > childdeep else childdeep
        return deepsest
    
    def __str__(self):
        childsValue = ''
        if len(self.__childs) > 0:
            i = 1 
            for child in self.__childs:
                childsValue += f'  {i}: {child.__root}'
                i += 1 
        return f'Value: {self.__root} Childs: {childsValue}'
    
    def GetValue(self) -> str:
        return self.__root
    
    def SteppedPrint(self,tabs) -> None:
        print(f'Value:{self.__root}')
        print(f'Props:{self.__props}')
        print('Childs:')
        for child in self.__childs:
            input()
            child.SteppedPrint(tabs)
        # tabs += '\t'

        # props: str = ''
        # if self.__props != None:
        #     for key, value  in self.__props.items():
        #         props += f'\n{tabs}{self.__hierarchySpacing*2}{key} = {value}'
        # else:
        #     props = f'\n{tabs}{self.__hierarchySpacing*2}None'

        # print(f"{tabs}{self.__root}:\n{tabs}{self.__hierarchySpacing}props:{props}")
        
        # print(f"{tabs}{self.__hierarchySpacing}childs:")
        # if len(self.__childs) == 0:
        #     print(f"{tabs}{self.__hierarchySpacing*2}None")
        # else:
        #     for child in self.__childs:
        #         input()
        #         child.Print(tabs)

        