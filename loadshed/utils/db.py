import gb
from gb import DebugMode


def estimates(arms, chosen_arm_index):
    if gb.debug_mode is not DebugMode.No:  # print out the current estimates
        s = 'arm {:2}: '.format(chosen_arm_index)
        for arm in arms:
            s += '{:5.1f} '.format(arm.density)
        print(s)


def separator():
    if gb.debug_mode is not DebugMode.No:
        print('--------------------------------------------------------')


def blank_string(s, width):
    s_out = ''
    for i in range(width - len(s)):
        s_out += ' '
    return s_out


def h1(title, subtitle=''):
    if gb.debug_mode is not DebugMode.No:
        w = 80
        s = ''
        for i in range(w):
            s += '-'
        print('')
        print('+{}+'.format(s))
        print('| {}{}|'.format(title, blank_string(title, w - 1)))
        if len(subtitle) > 0:
            print('| {}{}|'.format(subtitle, blank_string(subtitle, w - 1)))
        print('+{}+'.format(s))


def h2(title):
    if gb.debug_mode is not DebugMode.No:
        print('{}'.format(title))


def line(s):
    if gb.debug_mode is not DebugMode.No:
        print(s)


def line_brief(s):
    if gb.debug_mode >= DebugMode.Brief:
        line(s)


def line_detail(s):
    if gb.debug_mode >= DebugMode.Detail:
        line(s)


def line_verydetail(s):
    if gb.debug_mode >= DebugMode.VeryDetail:
        line(s)


def inline(s, is_enter=False):
    """
    Print string s without a "newline" at the end,
    so that the succeeding print will be in the same line
    :param s:
    :param is_enter:
    :return:
    """
    if gb.debug_mode is not DebugMode.No:
        print(s, sep=' ', end = '', flush = True)  # python3
        # sys.stdout.write(s)  # python2
        if is_enter:
            print('')


def inline_brief(s, is_enter=False):
    if gb.debug_mode >= DebugMode.Brief:
        inline(s, is_enter)


def inline_detail(s, is_enter=False):
    if gb.debug_mode >= DebugMode.Detail:
        inline(s, is_enter)


def inline_verydetail(s, is_enter=False):
    if gb.debug_mode >= DebugMode.VeryDetail:
        inline(s, is_enter)
