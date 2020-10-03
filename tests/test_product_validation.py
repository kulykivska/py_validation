from tornado.testing import gen_test

from tests.base_test_case import AsyncTestCase
from models.validation.product_validation import BlockValidator, DraftValidator, ExpireValidator, \
    ProductCodeAlreadyExistsValidator, TooShortPriceValidPeriodValidator, TooShortSalePeriodValidator
from controller.ErrorHandler import InactiveProductException, ProductCodeAlreadyExistsException, \
    TooShortPriceValidPeriodException, TooShortSalePeriodException
from models.items import Item


class TestProductValidation(AsyncTestCase):
    """
    Summary: Validates products.
    Unit under test: ProductValidator.
    Preconditions: None.
    Parameters to test: correct validation of products.
    Test scenario:
        1. Validate blocked product;
           Compare received error and sample one;

        2. Validate draft product;
           Compare received error and sample one;

        3. Validate expired product;
           Compare received error and sample one;

        4. Validate product with code that is already exists;
           Compare received error and sample one;

        5. Validate product with too short price valid period;
           Compare received error and sample one;

        6. Validate product with enabled sale, but too short sale period;
           Compare received error and sample one;
    """

    @gen_test
    def test_block_validator(self):
        product: Item = (yield Item.objects.get("59fae88e095c7628122c55c8"))

        with self.assertRaises(InactiveProductException):
            yield BlockValidator().validate(product)

    @gen_test
    def test_draft_validator(self):
        product: Item = (yield Item.objects.get("572eca0c095c7630d781dc3c"))

        with self.assertRaises(InactiveProductException):
            yield DraftValidator().validate(product)

    @gen_test
    def test_expire_validator(self):
        product: Item = (yield Item.objects.get("59fae88e095c7628122c55c8"))

        with self.assertRaises(InactiveProductException):
            yield ExpireValidator().validate(product)

    @gen_test
    def test_product_code_already_exists_validator(self):
        with self.assertRaises(ProductCodeAlreadyExistsException):
            yield ProductCodeAlreadyExistsValidator().validate_dictionary(
                product_to_validate={"productNo": " OR0507162206 "})

    @gen_test
    async def test_too_short_price_valid_period_validator(self):
        with self.assertRaises(TooShortPriceValidPeriodException):
            await TooShortPriceValidPeriodValidator().validate_dictionary(
                product_to_validate={"valitFrom": 1612432399, "validTill": 1612434237})

    @gen_test
    async def test_too_short_sale_period_validator(self):
        with self.assertRaises(TooShortSalePeriodException):
            await TooShortSalePeriodValidator().validate_dictionary(
                product_to_validate={"saleIsOn": True, "saleDateFrom": 1612432399, "saleDateTill": 1612434237})
