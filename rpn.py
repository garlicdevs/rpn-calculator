from errors import RpnErrors, StackUnderflowError, IntegerOperationError, DomainError, \
    UnsupportedDecimalError, InvalidSyntaxError
from format import Print
from lexer import RpnLexer
from operations import RpnOperations
from tokens import RpnTokens


class RpnReader(object):
    def __init__(self):
        self._stacks = []
        self._variables = {}
        self._macros = {}
        self._lexer = RpnLexer()
        self._print = Print()

    def _process_tokens(self, tokens):
        try:
            backup_stack = self._stacks.copy()
            backup_vars = self._variables.copy()
            valid, tokens = RpnTokens.check_syntax(tokens)
            if valid:
                for token in tokens:
                    if RpnTokens.contains_space(token):
                        continue
                    if RpnTokens.is_number(token):
                        num = RpnTokens.get_number(token, self._print.precision)
                        if num is not None:
                            if self._print.mode == 'dec':
                                self._stacks.append(num)
                            else:
                                if isinstance(num, float):
                                    raise UnsupportedDecimalError(token)
                                else:
                                    self._stacks.append(num)
                    elif RpnTokens.is_keyword(token):
                        if token[1] == RpnTokens.HEX[0]:
                            self._print.change_mode('hex', self._stacks, self._variables)
                        elif token[1] == RpnTokens.DEC[0]:
                            self._print.change_mode('dec', self._stacks, self._variables)
                        elif token[1] == RpnTokens.OCT[0]:
                            self._print.change_mode('oct', self._stacks, self._variables)
                        elif token[1] == RpnTokens.BIN[0]:
                            self._print.change_mode('bin', self._stacks, self._variables)
                        elif token[1] == RpnTokens.HELP[0]:
                            self._print.help()
                        elif token[1] == RpnTokens.EXIT[0]:
                            self._print.bye()
                            return 1
                        # Limit showing the number of digits after .
                        elif token[1] == RpnTokens.PREC[0]:
                            if len(self._stacks) < 1:
                                raise StackUnderflowError(token)
                            p = self._stacks.pop()
                            if not isinstance(p, int):
                                raise IntegerOperationError(token)
                            if p <= 0 or p > 100:
                                raise DomainError(token, 1, 100)
                            self._print.precision = p
                        # Limit showing the number of items in stack
                        elif token[1] == RpnTokens.LIMIT[0]:
                            if len(self._stacks) < 1:
                                raise StackUnderflowError(token)
                            p = self._stacks.pop()
                            if not isinstance(p, int):
                                raise IntegerOperationError(token)
                            if p <= 0 or p > 100:
                                raise DomainError(token, 1, 100)
                            self._print.precision = p
                        elif token[1] == RpnTokens.STACK[0]:
                            self._print.toggle_display()
                        elif token[1] == RpnTokens.THEME[0]:
                            self._print.toggle_theme()
                    elif RpnTokens.is_literal(token):
                        if token[1] in self._variables:
                            val = self._variables[token[1]]
                            if self._print.mode == 'dec':
                                self._stacks.append(val)
                            else:
                                if isinstance(val, float):
                                    raise UnsupportedDecimalError(token)
                                else:
                                    self._stacks.append(val)
                        elif token[1] in self._macros:
                            exp = self._macros[token[1]]
                            new_tokens = self._lexer.get_tokens(exp)
                            self._process_tokens(new_tokens)
                        else:
                            raise InvalidSyntaxError(token)
                    else:
                        if token[1].startswith('macro'):
                            cmd_str = token[1].split()
                            if len(cmd_str) <= 2:
                                raise InvalidSyntaxError(token)
                            mc = ' '.join(cmd_str[2:])
                            self._macros[cmd_str[1]] = mc
                        else:
                            ret = RpnOperations.execute(token, self._stacks, self._variables, self._print.mode)
                            if ret is not None:
                                self._stacks.append(ret)
        except RpnErrors as e:
            # Rollback to previous backup data if errors occur
            self._stacks = backup_stack
            self._variables = backup_vars
            self._print.error(e.get_message())
        return 0

    def process(self):
        self._print.welcome()
        while True:
            self._print.wait(self._stacks, self._variables)
            line_str = str(input())
            tokens = self._lexer.get_tokens(line_str)
            ret = self._process_tokens(tokens)
            if ret:
                break


if __name__ == '__main__':
    RpnReader().process()
