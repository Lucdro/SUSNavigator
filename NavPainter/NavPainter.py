from turtle import width
from typing import Any, Self

class NavPainter:
    __defaultImg = 'no-image.svg'
    __dom : dict[str,Any]

    def __init__(self , dom: dict[str,Any]) -> None:
        self.__dom = dom

    def DrawDom(self) -> None:
        self.DrawObj(self.__dom,0,0)

    def DrawObj(self, obj: dict[str,Any], x: int, y: int) -> None:
        objValue: str = obj.get('value','ValueNotFound')
        objStyle: dict[str, str] = obj.get('style', {})
        objChilds: list[dict[str,Any]]  = obj.get('childs',[])

        heigth:int
        width:int
        if objValue == '<img>':
            width,heigth = self.DrawImg(objStyle, x, y)

    def DrawImg(self, style: dict[str,str], x: int, y: int) -> tuple[int,int]:
        """
        Draws a img\n
        Return width, heigth
        """
        return 1,2

    def DrawTag(self) -> None:
        pass

    def DrawText(self) -> None:
        pass
