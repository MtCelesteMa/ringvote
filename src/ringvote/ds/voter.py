"""Objects representing voters."""

from .voter_pb2 import Voter as Voter_

import typing


class Voter:
    """An object representing a voter."""
    def __init__(self, name: str, extra_info: dict[str, str], public_key: bytes) -> None:
        """Constructs a Voter object.

        :param name: The name of the voter.
        :param extra_info: Extra information about the voter.
        :param public_key: The voter's public key.
        """
        self.name = name
        self.extra_info = extra_info
        self.public_key = public_key

    def dump(self) -> Voter_:
        """Exports the voter to a protocol buffer.

        :return: A protocol buffer containing the voter's information.
        """
        return Voter_(
            name=self.name,
            extra_info=self.extra_info,
            public_key=self.public_key
        )

    def dumps(self) -> bytes:
        """Exports the voter to a bytestring.

        :return: A bytestring containing the voter's information.
        """
        return self.dump().SerializeToString()

    @classmethod
    def load(cls, voter: Voter_) -> typing.Self:
        """Imports the voter from a protocol buffer.

        :param voter: A protocol buffer containing the voter's information.
        :return: A Voter object.
        """
        return cls(
            voter.name,
            {k: v for k, v in voter.extra_info.items()},
            voter.public_key
        )

    @classmethod
    def loads(cls, voter: bytes) -> typing.Self:
        """Imports the voter from a bytestring.

        :param voter: A bytestring containing the voter's information.
        :return: A Voter object.
        """
        return cls.load(Voter_.FromString(voter))
