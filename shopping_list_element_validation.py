from __future__ import annotations
from typing import Optional, Dict

from models.shopping_list_entry import ShoppingListElement


class ShoppingListElementValidator:
    def __init__(self, next_validator: Optional[ShoppingListElementValidator] = None):
        self.next_validator: Optional[ShoppingListElementValidator] = next_validator

    def validate(self, shopping_list_element_to_validate: ShoppingListElement) -> None:
        """
        Base implementation of validate method. Passes validation to the next validator if exists. Otherwise returns
        None.

        :param shopping_list_element_to_validate: Shopping list element to validate.
        """

        if self.next_validator is not None:
            self.next_validator.validate(shopping_list_element_to_validate)

    def validate_dictionary(self, shopping_list_element_to_validate: Dict) -> None:
        """
        Base implementation of validate dictionary method. Passes validation to the next validator if exists. Otherwise
        returns None.

        :param shopping_list_element_to_validate: Shopping list element to validate.
        """

        if self.next_validator is not None:
            self.next_validator.validate_dictionary(shopping_list_element_to_validate)


class NameValidator(ShoppingListElementValidator):
    MINIMUM_NAME_LENGTH: int = 1
    MAXIMUM_NAME_LENGTH: int = 100

    def validate(self, shopping_list_element_to_validate: ShoppingListElement) -> None:
        """
        Raises exception if specified name of custom shopping list element is invalid. Otherwise passes product to base
        validator.

        :param shopping_list_element_to_validate: Shopping list element to validate.
        """

        from controller.ErrorHandler import InvalidCustomShoppingListElementNameException

        is_name_valid: bool = self.MINIMUM_NAME_LENGTH <= len(
            shopping_list_element_to_validate.name) <= self.MAXIMUM_NAME_LENGTH
        if shopping_list_element_to_validate.is_custom and not is_name_valid:
            raise InvalidCustomShoppingListElementNameException(maximum_length=self.MAXIMUM_NAME_LENGTH)
        else:
            super().validate(shopping_list_element_to_validate)

    def validate_dictionary(self, shopping_list_element_to_validate: Dict) -> None:
        super().validate_dictionary(shopping_list_element_to_validate)
