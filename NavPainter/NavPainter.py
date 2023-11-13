import os
import string
from tkinter import font
from typing import Any, Self
import HtmlInterpreter.TokenDescription as TokenDescription
import pygame

class NavPainter:
    __defaultImg = 'no-image.svg'
    __root = {
    }
    __dom : dict[str,Any]
    __caracterTokenValue: int = TokenDescription.GetTokenValue('character')
    __defaultFontsize = '16px'
    __defaultBgColor: str = 'f6f6f6'
    __defaultColor: str = '101010'
    __backGroundColor: pygame.Color
    __fps: int
    __vh: int
    __vw: int
    __screen: pygame.Surface
    __transparent: pygame.Color = pygame.Color(246, 246, 246,0)
    __definedColors: dict[str,pygame.Color]={
        'red':pygame.Color(184, 22, 22),
        'green':pygame.Color(22,184,22),
        'blue':pygame.Color(22, 22, 184),
        'white':pygame.Color(230,230,230),
        'black':pygame.Color(22,22,22),
    }
    def __init__(self , dom: dict[str,Any], vw: int = 1280, vh: int = 720, fps: int = 60, bgColor: pygame.Color|None = None) -> None:
        self.__dom = dom
        self.__vw = vw
        self.__vh = vh
        self.__fps = fps
        if bgColor == None:
            self.__backGroundColor = pygame.Color(246, 246, 246)
        else:
            self.__backGroundColor = bgColor

    def Start(self) -> None:
        pygame.init()
        self.__screen = pygame.display.set_mode((self.__vw, self.__vh),pygame.SRCALPHA)
        clock = pygame.time.Clock()

        running = True
        while(running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__screen.fill(self.__backGroundColor)
            self.DrawDom()
            pygame.display.flip()
            clock.tick(self.__fps)
            #running = False
        pygame.quit()

    def DrawDom(self) -> None:
        self.DrawObj(self.__dom,0,0,{})

    def DrawObj(self, obj: dict[str,Any], x: int, y: int, lastStyle: dict[str,str]) -> tuple[int,int]:
        """
        Return width, height
        """
        objValue: str = obj.get('value','ValueNotFound')
        if objValue == '<head>':
            return 0,0
        
        objStyle: dict[str, str] = obj.get('style', {})
        id: str = obj.get('id', '')
        objChilds: list[dict[str,Any]]  = obj.get('childs',[])
        objType: str = obj.get('type','Not found')

        self.UpdateStyle(lastStyle,objStyle)

        fontsize = self.ConvertToPixels(lastStyle.get('font-size', self.__defaultFontsize))
        if objValue == 'root':
            self.__root['fontsize'] = fontsize

        objBackgroundColor: pygame.Color|None = self.ConvertToColor(objStyle.get('background',lastStyle.get('background','')))

        objPadding: int = self.ConvertToPixels(objStyle.get('padding','0'),fontsize)
        objMargin: int = self.ConvertToPixels(objStyle.get('margin','0'),fontsize)

        objWidth: int = self.ConvertToPixels(objStyle.get('width','0'),fontsize) 
        objHeight: int = self.ConvertToPixels(objStyle.get('height','0'),fontsize)
        objBorder:str = objStyle.get('border','')
        borderparams = objBorder.split(' ')
        borderSize: int = 0
        borderColor:pygame.Color|None = self.__transparent
        if len(borderparams) > 1:
            borderSize = self.ConvertToPixels(borderparams[0],fontsize)
            borderColor = self.ConvertToColor(borderparams[1])

        if not objType == self.__caracterTokenValue:
            if borderColor != None:
                self.DrawBackground(
                    x+objMargin,
                    y+objMargin,
                    objWidth,
                    objHeight,
                    borderColor
                    )
            if objBackgroundColor != None:
                self.DrawBackground(
                    x+objMargin+borderSize,
                    y+objMargin+borderSize,
                    objWidth - 2*borderSize,
                    objHeight - 2*borderSize,
                    objBackgroundColor
                    )

        objWidth += objMargin + objMargin + objPadding
        objHeight += objMargin + objMargin + objPadding
    
        totalWidth:int = objMargin
        totalHeight:int = objMargin
        #If has childs draw them, else draw itself
        if len(objChilds) > 0:
            #Draws Childs
            totalWidth += objPadding
            totalHeight += objPadding  
            for child in objChilds:
                childX,childY = self.DrawObj(child, x + totalWidth + borderSize, y + totalHeight + borderSize, lastStyle)
                #totalWidth += childX
                totalHeight += childY
            objPadding += objPadding
            objPadding += objPadding  
        else:
            #Draws himself
            
            if objType == self.__caracterTokenValue:
                self.DrawText(objValue,x,y,lastStyle, fontsize)
            if objValue == '<img>':
                self.DrawImg(objStyle, x, y, lastStyle)
        #Returns the space he used
        x += totalWidth + objMargin
        y += totalHeight + objMargin
        return objWidth, objHeight
    
    def ConvertToPixels(self, inp: str, fontsize: int = 0) -> int:
        num = inp.split(';')
        pixels: float = 0
        for n in num:        
            if n.isnumeric():
                pixels += float(n)
            elif 'px' in n:
                pixels += float(n[0:len(n)-2])
            elif 'rem' in n:
                pixels += float(n[0:len(n)-3]) * float(self.__root.get('fontsize', fontsize))
            elif 'em' in n:
                pixels += fontsize * float(n[0:len(n)-2])
            elif '%' in n:
                temp = n.split('%')
                #temp[0] = temp[0][0:len(temp[0])-1]
                qt: float = float(temp[0]) if len(temp[0]) > 0 else 0 
                unit = temp[1] 
                 
                if unit == 'vh':
                    pixels += float(self.__vh / 100 * qt)
                if unit == 'vw':
                    pixels += float(self.__vw / 100 * qt)
                else:
                    smaller = self.__vw if self.__vw < self.__vh else self.__vh
                    pixels += float(smaller / 100 * qt)
            elif 'vw' in n:
                pixels += int(float(n[0:len(n)-2]) * self.__vw)
            elif 'vh' in n:
                pixels += float(float(n[0:len(n)-2]) * self.__vh)
        return int(pixels) 
    
    def ConvertToColor(self, inp: str) -> pygame.Color | None:
        if inp.strip() == '':
            return self.__transparent
        if not all(c in string.hexdigits for c in inp):
            return self.GetColorByName(inp)
        if len(inp) < 3:
            return self.__transparent
        if len(inp) < 6:
            temp = inp[0:3]
            for c in temp:
                inp += c+c
        
        return pygame.Color(int(inp[0:2],16),int(inp[2:4],16),int(inp[4:6],16))
    
    def GetColorByName(self, color:str) -> pygame.Color | None:
        color = color.lower().strip()
        for name, value in self.__definedColors.items():
            if name == color:
                return value
        return None

    def DrawImg(self, style: dict[str,str], x: int, y: int, lastStyle: dict[str,str]) -> None:
        """
        Draws a img\n
        Return width, height
        """
        pass

    def DrawText(self, text: str, x: int, y: int, lastStyle: dict[str,str] , fontsize: int) -> None:
        font = lastStyle.get('font','')
        objFont: pygame.font.Font
        if os.path.exists(font):
            objFont = pygame.font.Font(font, fontsize)
        else:
            objFont = pygame.font.Font(None, fontsize)
        color = self.ConvertToColor(lastStyle.get('color',self.__defaultColor))
            
        renderer: pygame.Surface
        for s in text.split('\n'):
            if color == None:
                continue
            renderer = objFont.render(s,True,color)
            self.__screen.blit(renderer,(x,y))
            renderer = objFont.render('',True, pygame.Color(0,0,0,0))
            self.__screen.blit(renderer,(x,y))

    def DrawTag(self) -> None:
        pass

    def DrawBackground(self, x: int, y: int, l: int, a: int, color: pygame.Color) -> None:
        pygame.draw.rect(self.__screen, color,(x, y, l, a))

    def UpdateStyle(self, old: dict[str,str], new: dict[str,str]):
        for prop, value in new.items():
            old[prop] = value
