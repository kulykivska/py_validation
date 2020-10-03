from tornado.testing import gen_test
from mock import patch

from tests.base_test_case import AsyncTestCase
from models.validation.shopping_cart_element_validation import DeliveryMethodIsNotAvailableValidator
from controller.ErrorHandler import DeliveryMethodIsNotAvailableException
from models.sc_element import SCElement
from models.items import Item


class TestShoppingCartElementValidation(AsyncTestCase):
    """
    Summary: Validates shopping cart elements.
    Unit under test: models.validation.shopping_cart_element_validator.ShoppingCartElementValidator.
    Preconditions: None.
    Parameters to test:
        1. Is validation of delivery method correct;
    Test scenario:
        1. Validate delivery method that is not available;
           Check if appropriate exceptions were raised;
           Check if mocked methods were called with correct arguments;
    """

    @gen_test
    async def test_delivery_method_is_not_available_validator(self):
        async def get(*args, **kwargs):
            if args[0] == "test_shopping_element_1":
                return SCElement(item_id="test_item_id_1", deliveryOffered=False, marketPickOffered=True)
            elif args[0] == "test_shopping_element_2":
                return SCElement(item_id="test_item_id_2", deliveryOffered=True, marketPickOffered=False)
            elif args[0] == "test_item_id_1":
                return Item(deliveryOffered=False, marketPickOffered=True)
            elif args[0] == "test_item_id_2":
                return Item(deliveryOffered=True, marketPickOffered=False)

        with patch(target="motorengine.queryset.QuerySet.get", side_effect=get) as get_mock:
            with self.assertRaises(DeliveryMethodIsNotAvailableException):
                await DeliveryMethodIsNotAvailableValidator().validate_dictionary(
                    {"ID": "test_shopping_element_1", "delivery": {"method": "US Delivery"}})

            with self.assertRaises(DeliveryMethodIsNotAvailableException):
                await DeliveryMethodIsNotAvailableValidator().validate_dictionary(
                    {"ID": "test_shopping_element_2", "delivery": {"method": "Pick Up"}})

        self.assertEqual(get_mock.call_args_list[0][0][0], "test_shopping_element_1")
        self.assertEqual(get_mock.call_args_list[1][0][0], "test_item_id_1")
        self.assertEqual(get_mock.call_args_list[2][0][0], "test_shopping_element_2")
        self.assertEqual(get_mock.call_args_list[3][0][0], "test_item_id_2")
