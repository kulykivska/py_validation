from tornado.testing import gen_test

from tests.base_test_case import AsyncTestCase
from models.validation.address_validation import NoPrimaryValidator, InvalidAddressLine1LengthValidator, \
    InvalidAddressLine2LengthValidator
from controller.ErrorHandler import NoPrimaryAddressException, InvalidAddressLineFieldValuesException


class TestAddressValidation(AsyncTestCase):

    """
        Summary: AddressValidation validates addresses.
        Unit under test: AddressValidator.
        Preconditions: None.
        Parameters to test: correct validation of addresses.
        Test scenario:
            1. Validate list of not primary addresses;
               Compare received error and sample one;

            2. Validate list of addresses that contains address line 1 which length is invalid;
               Compare received error and sample one;

            3. Validate list of addresses that contains address line 2 which length is invalid;
               Compare received error and sample one;
    """

    def setUp(self):
        super(TestAddressValidation, self).setUp()
        AsyncTestCase.get_new_ioloop(self)

    @gen_test
    def test_no_primary_validator(self):
        with self.assertRaises(NoPrimaryAddressException):
            yield NoPrimaryValidator().validate([{"isPrimary": False}, {"isPrimary": False}])

    @gen_test
    def test_invalid_address_line_1_length_validator(self):
        with self.assertRaises(InvalidAddressLineFieldValuesException):
            yield InvalidAddressLine1LengthValidator().validate([{"address1": "a" * 101}])

    @gen_test
    def test_invalid_address_line_2_length_validator(self):
        with self.assertRaises(InvalidAddressLineFieldValuesException):
            yield InvalidAddressLine2LengthValidator().validate([{"address2": "a" * 101}])
