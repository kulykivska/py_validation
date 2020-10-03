from bcrypt import hashpw, gensalt

from tests.base_test_case import AsyncTestCase
from models.validation.password_validation import InvalidLengthValidator, NoDigitValidator, \
    NoLowercaseCharacterValidator, NoUppercaseCharacterValidator, WhitespaceValidator, \
    NewPasswordIsTheSameAsCurrentOneValidator, OldPasswordIsNotTheSameAsCurrentOneValidator, \
    PasswordIsNotTheSameAsRepeatPasswordValidator, GivenPasswordIsNotTheSameAsCurrentOneValidator
from controller.ErrorHandler import InvalidPasswordException, NewPasswordIsTheSameAsCurrentOneException, \
    OldPasswordIsNotTheSameAsCurrentOneException, PasswordIsNotTheSameAsRepeatPasswordException, \
    GivenPasswordIsNotTheSameAsCurrentOneException


class TestPasswordValidation(AsyncTestCase):
    """
    Summary: Validates passwords.
    Unit under test: models.validation.password_validation.PasswordValidator.
    Preconditions: None.
    Parameters to test:
        1. Is validation of password that length is invalid correct;
        2. Is validation of password that contains no digit validation correct;
        3. Is validation of password that contains no lowercase character correct;
        4. Is validation of password that contains no uppercase character correct;
        5. Is validation of password that contains whitespaces correct;
        6. Is validation of new password that is the same as current one correct;
        7. Is validation of old password that is not the same as current one correct;
        8. Is validation of password that is not the same as repeat password correct;
        9. Is validation of given password that is not the same as current one correct;
    Test scenario:
        1. Validate password which length is invalid;
           Compare received error and sample one;

        2. Validate password which contains no digit;
           Compare received error and sample one;

        3. Validate password which contains no lowercase character;
           Compare received error and sample one;

        4. Validate password which contains no uppercase character;
           Compare received error and sample one;

        5. Validate password which contains whitespaces;
           Compare received error and sample one;

        6. Validate new password that is the same as current one;
           Compare received error and sample one;

        7. Validate old password that is not the same as current one;
           Compare received error and sample one;

        8. Validate password that is not the same as repeat password;
           Compare received error and sample one;

        9. Validate given password that is not the same as currect one;
           Compare received error and sample one;
    """

    def test_invalid_length_validator(self):
        with self.assertRaises(InvalidPasswordException):
            InvalidLengthValidator().validate(password="Test123")

    def test_no_digit_validator(self):
        with self.assertRaises(InvalidPasswordException):
            NoDigitValidator().validate(password="Testtest")

    def test_no_lowercase_character_validator(self):
        with self.assertRaises(InvalidPasswordException):
            NoLowercaseCharacterValidator().validate(password="TEST1234")

    def test_no_uppercase_character_validator(self):
        with self.assertRaises(InvalidPasswordException):
            NoUppercaseCharacterValidator().validate(password="test1234")

    def test_whitespace_validator(self):
        with self.assertRaises(InvalidPasswordException):
            WhitespaceValidator().validate(password="Test 1234")

    def test_new_password_is_the_same_as_current_one_validator(self):
        with self.assertRaises(NewPasswordIsTheSameAsCurrentOneException):
            NewPasswordIsTheSameAsCurrentOneValidator.validate(new_password="Test1234",
                                                               current_hashed_password=hashpw(b"Test1234", gensalt()))

    def test_old_password_is_not_the_same_as_current_one_validator(self):
        with self.assertRaises(OldPasswordIsNotTheSameAsCurrentOneException):
            OldPasswordIsNotTheSameAsCurrentOneValidator.validate(old_password="Test12345",
                                                                  current_hashed_password=hashpw(b"Test1234",
                                                                                                 gensalt()))

    def test_password_is_not_the_same_as_repeat_password_validator(self):
        with self.assertRaises(PasswordIsNotTheSameAsRepeatPasswordException):
            PasswordIsNotTheSameAsRepeatPasswordValidator.validate(password="Test1234", repeat_password="Test12345")

    def test_given_password_is_not_the_same_as_current_one_validator(self):
        with self.assertRaises(GivenPasswordIsNotTheSameAsCurrentOneException):
            GivenPasswordIsNotTheSameAsCurrentOneValidator.validate(password="Test12345",
                                                                    current_hashed_password=hashpw(b"Test1234",
                                                                                                   gensalt()))
