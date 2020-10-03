from __future__ import annotations
from typing import Optional, Dict, List


class AddressValidator:
    def __init__(self, next_validator: Optional[AddressValidator] = None):
        self.next_validator: Optional[AddressValidator] = next_validator

    def validate(self, addresses_to_validate: List[Dict]) -> None:

        """
            Base implementation of validate method. Passes validation to the next validator if exists. Otherwise
                returns None.

            :type addresses_to_validate: List[Dict]
            :param addresses_to_validate: List of address fields presented in form of dictionary.

            :return: None
        """

        if self.next_validator is not None:
            self.next_validator.validate(addresses_to_validate)


class NoPrimaryValidator(AddressValidator):
    def validate(self, addresses_to_validate: List[Dict]) -> None:

        """
            Raises exception if there is no primary address in the list. Otherwise passes user to base validator.

            :type addresses_to_validate: List[Dict]
            :param addresses_to_validate: List of address fields presented in form of dictionary.

            :return: None
        """

        from controller.ErrorHandler import NoPrimaryAddressException
        if not any([address["isPrimary"] for address in addresses_to_validate]):
            raise NoPrimaryAddressException
        else:
            super().validate(addresses_to_validate)


class InvalidAddressLine1LengthValidator(AddressValidator):
    def validate(self, addresses_to_validate: List[Dict]) -> None:

        """
            Raises exception if address line 1 of any address is invalid. Otherwise passes user to base validator.

            :type addresses_to_validate: List[Dict]
            :param addresses_to_validate: List of address fields presented in form of dictionary.

            :return: None
        """

        from controller.ErrorHandler import InvalidAddressLineFieldValuesException

        MINIMUM_ADDRESS_LINE_1_LENGTH: int = 6
        MAXIMUM_ADDRESS_LINE_1_LENGTH: int = 100

        for address_to_validate in addresses_to_validate:
            if not MINIMUM_ADDRESS_LINE_1_LENGTH <= len(
                    address_to_validate["address1"]) <= MAXIMUM_ADDRESS_LINE_1_LENGTH:
                raise InvalidAddressLineFieldValuesException(line_number=1,
                                                             minimum_length=MINIMUM_ADDRESS_LINE_1_LENGTH,
                                                             maximum_length=MAXIMUM_ADDRESS_LINE_1_LENGTH)
        else:
            super().validate(addresses_to_validate)


class InvalidAddressLine2LengthValidator(AddressValidator):
    def validate(self, addresses_to_validate: List[Dict]) -> None:

        """
            Raises exception if address line 2 of any address is invalid. Otherwise passes user to base validator.

            :type addresses_to_validate: List[Dict]
            :param addresses_to_validate: List of address fields presented in form of dictionary.

            :return: None
        """

        from controller.ErrorHandler import InvalidAddressLineFieldValuesException

        MINIMUM_ADDRESS_LINE_2_LENGTH: int = 0
        MAXIMUM_ADDRESS_LINE_2_LENGTH: int = 100

        for address_to_validate in addresses_to_validate:
            if not MINIMUM_ADDRESS_LINE_2_LENGTH <= len(
                    address_to_validate.get("address2", "")) <= MAXIMUM_ADDRESS_LINE_2_LENGTH:
                raise InvalidAddressLineFieldValuesException(line_number=2,
                                                             minimum_length=MINIMUM_ADDRESS_LINE_2_LENGTH,
                                                             maximum_length=MAXIMUM_ADDRESS_LINE_2_LENGTH)
        else:
            super().validate(addresses_to_validate)
