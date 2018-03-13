"""
Source: https://github.com/tartley/colorama/blob/master/colorama/ansi.py
Copyright: Jonathan Hartley 2013. BSD 3-Clause license.
"""

CSI = '\033['
OSC = '\033]'
BEL = '\007'

def code_to_chars(code):
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

def simple_test_1():
    """these tests show that we can use fore and back reset both anytime."""
    print(Back.LIGHTGREEN_EX + 'TEST' + Fore.RESET + Back.RESET)
    print(Fore.LIGHTBLUE_EX + 'TEST' + Fore.RESET + Back.RESET)
    print(Fore.LIGHTWHITE_EX + Back.LIGHTBLUE_EX + 'TEST'
          + Fore.RESET + Back.RESET)
    print('without any fancy thing')

def simple_test_2():
    """these tests shows that connect them anyway will work."""
    print('\033[41;32m something here' + Back.RESET + Fore.RESET)
    print('\033[101m\033[92m something here' + Fore.RESET + Back.RESET)
    print('\033[95;104m something here'+ Fore.RESET + Back.RESET)
    print('\033[95m\033[104m something here'+ Fore.RESET + Back.RESET)

def show_all_colors():
    """show all fore,back colors and their combinations"""
    print('#'*48)
    print('#'+' '*46+'#')
    print("# maybe u will see nothing in IDE's console!!! #")
    print('#'+' '*46+'#')
    print('#'*48)

    fore_clr_names = [clr for clr in list(Fore.__dict__.keys())
                          if not clr.startswith('__') and clr != 'RESET']

    back_clr_names = [clr for clr in list(Back.__dict__.keys())
                          if not clr.startswith('__') and clr != 'RESET']

    #show all combinitions as following.
    from itertools import product

    for i, clr_name in enumerate(fore_clr_names, 1):
        clr_code = getattr(Fore, clr_name)
        #remind users this one is black in case he will get confused.
        if clr_name == 'BLACK':
            print(clr_code + Back.WHITE + clr_name + ' this one is black!'
                  + Fore.RESET + Back.RESET)
            continue

        #use blank lines to seperate fore_colors and back's
        if i == len(fore_clr_names):
            print(clr_code + clr_name + Fore.RESET + Back.RESET + '\n\n')
            continue

        print(clr_code + clr_name + Fore.RESET + Back.RESET + '|||', end='')

    for i, clr_name in enumerate(back_clr_names, 1):
        clr_code = getattr(Back, clr_name)

        #use blank lines to seperate back_colors and combinations
        if i == len(back_clr_names):
            print(clr_code + clr_name + Fore.RESET + Back.RESET + '\n\n')
            continue

        print(clr_code + clr_name + Fore.RESET + Back.RESET + '|||', end='')

    for clr_combs in product(fore_clr_names, back_clr_names):
        fore_clr, back_clr = clr_combs

        msg = '{fore} ON {back}'.format(fore=fore_clr, back=back_clr)
        fore_code, back_code = getattr(Fore, fore_clr), getattr(Back, back_clr)

        print(fore_code + back_code + msg + Fore.RESET + Back.RESET + '|||', end='')

if __name__ == "__main__":
    from colorama import init as colorama_init
    colorama_init()
    show_all_colors()
