"""Objects representing polls."""

from .poll_pb2 import Poll as Poll_
from .question import Question
from .voter import Voter

import typing


class Poll:
    """An object representing a poll."""
    def __init__(self, title: str, questions: list[Question], voters: list[Voter]) -> None:
        """Constructs a Poll object.

        :param title: The title of the poll.
        :param questions: The list of questions.
        :param voters: The list of voters.
        """
        self.title = title
        self.questions = questions
        self.voters = voters

    def dump(self) -> Poll_:
        """Exports the poll as a protocol buffer.

        :return: A protocol buffer containing the poll's information.
        """
        return Poll_(
            title=self.title,
            questions=[question.dump() for question in self.questions],
            voters=[voter.dump() for voter in self.voters]
        )

    def dumps(self) -> bytes:
        """Exports the poll as a bytestring.

        :return: A bytestring containing the poll's information.
        """
        return self.dump().SerializeToString()

    @classmethod
    def load(cls, poll: Poll_) -> typing.Self:
        """Imports the poll from a protocol buffer.

        :param poll: A protocol buffer containing the poll's information.
        :return: A Poll object.
        """
        return cls(
            title=poll.title,
            questions=[Question.load(question) for question in poll.questions],
            voters=[Voter.load(voter) for voter in poll.voters]
        )

    @classmethod
    def loads(cls, poll: bytes) -> typing.Self:
        """Imports the poll from a bytestring.

        :param poll: A bytestring containing the poll's information.
        :return: A Poll object.
        """
        return cls.load(Poll_.FromString(poll))
