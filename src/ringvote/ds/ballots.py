"""Objects representing ballots."""

from .ballot_pb2 import Ballot as _Ballot

from .polls import Poll
from .. import utils

import typing

from crypto_otrs import ring


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

    def sign(self, poll: Poll, public_key: bytes, private_key: bytes) -> None:
        """Signs the ballot using a public and private keypair.

        :param poll: The poll the ballot is part of.
        :param public_key: The public key to sign the ballot with.
        :param private_key: The private key to sign the ballot with.
        """
        pos = -1
        for i in range(len(poll.voters)):
            if public_key == poll.voters[i].public_key:
                pos = i
                break
        assert pos >= 0

        public_keys = [utils.bytes_to_list(voter.public_key) for voter in poll.voters]
        private_key = utils.bytes_to_list(private_key)

        sig = ring.RSign(public_keys, private_key, pos, " ".join(str(response) for response in self.responses).encode())
        self.signature = utils.list_to_bytes(sig)

    def verify(self, poll: Poll) -> bool:
        """Verifies the signature of the ballot.

        :param poll: The poll the ballot is part of.
        :return: True if the signature is legitimate, false otherwise.
        """
        public_keys = [utils.bytes_to_list(voter.public_key) for voter in poll.voters]
        sig = utils.bytes_to_list(self.signature)

        return ring.RVer(public_keys, " ".join(str(response) for response in self.responses).encode(), sig)

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
