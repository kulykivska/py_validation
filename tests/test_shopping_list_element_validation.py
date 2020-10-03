from tests.base_test_case import AsyncTestCase
from models.validation.shopping_list_element_validation import NameValidator
from models.shopping_list_entry import ShoppingListElement
from controller.ErrorHandler import InvalidCustomShoppingListElementNameException


class TestShoppingListElementValidation(AsyncTestCase):
    """
    Summary: Validates shopping list elements.
    Unit under test: ShoppingListElementValidator.
    Preconditions: None.
    Parameters to test:
        1. Is validation of custom shopping list element correct;
    Test scenario:
        1. Validate custom shopping list element name that is invalid;
           Compare received error and sample one;
    """

    def setUp(self):
        super(TestShoppingListElementValidation, self).setUp()
        AsyncTestCase.get_new_ioloop(self)

    def test_name_validator(self):
        with self.assertRaises(InvalidCustomShoppingListElementNameException):
            NameValidator().validate(ShoppingListElement(
                **{"is_custom": True, "name": "a" * 101, "subcategory_entry_id": "", "is_active": True}))
