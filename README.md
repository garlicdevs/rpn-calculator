This calculator is written in Python 3.6.

1. [Development] If running directly with Python3, the following libraries should be installed first
- pygments = '2.5.2'
- termcolor 
- numpy
- mpmath
- tabulate
- pandas
- pyfiglet
- pyinstaller
- colorama

2. [Testing] Run rpn directly from the standalone app distributed in folder ../rpn/dist/

NOTES: For flexibility, operators can be inseparable, 
For example users can type: 1 1 1 1+++---5 i.e., 1 1 1 1 ++ + -- -5
The rules based on the precedences between operators

1. Two digits operators -> high precedence (1)
2. The minus sign before a number becomes a negative number -> medium precedence (2)
3. One digit operators -> low precedence (3)


Of course, users can type operators separately.

Other notes: 
1. Macro can be recursive, variables are unlimited (ab=, x=, addh9_=, etc.), 
2. The number of decimal digits after . is limited to 10 (users can change it by using the command, e.g., 100 PREC)
3. The number of items showing in the stack is 10 (users can can change it by using the command, e.g, 5 LIMIT)
4. The calculator supports two themes: no text color decoration, and with text color (default) (best for dark mode).
Toggle them with THEME command


CHEERS

