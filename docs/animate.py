from typing import Optional
# from os import system
from time import sleep
from random import randrange


scene = """
xxxxxxxxxx
xxxxxxxxxx
xxxxxxxxxx
xxxxxxxxxx
""".lstrip()

lines = scene.splitlines()

h = len(lines)
w = len(lines[0])


def bkspc():
    """ Alas, ASCII backspace char only works on current line.
    So, cannot overwrite any output prior to newline/linefeed char.
    """
    unscene = '\b' * (len(scene) + 1)
    print(unscene, end='')


def clear():
    """ VT100 terminal control-sequence, e.g. as output by /usr/bin/clear
    Works in PyCharm, but ONLY if applicable Run configuration has enabled
    "emulate terminal in output console" option, which is NOT the default.
    """
    clear_seq = '\033c'
    print(clear_seq, end='')


def t_backspace():
    def t_eol(eol: Optional[str]):
        print(f"eol={repr(eol)}")
        bar = '========== '
        print(bar, end=eol)
        print(bar, end=eol)
        print('\b'*(len(bar)*2-2), end='')
        print(' FOO ', end='')
        print('\n'+'x'*len(bar)*2)
        return

    t_eol('')
    t_eol('\r')
    t_eol('\n')
    t_eol(None)
    t_eol('\r\n')
    return


def mutate() -> False:
    global scene, lines
    tries = 5
    while tries > 0:
        tries -= 1
        x = randrange(w)
        y = randrange(h)
        if lines[y][x] == 'x':
            chars = [c for c in lines[y]]
            chars[x] = '-'
            lines[y] = ''.join(chars)
            scene = ''.join([f"{line}\n" for line in lines])
            return True
    return False


def redraw():
    # XXX alas, no way to overwrite previous lines,
    # XXX only previous chars in current line. :-6
    clear()
    print(scene)


def t_animate():
    clear()
    print(scene)
    contd = 5
    while contd > 0:
        contd -= 1
        mutate()
        sleep(1)
        redraw()


# t_backspace()
t_animate()

print("DONE.")
# END
