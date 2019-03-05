DOCSTRING = """'''
This is a docstring

can be multiline

!!! note
    contain Markdown and such

![](http://image.com/something.jpg)'''"""


CLASS_0 = """
class MaClasse(object):
    pass 
"""

CLASS_1 = """
class MaClasse(object):
    '''Doctstring here
    dont mind me
    '''
    pass 
"""

CLASS_2a = """
class MaClasse(object):
    '''Doctstring here
    dont mind me
    '''
    
    def __init__(self):
        self.a = None 
"""


CLASS_2b = """
class MaClasse(object):
    def __init__(self):
        '''Doctstring here
        dont mind me
        '''
        self.a = None 
"""


CLASS_3 = """
class MaClasse(object):
    '''Doctstring here
    dont mind me
    '''
    
    def __init__(self):
        self.a = None
        
    def some_method(self):
        print('coucou') 
"""

CLASSES = (CLASS_0, CLASS_1, CLASS_2a, CLASS_2b, CLASS_3)
