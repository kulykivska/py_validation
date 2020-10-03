from tornado.testing import gen_test
from mock import patch, MagicMock

from tests.base_test_case import AsyncTestCase
from models.validation.user_validation import EmailValidator, LoginValidator, BuyerCompanyNameValidator, \
    BlockedUserValidator
from controller.ErrorHandler import EmailIsAlreadyInUseException, LoginIsAlreadyInUseException, \
    BuyerCompanyNameIsAlreadyInUseException, NoVerifyEmailAddress, BlockedUserException
from models.users import User


class TestUserValidation(AsyncTestCase):
    """
    Summary: Validates user.
    Unit under test: models.validation.user_validation.UserValidator.
    Preconditions:
        5. Mock models.validation.user_validation.UserValidator.validate method;
    Parameters to test:
        1. Is validation of user whose email that is in use correct;
        2. Is validation of user whose login that is in use correct;
        3. Is validation of user whose buyer/company name that is in use correct;
        4. Is validation of user whose email is not verified correct;
        5. Is validation of user that is blocked correct;
    Test scenario:
        1. Validate user whose email that is in use;
           Compare received error and sample one;

        2. Validate user whose login that is in use;
           Compare received error and sample one;

        3. Validate user whose buyer/company name that is in use;
           Compare received error and sample one;

        4. Validate user whose email is not verified;
           Compare received error and sample one;

        5. Validate user that is not blocked;
           Check if mocked methods were called with correct arguments;
           Validate user that is blocked;
           Compare received error and sample one;
    """

    @gen_test
    async def test_email_is_already_in_user_validator(self):
        with self.assertRaises(EmailIsAlreadyInUseException):
            await EmailValidator().validate_dictionary(user={"email": "example@example.com"})

    @gen_test
    async def test_login_validator(self):
        with self.assertRaises(LoginIsAlreadyInUseException):
            await LoginValidator().validate_dictionary(user={"login": "test1"})

    @gen_test
    async def test_buyer_company_name_validator(self):
        with self.assertRaises(BuyerCompanyNameIsAlreadyInUseException):
            await BuyerCompanyNameValidator().validate_dictionary(user={"accessLevel": 1, "title": "Test Test"})

    @gen_test
    async def test_email_is_not_verified_validator(self):
        user: User = await User.objects.get("57d90e96095c7605435dca70")
        with self.assertRaises(NoVerifyEmailAddress):
            EmailValidator().validate(user)

    @patch("models.validation.user_validation.UserValidator.validate")
    def test_blocked_user_validator(self, validate_mock: MagicMock):
        user: User = User(is_enable=True)

        BlockedUserValidator().validate(user)

        validate_mock.assert_called_with(user)

        with self.assertRaises(BlockedUserException):
            BlockedUserValidator().validate(user=User(is_enable=False))
