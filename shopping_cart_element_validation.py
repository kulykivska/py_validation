from __future__ import annotations
from typing import Optional, Dict

from models.sc_element import SCElement
from models.items import Item
from models.enums.delivery_method import DeliveryMethod


class ShoppingCartElementValidator:
    def __init__(self, next_validator: Optional[ShoppingCartElementValidator] = None):
        self.next_validator: Optional[ShoppingCartElementValidator] = next_validator

    def validate(self, shopping_cart_element_to_validate: SCElement) -> None:
        """
        Base implementation of validate method. Passes validation to the next validator if exists. Otherwise returns
        None.

        :param shopping_cart_element_to_validate: Shopping cart element to validate.
        """

        if self.next_validator is not None:
            self.next_validator.validate(shopping_cart_element_to_validate)

    async def validate_dictionary(self, shopping_cart_element_to_validate: Dict) -> None:
        """
        Base implementation of validate dictionary method. Passes validation to the next validator if exists. Otherwise
        returns None.

        :param shopping_cart_element_to_validate: Shopping cart element to validate.
        """

        if self.next_validator is not None:
            await self.next_validator.validate_dictionary(shopping_cart_element_to_validate)


class DeliveryMethodIsNotAvailableValidator(ShoppingCartElementValidator):
    def validate(self, shopping_cart_element_to_validate: SCElement) -> None:
        super().validate(shopping_cart_element_to_validate)

    async def validate_dictionary(self, shopping_cart_element_to_validate: Dict) -> None:
        """
        Raises exception if specified delivery method is not available. Otherwise passes product to base validator.

        :param shopping_cart_element_to_validate: Shopping cart element to validate.
        """

        from controller.ErrorHandler import DeliveryMethodIsNotAvailableException

        shopping_cart_element: SCElement = await SCElement.objects.get(shopping_cart_element_to_validate["ID"])
        product: Item = await Item.objects.get(shopping_cart_element.item_id)
        is_us_delivery_not_available: bool = shopping_cart_element_to_validate["delivery"][
                                                 "method"] == DeliveryMethod.US_DELIVERY.value and not product.deliveryOffered
        is_pick_up_not_available: bool = shopping_cart_element_to_validate["delivery"][
                                             "method"] == DeliveryMethod.PICK_UP.value and not product.marketPickOffered
        if is_us_delivery_not_available or is_pick_up_not_available:
            raise DeliveryMethodIsNotAvailableException
        else:
            await super().validate_dictionary(shopping_cart_element_to_validate)
