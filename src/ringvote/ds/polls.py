"""Objects representing polls."""

from .poll_pb2 import Poll as _Poll

from .voters import Voter
from .questions import Question

import typing


class Poll:
    """An object representing a poll."""

    def __init__(self, title: str, questions: list[Question], voters: list[Voter]) -> None:
        """Constructs a Poll object.

        :param title: The title of the poll.
        :param questions: A list of questions.
        :param voters: A list of voters participating in the poll.
        """
        self.title = title
        self.questions = questions
        self.voters = voters

    def dump(self) -> _Poll:
        """Exports the poll to a protocol buffer.

        :return: A protocol buffer containing the poll's information.
        """
        return _Poll(
            title=self.title,
            questions=[question.dump() for question in self.questions],
            voters=[voter.dump() for voter in self.voters]
        )

    @classmethod
    def load(cls, poll: _Poll) -> typing.Self:
        """Imports the question from a protocol buffer.

        :param poll: A protocol buffer containing the poll's information.
        :return: A Poll object.
        """
        return cls(
            poll.title,
            [Question.load(question) for question in poll.questions],
            [Voter.load(voter) for voter in poll.voters]
        )
