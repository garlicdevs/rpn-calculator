import colorama

from tokens import RpnTokens
import pandas as pd
from tabulate import tabulate
from pyfiglet import Figlet
from colorama import Fore, Back
colorama.init()


class Print(object):
    def __init__(self):
        self.colors = {
            'black': Fore.BLACK,
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
        }
        self.reset = Fore.RESET
        self.bg_colors = {
            'black': Back.BLACK,
            'red': Back.RED,
            'green': Back.GREEN,
            'yellow': Back.YELLOW,
            'blue': Back.BLUE,
            'magenta': Back.MAGENTA,
            'cyan': Back.CYAN,
            'white': Back.WHITE,
        }
        self.limit = 10
        self.precision = 10
        self.mode = 'dec'
        self.display = 'horizontal'
        self.fig = Figlet()
        self.theme = 1

    def toggle_theme(self):
        if self.theme == 0:
            self.theme = 1
        else:
            self.theme = 0

    def toggle_display(self):
        if self.display == 'horizontal':
            self.display = 'vertical'
        else:
            self.display = 'horizontal'

    def welcome(self):
        if self.theme:
            print(self.colors['yellow'])
        print(self.fig.renderText('RPN CALCULATOR'))
        print('Author: Duy Nguyen')
        print('Email: garlicdevs@gmail.com\n\n')
        if self.theme:
            print('Type' + self.colors['cyan'] + ' help ' + self.colors['yellow'] + 'for a list of commands ..')
        else:
            print('Type help for a list of commands ..')

    def help(self):
        messages = {
            'Arithmetic Operators': [
                RpnTokens.ADD,
                RpnTokens.SUBTRACT,
                RpnTokens.MULTIPLY,
                RpnTokens.DIVIDE,
                RpnTokens.CLEAR_ALL,
                RpnTokens.CLEAR_STACK,
                RpnTokens.CLEAR_VAR,
                RpnTokens.MODULUS,
                RpnTokens.INCREMENT,
                RpnTokens.DECREMENT,
            ],
            'Bitwise Operators': [
                RpnTokens.BIT_AND,
                RpnTokens.BIT_OR,
                RpnTokens.BIT_XOR,
                RpnTokens.BIT_NOT,
                RpnTokens.BIT_SHIFT_LEFT,
                RpnTokens.BIT_SHIFT_RIGHT,
            ],
            'Boolean Operators': [
                RpnTokens.BOOLEAN_NOT,
                RpnTokens.BOOLEAN_AND,
                RpnTokens.BOOLEAN_OR,
                RpnTokens.BOOLEAN_XOR,
            ],
            'Comparison Operators': [
                RpnTokens.NOT_EQUAL,
                RpnTokens.LESS_THAN,
                RpnTokens.LESS_THAN_OR_EQUAL,
                RpnTokens.EQUAL,
                RpnTokens.GREATER_THAN,
                RpnTokens.GREATER_THAN_OR_EQUAL,
            ],
            'Trigonometric Functions': [
                RpnTokens.ACOS,
                RpnTokens.ASIN,
                RpnTokens.ATAN,
                RpnTokens.COS,
                RpnTokens.COSH,
                RpnTokens.SIN,
                RpnTokens.SINH,
                RpnTokens.TANH,
            ],
            'Numeric Utilities': [
                RpnTokens.CEIL,
                RpnTokens.FLOOR,
                RpnTokens.ROUND,
                RpnTokens.IP,
                RpnTokens.FP,
                RpnTokens.SIGN,
                RpnTokens.ABS,
                RpnTokens.MAX,
                RpnTokens.MIN,
            ],
            'Display Modes': [
                RpnTokens.HEX,
                RpnTokens.DEC,
                RpnTokens.BIN,
                RpnTokens.OCT,
            ],
            'Constants': [
                RpnTokens.E,
                RpnTokens.PI,
                RpnTokens.RAND,
            ],
            'Mathematics Functions': [
                RpnTokens.EXP,
                RpnTokens.FACT,
                RpnTokens.SQRT,
                RpnTokens.LN,
                RpnTokens.LOG,
                RpnTokens.POW,
            ],
            'Networking': [
                RpnTokens.HNL,
                RpnTokens.HNS,
                RpnTokens.NHL,
                RpnTokens.NHS,
            ],
            'Stack Manipulation': [
                RpnTokens.PICK,
                RpnTokens.REPEAT,
                RpnTokens.DEPTH,
                RpnTokens.DROP,
                RpnTokens.DROPN,
                RpnTokens.DUP,
                RpnTokens.DUPN,
                RpnTokens.ROLL,
                RpnTokens.ROLLD,
                RpnTokens.STACK,
                RpnTokens.SWAP,
            ],
            'Macros and Variables': [
                RpnTokens.MACRO,
                RpnTokens.X_EQUAL,
            ],
            'Others': [
                RpnTokens.HELP,
                RpnTokens.EXIT,
                RpnTokens.LIMIT,
                RpnTokens.PREC,
                RpnTokens.THEME
            ],
        }
        index = 1
        for cat in messages:
            df = pd.DataFrame(messages[cat], columns=['Command', 'Description'])
            if self.theme:
                print(self.colors['yellow'])
            print('{}. {}'.format(index, cat.upper()))
            print(tabulate(df, showindex=False, tablefmt='rst', headers=['Command', 'Description']))
            index += 1

    def change_mode(self, mode, stack, variables):
        if mode != self.mode:
            if mode == 'hex' or mode == 'bin' or mode == 'oct':
                while True:
                    if self.theme:
                        print(self.colors['yellow'], 'This mode can only work with integers, '
                              'decimal numbers will be rounded, are you sure? (Yes|No): ', end='')
                    else:
                        print('This mode can only work with integers, '
                              'decimal numbers will be rounded, are you sure? (Yes|No): ',
                              end='')
                    r = str(input()).lower()
                    if r == 'y' or r == 'yes':
                        self.mode = mode
                        for i in range(len(stack)):
                            stack[i] = int(round(stack[i]))
                        for i in range(len(variables)):
                            variables[i] = int(round(variables[i]))
                        return
                    elif r == 'n' or r == 'no':
                        return
            else:
                self.mode = mode

    def wait(self, stack, variables):
        f = '{:.' + str(self.precision) + 'g}'
        var_str = []
        if len(variables) > 0:
            for v in variables:
                if self.mode == 'hex':
                    s = int(round(variables[v]))
                    w = v + ' = ' + hex(s).rstrip("L")
                    var_str.append(w)
                elif self.mode == 'oct':
                    s = int(round(variables[v]))
                    w = v + ' = ' + oct(s).rstrip("L")
                    var_str.append(w)
                elif self.mode == 'bin':
                    s = int(round(variables[v]))
                    w = v + ' = ' + bin(s).rstrip("L")
                    var_str.append(w)
                else:
                    if isinstance(variables[v], float):
                        var_str.append(v + ' = ' + f.format(variables[v]))
                    else:
                        var_str.append(v + ' = ' + str(variables[v]))
        var_str = '\n'.join(var_str)
        if len(var_str) == 0:
            var_str = ''
        else:
            var_str = '\n' + var_str + '\n'
        stack_str = []
        for s in stack:
            if self.mode == 'hex':
                s = int(round(s))
                stack_str.append(hex(s).rstrip("L"))
            elif self.mode == 'oct':
                s = int(round(s))
                stack_str.append(oct(s).rstrip("L"))
            elif self.mode == 'bin':
                s = int(round(s))
                stack_str.append(bin(s).rstrip("L"))
            else:
                if isinstance(s, float):
                    stack_str.append(f.format(s))
                else:
                    stack_str.append(str(s))
        if self.display == 'vertical':
            for i in range(len(stack_str)):
                stack_str[i] = stack_str[i] + '\n'
        if self.limit >= len(stack) > 0:
            if self.display == 'vertical':
                str_ = ' '.join(stack_str)
                str_ = '\n ' + str_
            else:
                str_ = ' '.join(stack_str)
        elif len(stack) == 0:
            str_ = ''
        else:
            if self.display == 'vertical':
                str_ = '..\n' + ' '.join(stack_str[-self.limit:])
            else:
                str_ = '.. ' + ' '.join(stack_str[-self.limit:])
        if self.theme:
            if var_str != '':
                print(self.colors['cyan'] + '[',
                      self.colors['red'] + str_,
                      self.colors['cyan'] + ']',
                      self.colors['red'] + var_str,
                      self.colors['yellow'] + '>',
                      self.reset, end='')
            else:
                print(self.colors['cyan'] + '[',
                      self.colors['red'] + str_,
                      self.colors['cyan'] + ']',
                      self.colors['yellow'] + '>',
                      self.reset, end='')
        else:
            if var_str != '':
                print('[',
                      str_,
                      ']',
                      var_str,
                      '> ', end='')
            else:
                print('[',
                      str_,
                      ']',
                      '> ',
                      end='')

    def error(self, error):
        errors = error.split(' ')
        if self.theme:
            print(self.colors['red'] + '(*) ' + errors[0] + self.reset,
                  self.colors['yellow'] + ' '.join(errors[1:]))
        else:
            print('(*) ' + errors[0] + self.reset,
                  ' '.join(errors[1:]))

    def bye(self):
        if self.theme:
            print(self.colors['green'], 'Bye')
        else:
            print('Bye')
