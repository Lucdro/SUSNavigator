#   Other tags will be converted to div
RECOGNIZEDTAGS = [
    ('<html>',True),
    ('<head>',True),
    ('<body>',True),
    ('<title>',True),
    ('<p>',True),
    ('<br>',False),
    ('<div>',True),
    ('<h1>',True),
    ('<h2>',True),
    ('<h3>',True),
    ('<h4>',True),
    ('<h5>',True),
    ('<h6>',True),
    ('<span>',True),
    ('<img>',True),
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