from HtmlInterpreter.Interpreter import Interpreter 
from NavPainter.NavPainter import NavPainter
interpreter = Interpreter()

dom = interpreter.Parse('''
<html>
    <head>
        <title>replit</title>
    </head>
    <body>
        <p style="border:2px black;background:777777">Hello world</p>
        <h1 style="border:2px black;font-size:30px;background:777777;color:red;">Olá, Eu sou uma página </h1>
        <div id="teste" style="border:2px black;color:black;background:777777">Unipinhal</div>
        <p style="background:777777;margin:20px;border:2px black;">Hello world</p>
    </body>
</html>
                        ''')


painter = NavPainter(dom.GetDOMObj())

painter.Start()