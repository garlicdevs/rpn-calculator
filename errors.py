
class RpnErrors(Exception):
    def __init__(self, token):
        self._token = token

    def get_message(self):
        raise NotImplementedError


class StackUnderflowError(RpnErrors):
    def get_message(self):
        return '[StackUnderflowError] Not enough operands for \'{}\''.format(self._token[1])


class InvalidNumberError(RpnErrors):
    def get_message(self):
        return '[InvalidNumberError] \'{}\' is an invalid number'.format(self._token[1])


class InvalidSyntaxError(RpnErrors):
    def get_message(self):
        return '[InvalidSyntaxError] Invalid syntax with \'{}\''.format(self._token[1])


class UnsupportedError(RpnErrors):
    def get_message(self):
        return '[UnsupportedError] Operation \'{}\' is not supported in the current mode'.format(self._token[1])


class UnsupportedDecimalError(RpnErrors):
    def get_message(self):
        return '[UnsupportedDecimalError] Decimal number \'{}\' is not supported in the current mode'.\
            format(self._token[1])


class IntegerOperationError(RpnErrors):
    def get_message(self):
        return '[IntegerOperationError] \'{}\' can only be applied to integers'.format(self._token[1])


class DomainError(RpnErrors):
    def __init__(self, token, min_, max_):
        self._token = token
        self.min = min_
        self.max = max_

    def get_message(self):
        return '[DomainError] Operation \'{}\' failed due to out of bound [{}, {}]'.format(self._token[1],
                                                                                           self.min, self.max)


class OperationExecutionError(RpnErrors):
    def __init__(self, token, message):
        self._token = token
        self._message = message

    def get_message(self):
        return '[OperationExecutionError] Operation \'{}\' failed - {}'.format(self._token[1], self._message)


