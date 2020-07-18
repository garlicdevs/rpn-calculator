from pygments.token import Token
from errors import InvalidNumberError, InvalidSyntaxError
import random
import mpmath as mp


class RpnTokens(object):
    # Arithmetic Operators
    ADD = ['+', 'Add']
    SUBTRACT = ['-', 'Subtract']
    MULTIPLY = ['*', 'Multiply']
    DIVIDE = ['/', 'Divide']
    CLEAR_ALL = ['cla', 'Clear the stack and variables']
    CLEAR_STACK = ['clr', 'Clear the stack']
    CLEAR_VAR = ['clv', 'Clear the variables']
    MODULUS = ['%', 'Modulus']
    INCREMENT = ['++', 'Increment']
    DECREMENT = ['--', 'Decrement']

    # Bitwise Operators
    BIT_AND = ['&', 'Bitwise AND']
    BIT_OR = ['|', 'Bitwise OR']
    BIT_XOR = ['^', 'Bitwise XOR']
    BIT_NOT = ['~', 'Bitwise NOT']
    BIT_SHIFT_LEFT = ['<<', 'Bitwise shift left']
    BIT_SHIFT_RIGHT = ['>>', 'Bitwise shift right']

    # Boolean Operators
    BOOLEAN_NOT = ['!', 'Boolean NOT']
    BOOLEAN_AND = ['&&', 'Boolean AND']
    BOOLEAN_OR = ['||', 'Boolean OR']
    BOOLEAN_XOR = ['^^', 'Boolean XOR']

    # Comparison Operators
    NOT_EQUAL = ['!=', 'Not equal to']
    LESS_THAN = ['<', 'Less than']
    LESS_THAN_OR_EQUAL = ['<=', 'Less than or equal to']
    EQUAL = ['==', 'Equal to']
    GREATER_THAN = ['>', 'Greater than']
    GREATER_THAN_OR_EQUAL = ['>=', 'Greater than or equal to']

    # Trigonometric Functions
    ACOS = ['acos', 'Arc Cosine']
    ASIN = ['asin', 'Arc Sine']
    ATAN = ['atan', 'Arc Tangent']
    COS = ['cos', 'Cosine']
    COSH = ['cosh', 'Hyperbolic Cosine']
    SIN = ['sin', 'Sine']
    SINH = ['sinh', 'Hyperbolic Sine']
    TANH = ['tanh', 'Hyperbolic tangent']

    # Numeric Utilities
    CEIL = ['ceil', 'Ceiling']
    FLOOR = ['floor', 'Floor']
    ROUND = ['round', 'Round']
    IP = ['ip', 'Integer part']
    FP = ['fp', 'Floating part']
    SIGN = ['sign', 'Push -1, 0, or 1 depending on the sign']
    ABS = ['abs', 'Absolute value']
    MAX = ['max', 'Max']
    MIN = ['min', 'Min']

    # Display Modes
    HEX = ['hex', 'Switch display mode to hexadecimal']
    DEC = ['dec', 'Switch display mode to decimal (default)']
    BIN = ['bin', 'Switch display mode to binary']
    OCT = ['oct', 'Switch display mode to octal']

    # Constants
    E = ['e', 'Push e']
    PI = ['pi', 'Push PI']
    RAND = ['rand', 'Generate a random number']

    # Mathematics Functions
    EXP = ['exp', 'Exponentiation']
    FACT = ['fact', 'Factorial']
    SQRT = ['sqrt', 'Square root']
    LN = ['ln', 'Natual Logarithm']
    LOG = ['log', 'Logarithm']
    POW = ['pow', 'Raise a number to a power']

    # Networking
    HNL = ['hnl', 'Host to network long']
    HNS = ['hns', 'Host to network short']
    NHL = ['nhl', 'Network to host long']
    NHS = ['nhs', 'Network to host short']

    # Stack Manipulation
    PICK = ['pick', 'Pick the -n\'th item from the stack']
    REPEAT = ['repeat', 'Repeat an operation n times, e.g. \'3 repeat +']
    DEPTH = ['depth', 'Push the current stack depth']
    DROP = ['drop', 'Drops the top item from the stack']
    DROPN = ['dropn', 'Drops n items from the stack']
    DUP = ['dup', 'Duplicates the top stack item']
    DUPN = ['dupn', 'Duplicates the top n stack items in order']
    ROLL = ['roll', 'Roll the stack upwards by n']
    ROLLD = ['rolld', 'Roll the stack downwards by n']
    STACK = ['stack', 'Toggles stack display from horizontal to vertical']
    SWAP = ['swap', 'Swap the top 2 stack items']

    # Macros and Variables
    MACRO = ['macro', 'Defines a macro, e.g. \'macro kib 1024 *\'']
    X_EQUAL = ['x=', 'Assigns a variable, e.g. \'1024 x=\'']

    # Other
    HELP = ['help', 'Print the help message']
    EXIT = ['exit', 'Exit the calculator']
    LIMIT = ['limit', 'Limit showing n stack items (default = 10)']
    PREC = ['prec', 'Number of digits after . of a decimal number (default = 10)']
    THEME = ['theme', 'Toggle color mode for text']

    @staticmethod
    def is_number(token):
        if token[0] == Token.Literal.Number.Integer \
                or token[0] == Token.Literal.Number.Float \
                or token[0] == Token.Literal.Number.Oct \
                or token[0] == Token.Literal.Number.Bin \
                or token[0] == Token.Literal.Number.Hex \
                or token[0] == Token.Keyword.Constant:
            return True
        return False

    @staticmethod
    def is_keyword(token):
        if token[0] == Token.Keyword:
            return True
        return False

    @staticmethod
    def is_literal(token):
        if token[0] == Token.Literal:
            return True
        return False

    @staticmethod
    def get_number(token, prec=10):
        try:
            if token[0] == Token.Literal.Number.Integer:
                return int(token[1])
            elif token[0] == Token.Literal.Number.Float:
                return float(token[1])
            elif token[0] == Token.Literal.Number.Oct\
                    or token[0] == Token.Literal.Number.Bin \
                    or token[0] == Token.Literal.Number.Hex:
                return int(token[1], 0)
            elif token[0] == Token.Keyword.Constant:
                if token[1] == RpnTokens.E[0]:
                    mp.dps = prec
                    return float(mp.e)
                elif token[1] == RpnTokens.PI[0]:
                    mp.dps = prec
                    return float(mp.pi)
                elif token[1] == RpnTokens.RAND[0]:
                    return random.uniform(0, 1)
        except:
            raise InvalidNumberError(token)

    @staticmethod
    def is_valid(token):
        if token[0] == Token.Error:
            raise InvalidSyntaxError(token)
        return True

    @staticmethod
    def contains_space(token):
        if token[0] == Token.Text:
            return True
        return False

    @staticmethod
    def check_syntax(tokens):
        tks = []
        for token in tokens:
            RpnTokens.is_valid(token)
            tks.append(token)
        return True, tks

