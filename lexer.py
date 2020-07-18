from pygments.lexer import RegexLexer, include, words, bygroups, using, this, default
from pygments.token import Keyword, Name, Number, Operator, Text, Literal
from tokens import RpnTokens


class RpnLexer(RegexLexer):
    """
        A syntax tree for RPN
    """

    name = 'RPN'
    aliases = ['rpn']
    filenames = ['*.rpn']
    mimetypes = ['text/rpn']

    operator_ = '!=|==|<<|>>|<=|>=|\+\+|--|&&|\|\||\^\^|[-+/*!%&|^~<>]'
    builtin_ = words((
                RpnTokens.HNL[0], RpnTokens.HNS[0], RpnTokens.NHL[0], RpnTokens.NHS[0],
                RpnTokens.CLEAR_ALL[0], RpnTokens.CLEAR_VAR[0], RpnTokens.CLEAR_STACK[0],

                RpnTokens.PICK[0], RpnTokens.DEPTH[0], RpnTokens.DROP[0], RpnTokens.DROPN[0],
                RpnTokens.DUP[0], RpnTokens.DUPN[0], RpnTokens.ROLL[0], RpnTokens.ROLLD[0],
                RpnTokens.SWAP[0],

                RpnTokens.EXP[0], RpnTokens.FACT[0], RpnTokens.SQRT[0], RpnTokens.LN[0], RpnTokens.LOG[0],
                RpnTokens.POW[0],

                RpnTokens.CEIL[0], RpnTokens.FLOOR[0], RpnTokens.ROUND[0], RpnTokens.IP[0], RpnTokens.FP[0],
                RpnTokens.SIGN[0],
                RpnTokens.ABS[0], RpnTokens.MAX[0], RpnTokens.MIN[0],

                RpnTokens.ACOS[0], RpnTokens.ASIN[0], RpnTokens.ATAN[0], RpnTokens.COS[0], RpnTokens.COSH[0],
                RpnTokens.SIN[0], RpnTokens.SINH[0], RpnTokens.TANH[0]), prefix=r'\b', suffix=r'\b')
    keywords_ = words((
                RpnTokens.HEX[0], RpnTokens.DEC[0], RpnTokens.BIN[0], RpnTokens.OCT[0], RpnTokens.STACK[0],
                RpnTokens.X_EQUAL[0], RpnTokens.HELP[0], RpnTokens.EXIT[0], RpnTokens.LIMIT[0], RpnTokens.PREC[0],
                RpnTokens.THEME[0]),
                prefix=r'\b',
                suffix=r'\b')
    constants_ = words((RpnTokens.E[0], RpnTokens.PI[0], RpnTokens.RAND[0]), prefix=r'\b', suffix=r'\b')
    float_ = r'-?(\d(\d)*\.(\d(\d)*)?|(\d(\d)*)?\.\d(\d)*)([eE][+-]?\d(\d)*)?'
    float_2 = r'-?\d(\d)*[eE][+-]?\d(\d)*'
    oct_ = r'-?0[oO]([0-7])+'
    bin_ = r'-?0[bB]([01])+'
    hex_ = r'-?0[xX]([a-fA-F0-9])+'
    int_ = r'-?\d(\d)*'
    numbers_ = '(' + constants_.get() + ')|(' + float_ + ')|(' + float_2 + ')|(' + oct_ + \
               ')|(' + bin_ + ')|(' + hex_ + ')|(' + int_ + ')'
    variables_ = r'\b[a-zA-Z][a-zA-Z0-9_]*'
    tokens = {
        'root': [
            # Whitespace or newline
            (r'[^\S\n]+', Text),

            # Numbers should be put here so it can recognized negative value, e.g. -5 vs (- 5 or --5 or -- 5)
            include('numbers'),

            # Operators
            (r'' + operator_, Operator),

            # Keywords
            include('keywords'),

            # Built-in functions
            include('builtins'),

            # Repeat
            (r'\b(repeat)\s+((?:' + operator_ + '|' + builtin_.get() + '))', Name.Builtin),

            # Macro
            (r'\b(macro)\s+(?:[a-zA-Z][a-zA-Z0-9_]*)\s+((?:' + operator_ + r'\s*|' + builtin_.get()
             + r'\s+|' + numbers_ + r'\s*|' + variables_ + r'\s+)+)', Name.Builtin),

            # Assignment
            (r'\b[a-zA-Z][a-zA-Z0-9_]*=', Name.Builtin),

            # Variables
            (variables_, Literal)
        ],
        'keywords': [
            (keywords_, Keyword),
            (constants_, Keyword.Constant),
        ],
        'builtins': [
            (builtin_,
             Name.Builtin),
        ],
        'numbers': [
            (float_, Number.Float),
            (float_2, Number.Float),
            (oct_, Number.Oct),
            (bin_, Number.Bin),
            (hex_, Number.Hex),
            (int_, Number.Integer),
        ],
    }