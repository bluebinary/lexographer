from lexographer.enumerations import Context


class LexographerError(Exception):
    """LexographerError is the root exception type for library exception handling."""

    pass


class LexerError(LexographerError):
    """LexerError is the exception type for errors raised by the Lexer class."""

    _context: Context = None

    def __init__(self, message: str, context: Context = None):
        super().__init__(message)

        if type is None:
            pass
        elif isinstance(context, Context):
            self._context = context
        else:
            raise TypeError(
                "The 'context' argument, if specified, must have a Context enumeration value!"
            )

    @property
    def context(self) -> Context | None:
        return self._context


class TokenizerError(LexographerError):
    """TokenizerError is the exception type for errors raised by the Tokenizer class."""

    pass


class ParserError(LexographerError):
    """ParserError is the exception type for errors raised by the Parser class."""

    pass
