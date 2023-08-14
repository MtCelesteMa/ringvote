"""Objects representing ballots."""

from .ballot_pb2 import Ballot as _Ballot

import typing


class Ballot:
    """An object representing a ballot."""
    def __init__(self, responses: list[int], signature: typing.Optional[bytes] = None) -> None:
        """Constructs a Ballot object.

        :param responses: A list of responses.
        :param signature: The signature of the ballot.
        """
        self.responses = responses
        self.signature = signature

    @property
    def signed(self) -> bool:
        """Whether the ballot is signed.

        :return: True if the ballot is signed, false otherwise.
        """
        return isinstance(self.signature, bytes)

    def dump(self) -> _Ballot:
        """Exports the ballot to a protocol buffer.

        :return: A protocol buffer containing the ballot's information.
        """
        return _Ballot(
            responses=self.responses,
            signature=self.signature
        )

    @classmethod
    def load(cls, ballot: _Ballot) -> typing.Self:
        return cls(
            [response for response in ballot.responses],
            ballot.signature if ballot.signature else None
        )
