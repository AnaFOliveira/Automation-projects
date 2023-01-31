import pytest
from .. import dashboard

#
# @pytest.fixture
# def default_text():
#     return ["Fear__is__the", "mind__killer"]


def test_to_text():
    """This function tests the conversion from a list of strings to a text works as expected."""
    text = ["Fear is the", "mind killer"]
    assert dashboard.to_text(text) == "Fear is the mind killer "


if __name__ == '__main__':
    pytest.main()
