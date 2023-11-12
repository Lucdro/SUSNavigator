TOKENSDESCRIPTION = [
    ('root',0),
    ('DOCTYPE',1),
    ('start tag',2),
    ('end tag',3),
    ('comment',4),
    ('character',5),
    ('end-of-file',6),
    ('self closing tag', 7)
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
