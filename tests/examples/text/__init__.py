import lexographer

from lexographer import Type, Token, Context

# Register several new token types for use by the custom Tokenizer and Parser subclasses
Type.register("Word")
Type.register("Number")


class Tokenizer(lexographer.Tokenizer):
    """Sample custom Tokenizer subclass demonstrating tokenizing a text string."""

    _types = {
        ".": Type.Period,
        ",": Type.Comma,
        "!": Type.Exclamation,
        "?": Type.Question,
        ":": Type.Colon,
        ";": Type.SemiColon,
        "\n": Type.NewLine,
        "\r": Type.CarriageReturn,
        "\t": Type.Tab,
    }

    def parse(self):
        """The 'parse' method is the entrypoint for customizing the Tokenizer for the
        structured text that will be processed into one or more Token instances."""

        self.context = Context.Start

        # Iterate through all of the individual characters in the source text
        while character := self.lexer.read():
            text: str = character

            if character in self._types:
                # Create a Token for each recognized special character that is found
                self.token = Token(
                    tokenizer=self,
                    type=self._types[character],
                    text=character,
                )
            elif character.isspace():
                # Parse and group one or more consecutive spaces into a Token
                while (character := self.lexer.peek()) and character.isspace():
                    text += self.lexer.read()

                self.token = Token(tokenizer=self, type=Type.Spacing, text=text)
            elif character.isnumeric() or character == ".":
                # Parse and group one or more consecutive number characters into a Token
                while character := self.lexer.peek() and (
                    character.isnumeric() or character == "." or character == ","
                ):
                    text += self.lexer.read()

                self.token = Token(tokenizer=self, type=Type.Number, text=text)
            elif character.isalpha() or character == "'":
                # Parse and group one or more consecutive word characters into a Token
                while (character := self.lexer.peek()) and (
                    character.isalpha() or character == "'"
                ):
                    text += self.lexer.read()

                self.token = Token(tokenizer=self, type=Type.Word, text=text)
            else:
                # Record any other characters, if any, as of the Unknown type
                self.token = Token(tokenizer=self, type=Type.Unknown, text=character)

        self.context = Context.Finish


class Parser(lexographer.Parser):
    """Sample custom Parser subclass demonstrating using a tokenized text string."""

    def parse(self) -> str:
        """Sample overridden parse() method implementation; this example reassembles the
        parsed text string, back into its original form with some slight modifications,
        but anything could be done with the parsed tokens depending on the use case."""

        text: str = ""

        for token in self.tokenizer.tokens:
            if token.type is Type.NewLine:
                text += "\t"
            elif token.type is Type.CarriageReturn:
                text += "\r"
            elif token.type is Type.Tab:
                text += "\t"
            elif token.type is Type.Period:
                # Swap "." with "!"
                text += "!"
            elif token.type is Type.Exclamation:
                # Swap "!" with "."
                text += "."
            elif token.type is Type.Spacing:
                # Replace the token's spaces with "•" characters
                text += "•" * token.length
            else:
                text += token.text

        return text


# Associate the new custom tokenizer with the new custom Parser
Parser.register_tokenizer(Tokenizer)
