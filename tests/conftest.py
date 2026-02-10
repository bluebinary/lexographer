import pytest
import sys
import os

path = os.path.join(os.path.dirname(__file__), "..", "source")

sys.path.insert(0, path)  # add 'lexographer' library path for importing into the tests

import lexographer

assert lexographer.__file__ == os.path.join(path, "lexographer", "__init__.py")


@pytest.fixture(scope="session", name="data")
def data() -> callable:
    """Create a fixture that can be used to obtain the contents of example data files as
    strings or bytes by specifying the path relative to the /tests/data folder."""

    def fixture(path: str, binary: bool = False) -> str:
        """Read the specified data file, returning its contents either as a string value
        or if requested in binary mode returning the encoded bytes value."""

        if not isinstance(path, str):
            raise TypeError("The 'path' argument must have a string value!")

        if not isinstance(binary, bool):
            raise TypeError("The 'binary' argument must have a boolean value!")

        filepath: str = os.path.join(os.path.dirname(__file__), "data", path)

        if not os.path.exists(filepath):
            raise ValueError(
                f"The requested example file, '{filepath}', does not exist!"
            )

        # If binary mode has been specified, adjust the read mode accordingly
        mode: str = "rb" if binary else "r"

        with open(filepath, mode) as handle:
            return handle.read()

    return fixture


@pytest.fixture(scope="session", name="path")
def path() -> callable:
    """Create a fixture that can be used to obtain the path for example data files as
    by specifying the path relative to the /tests/data folder."""

    def fixture(path: str) -> str:
        """Read the specified data file, returning its contents either as a string value
        or if requested in binary mode returning the encoded bytes value."""

        if not isinstance(path, str):
            raise TypeError("The 'path' argument must have a string value!")

        filepath: str = os.path.join(os.path.dirname(__file__), "data", path)

        if not os.path.exists(filepath):
            raise ValueError(
                f"The requested example file, '{filepath}', does not exist!"
            )

        return filepath

    return fixture
