class Parameter(object):
    """A data-filtering parameter."""

    EQUALS_OPERATION = '='
    NOT_EQUALS_OPERATION = '!='
    GREATER_THAN_OPERATION = '>'
    GREATER_THAN_OR_EQUALS_OPERATION = '>='
    LESS_THAN_OPERATION = '<'
    LESS_THAN_OR_EQUALS_OPERATION = '<='
    CONTAINS_OPERATION = '=~'
    NOT_CONTAINS_OPERATION = '!~'

    def __init__(self, field, op, value):
        """Creates a new data-filtering parameter.

        :param field(string): The field name.
        :param op(string): The operation to apply, one of the constants in this class.
        :param value: The value(s) to test against.
        """
        self.field = field
        self.op = op
        self.value = value
