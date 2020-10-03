from typing import Optional, Dict, Any

from models.users import User


class UserValidator:
    def __init__(self, next_validator: Optional["UserValidator"] = None):
        self.next_validator: Optional[UserValidator] = next_validator

    def validate(self, user: User) -> None:
        """
        Base implementation of validate method. Passes validation to the next validator if exists.

        :param user: User to validate.
        """

        if self.next_validator is not None:
            self.next_validator.validate(user)

    async def validate_dictionary(self, user: Dict[str, Any]) -> None:
        """
        Base implementation of validate dictionary method. Passes validation to the next validator if exists.

        :param user: User to validate.
        """

        if self.next_validator is not None:
            await self.next_validator.validate_dictionary(user)


class LoginValidator(UserValidator):
    def validate(self, user: User) -> None:
        super().validate(user)

    async def validate_dictionary(self, user: Dict[str, Any]) -> None:
        """
        Raises exception if there is user with the same login. Otherwise passes user to base validator.

        :param user: User to validate.
        """

        from controller.ErrorHandler import LoginIsAlreadyInUseException

        if await User.objects.get(login=user["login"].lower().strip()):
            raise LoginIsAlreadyInUseException
        else:
            await super().validate_dictionary(user)


class EmailValidator(UserValidator):
    def validate(self, user: User) -> None:
        """
        Raises exception if user's email is not verified. Otherwise passes user to base validator.

        :param user: User to validate.
        """

        from controller.ErrorHandler import NoVerifyEmailAddress

        if not user.email_conform:
            raise NoVerifyEmailAddress
        else:
            super().validate(user)

    async def validate_dictionary(self, user: Dict[str, Any]) -> None:
        """
        Raises exception if there is user with the same email address. Otherwise passes user to base validator.

        :param user: User to validate.
        """

        from controller.ErrorHandler import EmailIsAlreadyInUseException

        if await User.objects.get(email=user["email"].lower().strip()):
            raise EmailIsAlreadyInUseException
        else:
            await super().validate_dictionary(user)


class BuyerCompanyNameValidator(UserValidator):
    def validate(self, user: User) -> None:
        super().validate(user)

    async def validate_dictionary(self, user: Dict[str, Any]) -> None:
        """
        Raises exception if there is user with the same buyer/company name. Otherwise passes user to base validator.

        :param user: User to validate.
        """

        from controller.ErrorHandler import BuyerCompanyNameIsAlreadyInUseException

        if await User.objects.get(title=user["title"]):
            raise BuyerCompanyNameIsAlreadyInUseException(user)
        else:
            await super().validate_dictionary(user)


class BlockedUserValidator(UserValidator):
    def validate(self, user: User) -> None:
        """
        Raises exception if user is blocked. Otherwise passes user to base validator.

        :param user: User to validate.
        """

        from controller.ErrorHandler import BlockedUserException

        if not user.is_enable:
            raise BlockedUserException
        else:
            super().validate(user)

    async def validate_dictionary(self, user: Dict[str, Any]) -> None:
        await super().validate_dictionary(user)
