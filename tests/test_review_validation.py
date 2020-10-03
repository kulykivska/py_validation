from tornado.testing import gen_test

from tests.base_test_case import AsyncTestCase
from models.validation.review_validation import RatingValidator, BodyValidator
from controller.ErrorHandler import InvalidReviewRatingException, InvalidReviewBodyException


class TestReviewValidation(AsyncTestCase):

    """
        Summary: ReviewValidator validates reviews.
        Unit under test: ReviewValidator.
        Preconditions: None.
        Parameters to test: correct validation of reviews.
        Test scenario:
            1. Validate invalid review rating;
               Compare received error and sample one;

            2. Validate invalid review body;
               Compare received error and sample one;
    """

    def setUp(self):
        super(TestReviewValidation, self).setUp()
        AsyncTestCase.get_new_ioloop(self)

    @gen_test
    def test_rating_validator(self):
        with self.assertRaises(expected_exception=InvalidReviewRatingException):
            RatingValidator().validate({"rating": 0})

    @gen_test
    def test_text_validator(self):
        with self.assertRaises(expected_exception=InvalidReviewBodyException):
            BodyValidator().validate({"body": ""})
