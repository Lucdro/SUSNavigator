from HtmlInterpreter.Interpreter import Interpreter 
from NavPainter.NavPainter import NavPainter
interpreter = Interpreter()

dom = interpreter.Parse('<html><head> <title> Compiladores </title> </head><body> <p style="color:red;background:blue;" id="abc"> Unipinhal </p> <br> </body></html>')

#dom.PrintDom()

painter = NavPainter(dom.GetDOMObj())

while(True):
    painter.DrawDom()