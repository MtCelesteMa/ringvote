"""Objects representing questions."""

from .poll_pb2 import Poll as Poll_

import typing


class Question:
    """An object representing a question."""
    def __init__(self, question: str, choices: list[str]) -> None:
        """Constructs a Question object.

        :param question: The content of the question.
        :param choices: A list of choices.
        """
        self.question = question
        self.choices = choices

    def dump(self) -> Poll_.Question:
        """Exports the question to a protocol buffer.

        :return: A protocol buffer containing the question's information.
        """
        return Poll_.Question(
            question=self.question,
            choices=self.choices
        )

    @classmethod
    def load(cls, question: Poll_.Question) -> typing.Self:
        """Imports the question from a protocol buffer.

        :param question: A protocol buffer containing the question's information.
        :return: A Question object.
        """
        return cls(
            question.question,
            [choice for choice in question.choices]
        )

