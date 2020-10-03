from __future__ import annotations
from typing import Optional, Dict
from datetime import timedelta

from models.items import Item


class ProductValidator:
    def __init__(self, next_validator: Optional[ProductValidator] = None):
        self.next_validator: Optional[ProductValidator] = next_validator

    def validate(self, product_to_validate: Item) -> None:

        """
            Base implementation of validate method. Passes validation to the next validator if exists. Otherwise
                returns None.

            :type product_to_validate: Item
            :param product_to_validate: Product object.

            :return: None
        """

        if self.next_validator is not None:
            self.next_validator.validate(product_to_validate)

    async def validate_dictionary(self, product_to_validate: Dict) -> None:
        """
        Base implementation of validate dictionary method. Passes validation to the next validator if exists. Otherwise
        returns None.

        :param product_to_validate: Product presented in form of dictionary.
        """

        if self.next_validator is not None:
            await self.next_validator.validate_dictionary(product_to_validate)


class BlockValidator(ProductValidator):
    def validate(self, product_to_validate: Item) -> None:

        """
            Raises exception if product is blocked. Otherwise passes product to base validator.

            :type product_to_validate: Item
            :param product_to_validate: Product object.

            :return: None
        """

        from controller.ErrorHandler import InactiveProductException
        if not product_to_validate.is_enable:
            raise InactiveProductException
        else:
            super().validate(product_to_validate)

    async def validate_dictionary(self, product_to_validate: Dict) -> None:
        await super().validate_dictionary(product_to_validate)


class DraftValidator(ProductValidator):
    def validate(self, product_to_validate: Item) -> None:

        """
            Raises exception if product is draft. Otherwise passes product to base validator.

            :type product_to_validate: Item
            :param product_to_validate: Product object.

            :return: None
        """

        from controller.ErrorHandler import InactiveProductException
        if product_to_validate.draft:
            raise InactiveProductException
        else:
            super().validate(product_to_validate)

    async def validate_dictionary(self, product_to_validate: Dict) -> None:
        await super().validate_dictionary(product_to_validate)


class ExpireValidator(ProductValidator):
    def validate(self, product_to_validate: Item) -> None:

        """
            Raises exception if product is expired. Otherwise passes product to base validator.

            :type product_to_validate: Item
            :param product_to_validate: Product object.

            :return: None
        """

        from controller.ErrorHandler import InactiveProductException
        if product_to_validate.is_expired():
            raise InactiveProductException
        else:
            super().validate(product_to_validate)

    async def validate_dictionary(self, product_to_validate: Dict) -> None:
        await super().validate_dictionary(product_to_validate)


class ProductCodeAlreadyExistsValidator(ProductValidator):
    def validate(self, product_to_validate: Item) -> None:
        super().validate(product_to_validate)

    async def validate_dictionary(self, product_to_validate: Dict) -> None:
        """
        Raises exception if product's code is already exists. Otherwise passes product to base validator.

        :param product_to_validate: Product presented in form of dictionary.
        """

        from controller.ErrorHandler import ProductCodeAlreadyExistsException

        if product_to_validate.get("productNo") and await Item.objects.get(
                productNo=product_to_validate["productNo"].strip(), is_parent=True) is not None:
            raise ProductCodeAlreadyExistsException
        else:
            await super().validate_dictionary(product_to_validate)


class TooShortPriceValidPeriodValidator(ProductValidator):
    def validate(self, product_to_validate: Item) -> None:
        super().validate(product_to_validate)

    async def validate_dictionary(self, product_to_validate: Dict) -> None:
        """
        Raises exception if product's price valid period is too short. Otherwise passes product to base validator.

        :param product_to_validate: Product presented in form of dictionary.
        """

        from controller.ErrorHandler import TooShortPriceValidPeriodException

        if product_to_validate["validTill"] - product_to_validate["valitFrom"] < timedelta(hours=1).total_seconds():
            raise TooShortPriceValidPeriodException
        else:
            await super().validate_dictionary(product_to_validate)


class TooShortSalePeriodValidator(ProductValidator):
    def validate(self, product_to_validate: Item) -> None:
        super().validate(product_to_validate)

    async def validate_dictionary(self, product_to_validate: Dict) -> None:
        """
        Raises exception if product's sale period is too short. Otherwise passes product to base validator.

        :param product_to_validate: Product presented in form of dictionary.
        """

        from controller.ErrorHandler import TooShortSalePeriodException

        if product_to_validate.get("saleIsOn", False) and (
            product_to_validate["saleDateTill"] - product_to_validate["saleDateFrom"]) < timedelta(
                hours=1).total_seconds():
            raise TooShortSalePeriodException
        else:
            await super().validate_dictionary(product_to_validate)
