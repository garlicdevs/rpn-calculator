from errors import StackUnderflowError, IntegerOperationError, OperationExecutionError, UnsupportedError, \
    DomainError, RpnErrors
from tokens import RpnTokens
import math
from functools import partial
import socket
import numpy as np


class RpnOperations(object):
    @staticmethod
    def execute(token, stack, variables, mode):
        if mode != 'dec':
            require_int = True
        else:
            require_int = False
        if token[1] == RpnTokens.ADD[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '+'), 2, require_int)
        elif token[1] == RpnTokens.SUBTRACT[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '-'), 2, require_int)
        elif token[1] == RpnTokens.MULTIPLY[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '*'), 2, require_int)
        elif token[1] == RpnTokens.DIVIDE[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '/', mode=mode), 2,
                                       require_int)

        elif token[1] == RpnTokens.CLEAR_ALL[0]:
            return RpnOperations.clear_all(token, stack, variables)
        elif token[1] == RpnTokens.CLEAR_STACK[0]:
            return RpnOperations.clear_stack(token, stack, variables)
        elif token[1] == RpnTokens.CLEAR_VAR[0]:
            return RpnOperations.clear_var(token, stack, variables)

        elif token[1] == RpnTokens.MODULUS[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '%'), 2, True)
        elif token[1] == RpnTokens.INCREMENT[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '++'), 1, True)
        elif token[1] == RpnTokens.DECREMENT[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '--'), 1, True)

        elif token[1] == RpnTokens.BIT_AND[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '&'), 2, True)
        elif token[1] == RpnTokens.BIT_OR[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '|'), 2, True)
        elif token[1] == RpnTokens.BIT_XOR[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '^'), 2, True)
        elif token[1] == RpnTokens.BIT_NOT[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '~'), 1, True)
        elif token[1] == RpnTokens.BIT_SHIFT_LEFT[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '<<'), 2, True)
        elif token[1] == RpnTokens.BIT_SHIFT_RIGHT[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '>>'), 2, True)

        elif token[1] == RpnTokens.BOOLEAN_NOT[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '!'), 1, True)
        elif token[1] == RpnTokens.BOOLEAN_AND[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '&&'), 2, True)
        elif token[1] == RpnTokens.BOOLEAN_OR[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '||'), 2, True)
        elif token[1] == RpnTokens.BOOLEAN_XOR[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '^^'), 2, True)

        elif token[1] == RpnTokens.NOT_EQUAL[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '!='), 2)
        elif token[1] == RpnTokens.LESS_THAN[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '<'), 2)
        elif token[1] == RpnTokens.EQUAL[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '=='), 2)
        elif token[1] == RpnTokens.LESS_THAN_OR_EQUAL[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '<='), 2)
        elif token[1] == RpnTokens.GREATER_THAN[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '>'), 2)
        elif token[1] == RpnTokens.GREATER_THAN_OR_EQUAL[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, '>='), 2)

        elif token[1] == RpnTokens.ACOS[0]:
            return RpnOperations.apply(token, stack, variables, math.acos, 1, unsupported=require_int)
        elif token[1] == RpnTokens.ASIN[0]:
            return RpnOperations.apply(token, stack, variables, math.asin, 1, unsupported=require_int)
        elif token[1] == RpnTokens.ATAN[0]:
            return RpnOperations.apply(token, stack, variables, math.atan, 1, unsupported=require_int)
        elif token[1] == RpnTokens.COS[0]:
            return RpnOperations.apply(token, stack, variables, math.cos, 1, unsupported=require_int)
        elif token[1] == RpnTokens.COSH[0]:
            return RpnOperations.apply(token, stack, variables, math.cosh, 1, unsupported=require_int)
        elif token[1] == RpnTokens.SIN[0]:
            return RpnOperations.apply(token, stack, variables, math.sin, 1, unsupported=require_int)
        elif token[1] == RpnTokens.SINH[0]:
            return RpnOperations.apply(token, stack, variables, math.sinh, 1, unsupported=require_int)
        elif token[1] == RpnTokens.TANH[0]:
            return RpnOperations.apply(token, stack, variables, math.tanh, 1, unsupported=require_int)

        elif token[1] == RpnTokens.CEIL[0]:
            return RpnOperations.apply(token, stack, variables, math.ceil, 1, unsupported=require_int)
        elif token[1] == RpnTokens.FLOOR[0]:
            return RpnOperations.apply(token, stack, variables, math.floor, 1, unsupported=require_int)
        elif token[1] == RpnTokens.ROUND[0]:
            return RpnOperations.apply(token, stack, variables, round, 1, unsupported=require_int)
        elif token[1] == RpnTokens.IP[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, 'ip', mode=mode),
                                       1, unsupported=require_int)
        elif token[1] == RpnTokens.FP[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, 'fp', mode=mode),
                                       1, unsupported=require_int)

        elif token[1] == RpnTokens.SIGN[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, 'sign', mode=mode), 1)
        elif token[1] == RpnTokens.ABS[0]:
            return RpnOperations.apply(token, stack, variables, abs, 1)
        elif token[1] == RpnTokens.MAX[0]:
            return RpnOperations.apply(token, stack, variables, max, 'all')
        elif token[1] == RpnTokens.MIN[0]:
            return RpnOperations.apply(token, stack, variables, min, 'all')

        elif token[1] == RpnTokens.EXP[0]:
            return RpnOperations.apply(token, stack, variables, math.exp, 1, unsupported=require_int)
        elif token[1] == RpnTokens.FACT[0]:
            return RpnOperations.apply(token, stack, variables, math.factorial, 1, require_int=True)
        elif token[1] == RpnTokens.SQRT[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, 'sqrt', mode=mode),
                                       1, require_int=require_int)
        elif token[1] == RpnTokens.LN[0]:
            return RpnOperations.apply(token, stack, variables, math.log2, 1, unsupported=require_int)
        elif token[1] == RpnTokens.LOG[0]:
            return RpnOperations.apply(token, stack, variables, math.log10, 1, unsupported=require_int)
        elif token[1] == RpnTokens.POW[0]:
            return RpnOperations.apply(token, stack, variables, partial(RpnOperations.operator, 'pow', mode=mode),
                                       2, require_int=require_int)

        elif token[1] == RpnTokens.HNL[0]:
            return RpnOperations.apply(token, stack, variables, socket.htonl, 1, require_int=True)
        elif token[1] == RpnTokens.HNS[0]:
            return RpnOperations.apply(token, stack, variables, socket.htons, 1, require_int=True)
        elif token[1] == RpnTokens.NHL[0]:
            return RpnOperations.apply(token, stack, variables, socket.ntohl, 1, require_int=True)
        elif token[1] == RpnTokens.NHS[0]:
            return RpnOperations.apply(token, stack, variables, socket.ntohs, 1, require_int=True)

        elif token[1] == RpnTokens.PICK[0]:
            return RpnOperations.stack(token, stack, variables, 'pick', 1, require_int=True, mode=mode)
        elif token[1].startswith(RpnTokens.REPEAT[0]):
            return RpnOperations.stack(token, stack, variables, 'repeat', 1, require_int=True, mode=mode)
        elif token[1] == RpnTokens.DEPTH[0]:
            return RpnOperations.stack(token, stack, variables, 'depth', 0, require_int=False, mode=mode)
        elif token[1] == RpnTokens.DROP[0]:
            return RpnOperations.stack(token, stack, variables, 'drop', 0, require_int=False, mode=mode)
        elif token[1] == RpnTokens.DROPN[0]:
            return RpnOperations.stack(token, stack, variables, 'dropn', 1, require_int=True, mode=mode)
        elif token[1] == RpnTokens.DUP[0]:
            return RpnOperations.stack(token, stack, variables, 'dup', 0, require_int=False, mode=mode)
        elif token[1] == RpnTokens.DUPN[0]:
            return RpnOperations.stack(token, stack, variables, 'dupn', 1, require_int=True, mode=mode)
        elif token[1] == RpnTokens.ROLL[0]:
            return RpnOperations.stack(token, stack, variables, 'roll', 1, require_int=True, mode=mode)
        elif token[1] == RpnTokens.ROLLD[0]:
            return RpnOperations.stack(token, stack, variables, 'rolld', 1, require_int=True, mode=mode)
        elif token[1] == RpnTokens.SWAP[0]:
            return RpnOperations.stack(token, stack, variables, 'swap', 0, require_int=False, mode=mode)

        elif len(token[1]) > 0 and token[1][-1] == '=':
            if len(stack) < 1:
                raise StackUnderflowError(token)
            item = stack.pop()
            variables[token[1][:-1]] = item

    @staticmethod
    def stack(token, stack, variables, func, num_ops, require_int, mode):
        if isinstance(num_ops, int) and len(stack) < num_ops:
            raise StackUnderflowError(token)
        else:
            try:
                ops = []
                for i in range(num_ops):
                    n = stack.pop()
                    if require_int:
                        if not isinstance(n, int):
                            raise IntegerOperationError(token)
                    ops.insert(0, n)
                if func == 'pick':
                    return stack[ops[0]]
                elif func == 'repeat':
                    if ops[0] <= 0:
                        raise DomainError(token, 1, '+inf')
                    cmd = token[1].strip().split()
                    new_token = (token[0], cmd[-1])
                    for i in range(ops[0]):
                        item = RpnOperations.execute(new_token, stack, variables, mode)
                        if item is not None:
                            stack.append(item)
                elif func == 'depth':
                    return len(stack)
                elif func == 'drop':
                    stack.pop()
                    return None
                elif func == 'dropn':
                    for i in range(ops[0]):
                        stack.pop()
                    return None
                elif func == 'dup':
                    stack.append(stack[-1])
                    return None
                elif func == 'dupn':
                    for i in range(ops[0]):
                        stack.append(stack[-1])
                    return None
                elif func == 'roll':
                    cp = np.roll(stack, ops[0])
                    for i in range(len(stack)):
                        stack[i] = cp[i]
                    return None
                elif func == 'rolld':
                    cp = np.roll(stack, -ops[0])
                    for i in range(len(stack)):
                        stack[i] = cp[i]
                    return None
                elif func == 'swap':
                    top = stack[-1]
                    stack[-1] = stack[-2]
                    stack[-2] = top
                    return None
            except Exception as e:
                if isinstance(e, RpnErrors):
                    raise e
                if hasattr(e, 'message'):
                    m = e.message
                else:
                    m = e
                raise OperationExecutionError(token, m)

    @staticmethod
    def operator(f, *args, mode='dec'):
        if f == '+':
            return args[0] + args[1]
        elif f == '-':
            return args[0] - args[1]
        elif f == '*':
            return args[0] * args[1]
        elif f == '/':
            if mode == 'dec':
                return args[0] / args[1]
            else:
                return args[0] // args[1]
        elif f == '%':
            return args[0] % args[1]
        elif f == '++':
            return args[0] + 1
        elif f == '--':
            return args[0] - 1
        elif f == '&':
            return args[0] & args[1]
        elif f == '|':
            return args[0] | args[1]
        elif f == '^':
            return args[0] ^ args[1]
        elif f == '~':
            return ~args[0]
        elif f == '<<':
            return args[0] << args[1]
        elif f == '>>':
            return args[0] >> args[1]
        elif f == '!':
            if args[0] == 0:
                return 1
            else:
                return 0
        elif f == '&&':
            if args[0] != 0 and args[1] != 0:
                return 1
            else:
                return 0
        elif f == '||':
            if args[0] != 0 or args[1] != 0:
                return 1
            else:
                return 0
        elif f == '^^':
            if (args[0] != 0 and args[1] != 0) or (args[0] == 0 and args[1] == 0):
                return 0
            else:
                return 1
        elif f == '!=':
            if args[0] != args[1]:
                return 1
            else:
                return 0
        elif f == '==':
            if args[0] == args[1]:
                return 1
            else:
                return 0
        elif f == '<':
            if args[0] < args[1]:
                return 1
            else:
                return 0
        elif f == '<=':
            if args[0] <= args[1]:
                return 1
            else:
                return 0
        elif f == '>':
            if args[0] > args[1]:
                return 1
            else:
                return 0
        elif f == '>=':
            if args[0] >= args[1]:
                return 1
            else:
                return 0
        elif f == 'sqrt':
            if mode == 'dec':
                return math.sqrt(args[0])
            else:
                return int(round(math.sqrt(args[0])))
        elif f == 'pow':
            if mode == 'dec':
                return math.pow(args[0], args[1])
            else:
                return int(round(math.pow(args[0], args[1])))
        elif f == 'sign':
            return 1 if args[0] > 0 else -1 if args[0] < 0 else 0
        elif f == 'ip':
            return int(args[0])
        elif f == 'fp':
            return args[0] - int(args[0])

    @staticmethod
    def apply(token, stack, variables, func, num_ops, require_int=False, unsupported=False):
        if unsupported:
            raise UnsupportedError(token)
        if isinstance(num_ops, int) and len(stack) < num_ops:
            raise StackUnderflowError(token)
        else:
            try:
                if isinstance(num_ops, str) and num_ops == 'all':
                    return func(stack)
                else:
                    ops = []
                    for i in range(num_ops):
                        n = stack.pop()
                        if require_int:
                            if not isinstance(n, int):
                                raise IntegerOperationError(token)
                        ops.insert(0, n)
                    return func(*ops)
            except Exception as e:
                if isinstance(e, RpnErrors):
                    raise e
                if hasattr(e, 'message'):
                    m = e.message
                else:
                    m = e
                raise OperationExecutionError(token, m)

    @staticmethod
    def clear_all(token, stack, variables):
        stack.clear()
        variables.clear()
        return None

    @staticmethod
    def clear_stack(token, stack, variables):
        stack.clear()
        return None

    @staticmethod
    def clear_var(token, stack, variables):
        variables.clear()
        return None



