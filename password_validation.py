from typing import Optional

from bcrypt import checkpw


class PasswordValidator:
    def __init__(self, next_validator: Optional["PasswordValidator"] = None):
        self.next_validator: Optional[PasswordValidator] = next_validator

    def validate(self, password: str) -> None:
        """
        Base implementation of validate method. Passes validation to the next validator if exists.

        :param password: Password to validate.
        """

        if self.next_validator is not None:
            self.next_validator.validate(password)


class InvalidLengthValidator(PasswordValidator):
    MINIMUM_PASSWORD_LENGTH: int = 8
    MAXIMUM_PASSWORD_LENGTH: int = 100

    def validate(self, password: str) -> None:
        """
        Raises exception if password length is invalid. Otherwise passes password to base validator.

        :param password: Password to validate.
        """

        from controller.ErrorHandler import InvalidPasswordException

        if not (self.MINIMUM_PASSWORD_LENGTH <= len(password) <= self.MAXIMUM_PASSWORD_LENGTH):
            raise InvalidPasswordException
        else:
            super().validate(password)


class NoDigitValidator(PasswordValidator):
    def validate(self, password: str) -> None:
        """
        Raises exception if password contains no digit. Otherwise passes password to base validator.

        :param password: Password to validate.
        """

        from controller.ErrorHandler import InvalidPasswordException

        if not any(map(str.isdigit, password)):
            raise InvalidPasswordException
        else:
            super().validate(password)


class NoLowercaseCharacterValidator(PasswordValidator):
    def validate(self, password: str) -> None:
        """
        Raises exception if password contains no lowercase character. Otherwise passes password to base validator.

        :param password: Password to validate.
        """

        from controller.ErrorHandler import InvalidPasswordException

        if not any(map(str.islower, password)):
            raise InvalidPasswordException
        else:
            super().validate(password)


class NoUppercaseCharacterValidator(PasswordValidator):
    def validate(self, password: str) -> None:
        """
        Raises exception if password contains no uppercase character. Otherwise passes password to base validator.

        :param password: Password to validate.
        """

        from controller.ErrorHandler import InvalidPasswordException

        if not any(map(str.isupper, password)):
            raise InvalidPasswordException
        else:
            super().validate(password)


class WhitespaceValidator(PasswordValidator):
    def validate(self, password: str) -> None:
        """
        Raises exception if password contains whitespaces. Otherwise passes password to base validator.

        :param password: Password to validate.
        """

        from controller.ErrorHandler import InvalidPasswordException

        if any(map(str.isspace, password)):
            raise InvalidPasswordException
        else:
            super().validate(password)


class NewPasswordIsTheSameAsCurrentOneValidator:
    @staticmethod
    def validate(new_password: str, current_hashed_password: bytes) -> None:
        """
        Raises exception if new password is the same as current one.

        :param new_password: Password to validate.
        :param current_hashed_password: Hashed password to validate the first one regarding to another one.
        """

        from controller.ErrorHandler import NewPasswordIsTheSameAsCurrentOneException

        if checkpw(password=new_password.encode("utf-8"), hashed_password=current_hashed_password):
            raise NewPasswordIsTheSameAsCurrentOneException


class OldPasswordIsNotTheSameAsCurrentOneValidator:
    @staticmethod
    def validate(old_password: str, current_hashed_password: bytes) -> None:
        """
        Raises exception if old password is the same as current one.

        :param old_password: Password to validate.
        :param current_hashed_password: Hashed password to validate the first one regarding to another one.
        """

        from controller.ErrorHandler import OldPasswordIsNotTheSameAsCurrentOneException

        if not checkpw(password=old_password.encode("utf-8"), hashed_password=current_hashed_password):
            raise OldPasswordIsNotTheSameAsCurrentOneException


class PasswordIsNotTheSameAsRepeatPasswordValidator:
    @staticmethod
    def validate(password: str, repeat_password: str) -> None:
        """
        Raises exception if password is not the same as repeat one.

        :param password: Password to validate.
        :param repeat_password: Password to validate the first one regarding to another one.
        """

        from controller.ErrorHandler import PasswordIsNotTheSameAsRepeatPasswordException

        if password != repeat_password:
            raise PasswordIsNotTheSameAsRepeatPasswordException


class GivenPasswordIsNotTheSameAsCurrentOneValidator:
    @staticmethod
    def validate(password: str, current_hashed_password: bytes) -> None:
        """
        Raises exception if given password is the same as current one.

        :param password: Password to validate.
        :param current_hashed_password: Hashed password to validate the first one regarding to another one.
        """

        from controller.ErrorHandler import GivenPasswordIsNotTheSameAsCurrentOneException

        if not checkpw(password=password.encode("utf-8"), hashed_password=current_hashed_password):
            raise GivenPasswordIsNotTheSameAsCurrentOneException
