from __future__ import annotations
from typing import Optional, Dict


class ReviewValidator:
    def __init__(self, next_validator: Optional[ReviewValidator] = None):
        self.next_validator: Optional[ReviewValidator] = next_validator

    def validate(self, review_to_validate: Dict) -> None:

        """
            Base implementation of validate method. Passes validation to the next validator if exists. Otherwise
                returns None.

            :type review_to_validate: Dict
            :param review_to_validate: Review fields presented in form of dictionary.

            :return: None
        """

        if self.next_validator is not None:
            self.next_validator.validate(review_to_validate)


class RatingValidator(ReviewValidator):
    def validate(self, review_to_validate: Dict) -> None:

        """
            Raises exception if review rating is out of range. Otherwise passes user to base validator.

            :type review_to_validate: Dict
            :param review_to_validate: Review fields presented in form of dictionary.

            :return: None
        """

        from controller.ErrorHandler import InvalidReviewRatingException

        MINIMUM_RATING: int = 1
        MAXIMUM_RATING: int = 5

        if not MINIMUM_RATING <= review_to_validate["rating"] <= MAXIMUM_RATING:
            raise InvalidReviewRatingException
        else:
            super().validate(review_to_validate)


class BodyValidator(ReviewValidator):
    def validate(self, review_to_validate: Dict) -> None:

        """
            Raises exception if review body is invalid. Otherwise passes user to base validator.

            :type review_to_validate: Dict
            :param review_to_validate: Review fields presented in form of dictionary.

            :return: None
        """

        from controller.ErrorHandler import InvalidReviewBodyException

        MINIMUM_REVIEW_TEXT_LENGTH: int = 1
        MAXIMUM_REVIEW_TEXT_LENGTH: int = 200

        if not MINIMUM_REVIEW_TEXT_LENGTH <= len(review_to_validate["body"]) <= MAXIMUM_REVIEW_TEXT_LENGTH:
            raise InvalidReviewBodyException
        else:
            super().validate(review_to_validate)
