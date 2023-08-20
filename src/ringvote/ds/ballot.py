"""Objects representing ballots."""

from .ballot_pb2 import Ballot as Ballot_
from .response import Response
from .. import utils

import typing
import hashlib

from crypto_otrs import ring


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

    def check_format(self) -> bool:
        """Checks if the response format is valid. THIS DOES NOT DETERMINE WHETHER THE SIGNATURE IS VALID!

        :return: True if all the responses have valid formats, false otherwise.
        """
        for response in self.responses:
            if not response.check_format():
                return False
        return True

    def repr_responses(self) -> bytes:
        return hashlib.sha256(b" ".join(response.hash() for response in self.responses)).digest()

    def sign(self, key_ring: list[bytes], public_key: bytes, private_key: bytes) -> bytes:
        """Signs the ballot using a public and private keypair.

        :param key_ring: A list containing every voter's public key.
        :param public_key: The public key to sign the ballot with. Must be in key_ring.
        :param private_key: The private key to sign the ballot with.
        :return: The signature of the ballot.
        """
        pos = -1
        for i, key in enumerate(key_ring):
            if key == public_key:
                pos = i
                break
        if pos < 0:
            raise KeyError("public key not found in key ring.")

        key_ring = [utils.bytes_to_list(key) for key in key_ring]
        private_key = utils.bytes_to_list(private_key)

        sig = ring.RSign(key_ring, private_key, pos, self.repr_responses())
        self.signature = utils.list_to_bytes(sig)
        return self.signature

    def verify(self, key_ring: list[bytes]) -> bool:
        """Verifies the signature of the ballot.

        :param key_ring: A list containing every voter's public key.
        :return: True if the signature is valid, false otherwise.
        """
        key_ring = [utils.bytes_to_list(key) for key in key_ring]
        sig = utils.bytes_to_list(self.signature)

        return ring.RVer(key_ring, self.repr_responses(), sig)

    def trace(self, key_ring: list[bytes], other: typing.Self) -> tuple[bool, bytes | None]:
        """Determines if the two ballots are signed by the same voter.

        :param key_ring: A list containing every voter's public key.
        :param other: Another ballot.
        :return: If they are signed by the same person, return true along with their public key. False otherwise.
        """
        key_ring = [utils.bytes_to_list(key) for key in key_ring]
        sig_a, sig_b = utils.bytes_to_list(self.signature), utils.bytes_to_list(other.signature)

        is_duplicate, traced_key = ring.RTrace(key_ring, sig_a, sig_b)
        if is_duplicate:
            return True, utils.list_to_bytes(traced_key)
        return False, None

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
