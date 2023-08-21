"""Objects representing ballots."""

from .ballot_pb2 import Ballot as Ballot_

from .polls import Poll
from ... import utils

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

    def check(self, poll: Poll) -> bool:
        """Checks if the responses are valid. THIS DOES NOT DETERMINE WHETHER THE SIGNATURE IS VALID!

        :param poll: The corresponding poll.
        :return: True if the responses are valid, false otherwise.
        """
        if len(self.responses) != len(poll.questions):
            return False
        for response, question in zip(self.responses, poll.questions):
            if response < 0 or response >= len(question.choices):
                return False
        return True

    @property
    def signed(self) -> bool:
        """Whether the ballot is signed.

        :return: True if the ballot is signed, false otherwise.
        """
        return isinstance(self.signature, bytes)

    def sign(self, poll: Poll, public_key: bytes, private_key: bytes) -> None:
        """Signs the ballot using a public and private keypair.

        :param poll: The poll associated with the ballot.
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

        :param poll: The poll associated with the ballot.
        :return: True if the signature is legitimate, false otherwise.
        """
        public_keys = [utils.bytes_to_list(voter.public_key) for voter in poll.voters]
        sig = utils.bytes_to_list(self.signature)

        return ring.RVer(public_keys, " ".join(str(response) for response in self.responses).encode(), sig)

    def trace(self, poll: Poll, other: typing.Self) -> tuple[bool, str | None]:
        """Determines if the two ballots are signed by the same voter.

        :param poll: The poll associated with the ballot.
        :param other: Another ballot.
        :return: If they are signed by the same person, return true along with their name. False otherwise.
        """
        public_keys = [utils.bytes_to_list(voter.public_key) for voter in poll.voters]
        sig_a, sig_b = utils.bytes_to_list(self.signature), utils.bytes_to_list(other.signature)

        d, k = ring.RTrace(public_keys, sig_a, sig_b)
        if d:
            name = {voter.public_key: voter.name for voter in poll.voters}[utils.list_to_bytes(k)]
            return True, name
        return False, None

    def dump(self) -> Ballot_:
        """Exports the ballot to a protocol buffer.

        :return: A protocol buffer containing the ballot's information.
        """
        return Ballot_(
            responses=self.responses,
            signature=self.signature
        )

    @classmethod
    def load(cls, ballot: Ballot_) -> typing.Self:
        return cls(
            [response for response in ballot.responses],
            ballot.signature if ballot.signature else None
        )
