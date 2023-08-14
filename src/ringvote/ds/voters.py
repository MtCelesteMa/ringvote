"""Objects representing voters."""

from .voter_pb2 import Voter as _Voter

import typing


class Voter:
    """An object representing a voter."""
    def __init__(self, name: str, extra_infos: dict[str, str], public_key: bytes) -> None:
        """Constructs a Voter object.

        :param name: The name of the voter.
        :param extra_infos: Extra information about the voter.
        :param public_key: The voter's public key.
        """
        self.name = name
        self.extra_infos = extra_infos
        self.public_key = public_key

    def dump(self) -> _Voter:
        """Exports the voter to a protocol buffer.

        :return: A protocol buffer containing the voter's information.
        """
        return _Voter(
            name=self.name,
            extra_infos=[
                _Voter.ExtraInfo(title=title, content=content)
                for title, content in self.extra_infos.items()
            ],
            public_key=self.public_key
        )

    @classmethod
    def load(cls, voter: _Voter) -> typing.Self:
        """Imports the voter from a protocol buffer.

        :param voter: A protocol buffer containing the voter's information.
        :return: A Voter object.
        """
        return cls(
            voter.name,
            {extra.title: extra.content for extra in voter.extra_infos},
            voter.public_key
        )
