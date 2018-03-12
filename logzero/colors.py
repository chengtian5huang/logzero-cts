"""
Source: https://github.com/tartley/colorama/blob/master/colorama/ansi.py
Copyright: Jonathan Hartley 2013. BSD 3-Clause license.
"""

CSI = '\033['
OSC = '\033]'
BEL = '\007'


def codes_to_chars(*code):
    """this one can recive multi codes to set foreground and background """
    """at the same time"""
    assert 0 < len(code) <= 2, '\033[91m accept one or two colors! \033[0m'
    back_clr, fore_clr = sorted(code)

    return CSI + str(code) + 'm'

def code_to_chars(code):
    """this one can recive multi codes to set foreground and background """
    """at the same time"""
    return CSI + str(code) + 'm'

def set_title(title):
    return OSC + '2;' + title + BEL


def clear_screen(mode=2):
    return CSI + str(mode) + 'J'


def clear_line(mode=2):
    return CSI + str(mode) + 'K'


class AnsiCodes(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))
### define an __add__ here! when adding to colors
### return somthing like \033[95;104m
### maybe we need a color class!
### or find a way to hook out the numbers.
    def __add__(self, other):
        print(self, other)

class AnsiCursor(object):
    def UP(self, n=1):
        return CSI + str(n) + 'A'

    def DOWN(self, n=1):
        return CSI + str(n) + 'B'

    def FORWARD(self, n=1):
        return CSI + str(n) + 'C'

    def BACK(self, n=1):
        return CSI + str(n) + 'D'

    def POS(self, x=1, y=1):
        return CSI + str(y) + ';' + str(x) + 'H'


class AnsiFore(AnsiCodes):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 90
    LIGHTRED_EX = 91
    LIGHTGREEN_EX = 92
    LIGHTYELLOW_EX = 93
    LIGHTBLUE_EX = 94
    LIGHTMAGENTA_EX = 95
    LIGHTCYAN_EX = 96
    LIGHTWHITE_EX = 97


class AnsiBack(AnsiCodes):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 100
    LIGHTRED_EX = 101
    LIGHTGREEN_EX = 102
    LIGHTYELLOW_EX = 103
    LIGHTBLUE_EX = 104
    LIGHTMAGENTA_EX = 105
    LIGHTCYAN_EX = 106
    LIGHTWHITE_EX = 107


class AnsiStyle(AnsiCodes):
    BRIGHT = 1
    DIM = 2
    NORMAL = 22
    RESET_ALL = 0


Fore = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()
Cursor = AnsiCursor()

if __name__ == "__main__":
    from colorama import init as colorama_init
    #colorama_init()

    fore_clr_names = list(AnsiFore.__dict__)[3:-1]
    back_clr_names = list(AnsiBack.__dict__)[3:-1]
    ans = Fore.BLACK + Back.LIGHTWHITE_EX
    print(ans, '\033[30;107m')
    #print(code_to_chars(104,95, 6)+'TEST'+ code_to_chars(0))
    print('\033[41;32m something here \033[0m')
    print('\033[101;92m something here \033[0m')
    print('\033[95;104m something here \033[0m')
    '''
    for clr_name in fore_clr_names:
        clr_code = getattr(AnsiFore, clr_name)
        print(code_to_chars(clr_code)+clr_name+code_to_chars(39))

    for clr_name in back_clr_names:
        clr_code = getattr(AnsiBack, clr_name)
        print(code_to_chars(clr_code)+clr_name+code_to_chars(39))
    '''