import pytest
import lexographer

from lexographer import Position


def test_position_instantiation_with_defaults():
    """Test instantiation of the Position class with default values."""

    position = Position()

    assert isinstance(position, Position)

    assert position.index == 0
    assert position.column == 0
    assert position.line == 0


def test_position_instantiation_with_values():
    """Test instantiation of the Position class with specified values."""

    position = Position(index=1, column=2, line=3)

    assert isinstance(position, Position)

    assert position.index == 1
    assert position.column == 2
    assert position.line == 3


@pytest.fixture(name="position", scope="function")
def position_fixture() -> Position:
    """Create, validate, and return an instance of the Position class."""

    # Create an instance of the Position class with specified values
    position = Position(index=4, column=5, line=6)

    # Ensure the class instance is of the expected type
    assert isinstance(position, Position)

    # Ensure that the property values are as expected, per those specified on creation
    assert position.index == 4
    assert position.column == 5
    assert position.line == 6

    return position


def test_position_copy(position: Position):
    """Test instantiation of the Position class with specified values."""

    # Create a copy of the position instance
    newposition = position.copy()

    # Ensure that the copy has the expected type
    assert isinstance(newposition, Position)

    # Ensure that the copy does not refer to the same object in memory
    assert not newposition is position

    # Ensure that the copy is a different object with a different identifier
    assert not id(newposition) == id(position)

    # Ensure that the copy contains the same values
    assert newposition.index == position.index
    assert newposition.column == position.column
    assert newposition.line == position.line


def test_position_equality(position: Position):
    """Test the numeric equality of a Position class instance."""

    # Create a copy of the position instance
    newposition = position.copy()

    # Ensure that the copy of the position has value equality with the original
    assert (newposition == position) is True


def test_position_non_equality(position: Position):
    """Test the numeric equality of a Position class instance."""

    # Create a copy of the position instance
    newposition = position.copy()

    # Ensure that the copy of the position has value equality with the original
    assert not (newposition == position) is False


def test_position_greater_than(position: Position):
    """Test the numeric greater than equality of a Position class instance."""

    # Create a copy of the position instance and adjust its index and column positions
    newposition = position.copy().adjust(offset=1)  # offset forward by 1

    # Ensure that the adjusted copy of the position numerically compares as expected
    assert newposition > position

    assert newposition.index == position.index + 1
    assert newposition.column == position.column + 1
    assert newposition.line == position.line


def test_position_less_than(position: Position):
    """Test the numeric less than equality of a Position class instance."""

    # Create a copy of the position instance and adjust its index and column positions
    newposition = position.copy().adjust(offset=-1)  # offset backward by 1

    # Ensure that the adjusted copy of the position numerically compares as expected
    assert newposition < position

    assert newposition.index == position.index - 1
    assert newposition.column == position.column - 1
    assert newposition.line == position.line


def test_position_greater_than_equal(position: Position):
    """Test the numeric greater than equality of a Position class instance."""

    # Create a copy of the position instance and adjust its index and column positions
    newposition = position.copy().adjust(offset=1)  # offset forward by 1

    # Ensure that the adjusted copy of the position numerically compares as expected
    assert newposition >= position

    assert newposition.index == position.index + 1
    assert newposition.column == position.column + 1
    assert newposition.line == position.line


def test_position_less_than_equal(position: Position):
    """Test the numeric less than equality of a Position class instance."""

    # Create a copy of the position instance and adjust its index and column positions
    newposition = position.copy().adjust(offset=-1)  # offset backward by 1

    # Ensure that the adjusted copy of the position numerically compares as expected
    assert newposition <= position

    assert newposition.index == position.index - 1
    assert newposition.column == position.column - 1
    assert newposition.line == position.line
