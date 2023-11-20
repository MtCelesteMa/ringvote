"""Utility functions for RingVote"""

SER_LEN_BYTES = 8


def list_to_bytes(a: list[int]) -> bytes:
    """Converts a list of 8-bit integers to a bytestring.

    :param a: A list of 8-bit integers.
    :return: The corresponding bytestring.
    """
    assert max(a) <= 255 and min(a) >= 0
    return b"".join(int.to_bytes(a_) for a_ in a)


def bytes_to_list(b: bytes) -> list[int]:
    """Converts a bytestring to a list of 8-bit integers.

    :param b: A bytestring.
    :return: The corresponding list of 8-bit integers.
    """
    return [b_ for b_ in b]


def serialize_bl(a: list[bytes]) -> bytes:
    """Serializes a list of bytestrings.

    :param a: A list of bytestrings.
    :return: A serialized list of bytestrings.
    """
    return b"".join(int.to_bytes(len(a_), SER_LEN_BYTES) + a_ for a_ in a)


def deserialize_bl(b: bytes) -> list[bytes]:
    """Deserializes a list of bytestrings.

    :param b: A serialized list of bytestrings.
    :return: A list of bytestrings.
    """
    a: list[bytes] = []
    i = 0
    while i < len(b):
        s = int.from_bytes(b[i:i + SER_LEN_BYTES])
        i += SER_LEN_BYTES
        a.append(b[i:i + s])
        i += s
    return a
