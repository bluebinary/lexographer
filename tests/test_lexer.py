import pytest
import lexographer

from lexographer import Context, Type, Token


def test_lexer_instantiation_with_text(data: callable):
    """Test the instantiation of the Lexer class."""

    # Load some sample text data
    text: str = data("sample.txt")

    # Ensure that the sample text data loaded as expected
    assert isinstance(text, str)
    assert len(text) > 0

    # Create an instance of the Lexer subclass
    lexer = lexographer.Lexer(text=text)

    # Ensure that the Lexer class instance has the expected type
    assert isinstance(lexer, lexographer.Lexer)

    # Ensure that the text specified during instantiation is as expected
    assert lexer.text == text

    # Ensure the length of the text specified during instantiation is as expected
    assert lexer.length == len(text)


def text_lexer_instantiation_with_file(path: callable, data: callable):
    """Test the instantiation of the Lexer class with a file path."""

    # Obtain the file path for the sample file
    file: str = path("sample.txt")

    # Ensure that the file path has the expected type
    assert isinstance(file, str)

    # Create an instance of the Lexer subclass
    lexer = lexographer.Lexer(file=file)

    # Ensure that the Lexer class instance has the expected type
    assert isinstance(lexer, lexographer.Lexer)

    # Ensure that the file specified during instantiation is as expected
    assert lexer.file == file

    # Load some sample text data
    text: str = data("sample.txt")

    # Ensure that the sample text data loaded as expected
    assert isinstance(text, str)
    assert len(text) > 0

    # Ensure that the text specified during instantiation is as expected
    assert lexer.text == text

    # Ensure the length of the text specified during instantiation is as expected
    assert lexer.length == len(text)


@pytest.fixture(name="lexer", scope="function")
def lexer_fixture(path: callable, data: callable) -> lexographer.Lexer:
    """Create an instance of the Lexer class initialised with the sample text data."""

    # Obtain the path for the sample text data
    file: str = path("sample.txt")

    # Ensure that the sample text data loaded as expected
    assert isinstance(file, str)

    # Create an instance of the Lexer class
    lexer = lexographer.Lexer(file=file)

    # Ensure that the Lexer class instance has the expected type
    assert isinstance(lexer, lexographer.Lexer)

    # Load the sample text data to compare against the data loaded by the Lexer
    text: str = data("sample.txt")

    # Ensure that the sample text data loaded as expected
    assert isinstance(text, str)
    assert len(text) > 0

    # Ensure that the text specified during Lexer instantiation is as expected
    assert lexer.text == text

    # Ensure the length of the text specified during instantiation is as expected
    assert lexer.length == len(lexer) == len(text)

    return lexer


def text_lexer_iterator():
    """Test the Lexer's iterator support."""

    # Define some sample text to lex through
    text: str = "abcdef"

    # Create an instance of the Lexer class, instantiated with the sample text
    lexer = lexographer.Lexer(text=text)

    # Ensure that the Lexer class was initialised as expected with the sample text
    assert lexer.text == text

    # Ensure that the Lexer class' len() support and .length property report as expected
    assert len(lexer) == lexer.length == len(lexer.text)

    # Iterate through the Lexer's source text character-by-character, and ensure
    # that the returned characters are as expected and that the Lexer's cursor index
    # position is updated to the expected value on each cycle through the iterator
    for index, character in enumerate(lexer):
        # Ensure that the returned character is as expected
        assert character == text[index]

        # Ensure that the returned character matches the most recently lexed character(s)
        assert character == lexer.characters

        # Ensure that the cursor index position is as expected (index starts at 0)
        assert lexer.index == index

        # Ensure that the column number is as expected (column starts at 1)
        assert lexer.column == index + 1

        # Ensure that the line number is as expected (line starts at 1, and increments
        # when an new line character '\n' is encountered in the source input text)
        assert lexer.line == 1

        # The Lexer class also provides access to a Position instance which wraps the
        # positional attributes up together in a single instance for easy value passing
        assert isinstance(lexer.position, lexographer.Position)

        # Ensure that the positional values held by the returned Position instance are
        # as expected and that they match those reported directly by the Lexer
        assert lexer.position.index == lexer.index == index
        assert lexer.position.column == lexer.column == index + 1
        assert lexer.position.line == lexer.line == 1


def test_lexer_read(lexer: lexographer.Lexer):
    """Test reading one character through the Lexer class."""

    # Read the first single character from the Lexer's source input text, incrementing
    # the Lexer's cursor position by the number of read characters, in preparation for
    # the next read
    read: str = lexer.read()

    # Ensure that the read value is a string
    assert isinstance(read, str)

    # Ensure that the read value is a single character in length (the default)
    assert len(read) == 1

    # Ensure that the read character matches the first character of the source input
    assert read == lexer.text[0]

    # Read the second single character from the Lexer's source input text
    read: str = lexer.read()

    # Ensure that the read value is a string
    assert isinstance(read, str)

    # Ensure that the read value is a single character in length (the default)
    assert len(read) == 1

    # Ensure that the read character matches the second character of the source input
    assert read == lexer.text[1]


def test_lexer_read_with_length(lexer: lexographer.Lexer):
    """Test reading a specified number of characters through the Lexer class."""

    # Read the specified number of characters from the Lexer's source input text
    read: str = lexer.read(length=3)

    # Ensure that the read value is a string
    assert isinstance(read, str)

    # Ensure that the read value length matches the number of specified characters
    assert len(read) == 3

    # Ensure that the read characters match the expected characters of the source input
    assert read == lexer.text[0:3]


def test_lexer_peek(lexer: lexographer.Lexer):
    """Test peeking the default number of characters through the Lexer class."""

    # Peek the first character from the Lexer's source input text, while leaving the
    # Lexer's cursor position unchanged
    peek: str = lexer.peek()

    # Ensure that the peeked value is a string
    assert isinstance(peek, str)

    # Ensure that the peeked value is a single character in length (the default)
    assert len(peek) == 1

    # Ensure that the peeked character matches the first character of the source input
    # as this peek took place immediately after initialisation of the Lexer class when
    # the cursor index position is at 0 representing the first character of source input
    assert peek == lexer.text[0]

    # As a peek() does not affect the cursor index position, it should be the same as it
    # was before the peek() call was made
    assert lexer.index == 0


def test_lexer_peek_with_offset(lexer: lexographer.Lexer):
    """Test peeking the specified number of characters through the Lexer class."""

    # Peek the second character from the Lexer's source input text, while leaving the
    # Lexer's cursor position unchanged
    peek: str = lexer.peek(offset=1)

    # Ensure that the peeked value is a string
    assert isinstance(peek, str)

    # Ensure that the peeked value is a single character in length (the default)
    assert len(peek) == 1

    # Ensure that the peeked character matches the second character of the source input
    assert peek == lexer.text[1]

    # As a peek() does not affect the cursor index position, it should be the same as it
    # was before the peek() call was made
    assert lexer.index == 0


def test_lexer_peek_with_negative_offset(lexer: lexographer.Lexer):
    """Test peeking the specified number of characters through the Lexer class."""

    # Read the first character from the Lexer's source input text, advancing the cursor
    read: str = lexer.read()

    # Ensure that the read value is a string
    assert isinstance(read, str)

    # Ensure that the cursor index was advanced as expected by the call to .read()
    assert lexer.index == 1

    # Peek the second character from the Lexer's source input text, while leaving the
    # Lexer's cursor position unchanged
    peek: str = lexer.peek(offset=-1)

    # Ensure that the peeked value is a string
    assert isinstance(peek, str)

    # Ensure that the peeked value is a single character in length (the default)
    assert len(peek) == 1

    # Ensure that the peeked character matches the second character of the source input
    assert peek == lexer.text[0]

    # As a peek() does not affect the cursor index position, it should be the same as it
    # was before the peek() call was made
    assert lexer.index == 1


def text_lexer_consume(lexer: lexographer.Lexer):
    """Test the Lexer class' .consume() method."""

    # Before any calls to .read() or .consume() the cursor index should be at 0
    assert lexer.index == 0
    assert lexer.column == 1
    assert lexer.line == 1

    # Peek the first character from the Lexer's source input text, while leaving the
    # Lexer's cursor position unchanged
    peek: str = lexer.peek()

    # Ensure that the peeked value is a string
    assert isinstance(peek, str)

    # Ensure that the peeked value is a single character in length (the default)
    assert len(peek) == 1

    # Ensure that the peeked character matches the first character of the source input
    # as this peek took place immediately after initialisation of the Lexer class when
    # the cursor index position is at 0 representing the first character of source input
    assert peek == lexer.text[0]

    # As calls to .peek() do not impact the cursor index position, it should be the same
    assert lexer.index == 0

    # Calling .consume(), consumes the current character and advances the cursor index
    consume: str = lexer.consume()

    # The .consume() method returns the character that was consumed
    assert isinstance(consume, str)

    # This should be the same as the character that was peeked immediately prior
    assert consume == peek

    # After a call to .read() or .consume() the cursor index should have advanced
    assert lexer.index == 1


def text_lexer_push(lexer: lexographer.Lexer):
    """Test the Lexer class' .push() method."""

    # Before any calls to .read() or .consume() the cursor index should be at 0
    assert lexer.index == 0
    assert lexer.column == 1
    assert lexer.line == 1

    # Read the first three characters of the source input text, advancing the cursor
    read: str = lexer.read(length=3)

    # Ensure that the return value of the call to .read() is a string
    assert isinstance(read, str)

    # Ensure that the returned value is as expected
    assert read == "The"

    # Ensure that the cursor index position has been advanced as expected by the .read()
    assert lexer.index == 2
    assert lexer.column == 3
    assert lexer.line == 1

    # Push back the specified number of characters, that is to move back the cursor index
    push: str = lexer.push(length=1)

    # Ensure that the return value of the call to .push() is a string
    assert isinstance(push, str)

    # Ensure that the returned value is as expected
    assert push == "e"

    # Ensure the cursor index position was pushed back as expected by the call to .push()
    assert lexer.index == 1
    assert lexer.column == 2
    assert lexer.line == 1


def text_lexer_lookahead(lexer: lexographer.Lexer):
    """Test the Lexer class' .lookahead() method."""

    # Before any calls to .read() or .consume() the cursor index should be at 0
    assert lexer.index == 0
    assert lexer.column == 1
    assert lexer.line == 1

    # Determine if the specified character or characters are present at the cursor index
    assert lexer.lookahead("The") is True

    # Ensure that the cursor index position is unmodified by the call to .lookahead()
    assert lexer.index == 0


def text_lexer_lookbehind(lexer: lexographer.Lexer):
    """Test the Lexer class' .lookbehind() method."""

    # Before any calls to .read() or .consume() the cursor index should be at 0
    assert lexer.index == 0
    assert lexer.column == 1
    assert lexer.line == 1

    # Read the first three characters of the source input text, advancing the cursor
    read: str = lexer.read(length=3)

    # Ensure that the cursor index position has been advanced as expected by the .read()
    assert lexer.index == 2
    assert lexer.column == 3
    assert lexer.line == 1

    assert isinstance(read, str)

    assert read == "The"

    # Determine if the specified character or characters are present at the cursor index
    assert lexer.lookbehind("The") is True

    # Ensure that the cursor index position is unmodified by the call to .lookahead()
    assert lexer.index == 2
    assert lexer.column == 3
    assert lexer.line == 1
