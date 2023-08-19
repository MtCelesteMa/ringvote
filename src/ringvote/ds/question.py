"""Objects representing questions."""

from .question_pb2 import Question as Question_
from .question_pb2 import Response as Response_

import enum
import typing


class QuestionType(enum.IntEnum):
    QUESTION_TYPE_UNSPECIFIED = 0

    QUESTION_TYPE_INTEGER = 1
    QUESTION_TYPE_DECIMAL = 2
    QUESTION_TYPE_STRING = 3
    QUESTION_TYPE_BYTES = 4

    QUESTION_TYPE_SINGLE_CHOICE = 5
    QUESTION_TYPE_SINGLE_CHOICE_ALLOW_OTHER = 6
    QUESTION_TYPE_MULTIPLE_CHOICE = 7
    QUESTION_TYPE_MULTIPLE_CHOICE_ALLOW_OTHER = 8


class Question:
    """An object representing a question."""
    def __init__(self, question: str, question_type: QuestionType, choices: typing.Optional[list[str]] = None) -> None:
        """Constructs a Question object.

        :param question: The question.
        :param question_type: The type of the question.
        :param choices: A list of choices. Ignored if question type is not single or multiple choice.
        """
        self.question = question
        self.question_type = question_type
        self.choices = choices

    def dump(self) -> Question_:
        """Exports the question to a protocol buffer.

        :return: A protocol buffer containing the question's information.
        """
        return Question_(
            question=self.question,
            type=self.question_type.value,
            choices=self.choices
        )

    def dumps(self) -> bytes:
        """Exports the question to a bytestring.

        :return: A bytestring containing the question's information.
        """
        return self.dump().SerializeToString()

    @classmethod
    def load(cls, question: Question_) -> typing.Self:
        """Imports the question from a protocol buffer.

        :param question: A protocol buffer containing the question's information.
        :return: A Question object.
        """
        return cls(
            question=question.question,
            question_type=QuestionType(question.type),
            choices=[choice for choice in question.choices]
        )

    @classmethod
    def loads(cls, question: bytes) -> typing.Self:
        """Imports the question from a bytestring.

        :param question: A bytestring containing the question's information.
        :return: A Question object.
        """
        return cls.load(Question_.FromString(question))


class Response:
    """An object representing a response."""
    def __init__(
            self,
            response_type: QuestionType,
            int_field: typing.Optional[int] = None,
            dec_field: typing.Optional[float] = None,
            string_field: typing.Optional[str] = None,
            bytes_field: typing.Optional[bytes] = None
    ) -> None:
        """Constructs a Response object.

        :param response_type: The type of the response.
        :param int_field: An integer. Optional
        :param dec_field: A float. Optional.
        :param string_field: A string. Optional.
        :param bytes_field: A bytestring. Optional.
        """
        self.response_type = response_type
        self.int_field = int_field
        self.dec_field = dec_field
        self.string_field = string_field
        self.bytes_field = bytes_field

    def dump(self) -> Response_:
        """Exports the response to a protocol buffer.

        :return: A protocol buffer containing the response's information.
        """
        return Response_(
            type=self.response_type.value,
            int_field=self.int_field,
            double_field=self.dec_field,
            string_field=self.string_field,
            bytes_field=self.bytes_field
        )

    def dumps(self) -> bytes:
        """Exports the response to a bytestring.

        :return: A bytestring containing the response's information.
        """
        return self.dump().SerializeToString()

    @classmethod
    def load(cls, response: Response_) -> typing.Self:
        """Imports the response from a protocol buffer.

        :param response: A protocol buffer containing the response's information.
        :return: A Response object.
        """
        return cls(
            response_type=QuestionType(response.type),
            int_field=response.int_field,
            dec_field=response.double_field,
            string_field=response.string_field,
            bytes_field=response.bytes_field
        )

    @classmethod
    def loads(cls, response: bytes) -> typing.Self:
        """Imports the response from a bytestring.

        :param response: A bytestring containing the response's information.
        :return: A Response object.
        """
        return cls.load(Response_.FromString(response))
