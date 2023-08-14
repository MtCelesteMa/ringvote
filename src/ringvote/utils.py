"""Utility functions for RingVote"""


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
