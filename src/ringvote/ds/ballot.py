"""Objects representing ballots."""

from .ballot_pb2 import Ballot as Ballot_
from .question import Response

import typing


class Ballot:
    """An object representing a ballot."""
    def __init__(self, poll_title: str, responses: list[Response], signature: typing.Optional[bytes] = None) -> None:
        """Constructs a Ballot object.

        :param poll_title: The title of the corresponding poll.
        :param responses: The responses to the questions.
        :param signature: The signature of the ballot. Optional when initializing.
        """
        self.poll_title = poll_title
        self.responses = responses
        self.signature = signature

    @property
    def signed(self) -> bool:
        """Determines whether the ballot is signed.

        :return: True if the ballot is signed, false otherwise.
        """
        return isinstance(self.signature, bytes)

    def dump(self) -> Ballot_:
        """Exports the ballot to a protocol buffer.

        :return: A protocol buffer containing the ballot's information.
        """
        return Ballot_(
            poll_title=self.poll_title,
            responses=[response.dump() for response in self.responses],
            signature=self.signature
        )

    def dumps(self) -> bytes:
        """Exports the ballot to a bytestring.

        :return: A bytestring containing the ballot's information.
        """
        return self.dump().SerializeToString()

    @classmethod
    def load(cls, ballot: Ballot_) -> typing.Self:
        """Imports the ballot from a protocol buffer.

        :param ballot: A protocol buffer containing the ballot's information.
        :return: A Ballot object.
        """
        return cls(
            poll_title=ballot.poll_title,
            responses=[Response.load(response) for response in ballot.responses],
            signature=ballot.signature if ballot.signature else None
        )

    @classmethod
    def loads(cls, ballot: bytes) -> typing.Self:
        """Imports the ballot from a bytestring.

        :param ballot: A bytestring containing the ballot's information.
        :return: A Ballot object.
        """
        return cls.load(Ballot_.FromString(ballot))
