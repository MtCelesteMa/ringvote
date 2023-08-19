"""Objects representing questions."""

from .question_pb2 import Question as Question_

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
