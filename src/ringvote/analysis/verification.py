"""Processor for processing finished polls."""

from ..ds import QuestionType, Poll, Ballot

import enum


class BallotStatus(enum.Enum):
    UNKNOWN = "UNKNOWN"
    FMT_INVALID = "FORMAT INVALID"
    UNSIGNED = "UNSIGNED"
    SIG_INVALID = "SIGNATURE INVALID"
    DUPLICATE = "DUPLICATE"
    VERIFIED = "VERIFIED"


def check_format(poll: Poll, ballot: Ballot) -> bool:
    """Checks if a ballot's response format is valid. THIS DOES NOT DETERMINE WHETHER THE SIGNATURES ARE VALID!

    :param poll: A poll.
    :param ballot: A ballot.
    :return: True if the response format is valid, false otherwise.
    """
    if not ballot.check_format():
        return False
    if poll.title != ballot.poll_title:
        return False
    for question, response in zip(poll.questions, ballot.responses):
        if question.question_type != response.response_type:
            return False
        if question.question_type == QuestionType.QUESTION_TYPE_SINGLE_CHOICE \
                or question.question_type == QuestionType.QUESTION_TYPE_SINGLE_CHOICE_ALLOW_OTHER:
            if response.fields[0].data < 0 or response.fields[0].data >= len(question.choices):
                return False
        elif question.question_type == QuestionType.QUESTION_TYPE_MULTIPLE_CHOICE \
                or question.question_type == QuestionType.QUESTION_TYPE_MULTIPLE_CHOICE_ALLOW_OTHER:
            if response.fields[0].data < 0 or response.fields[0].data >= 1 << len(question.choices):
                return False
    return True


def verify_all(poll: Poll, ballots: list[Ballot]) -> tuple[list[BallotStatus], list[str | None]]:
    """Determines the status of each ballot.

    :param poll: A poll.
    :param ballots: A list of ballots.
    :return: A list of statuses and names of duplicate voters.
    """
    statuses = [BallotStatus.UNKNOWN for _ in range(len(ballots))]
    key_ring = [voter.public_key for voter in poll.voters]
    for i, ballot in enumerate(ballots):
        if check_format(poll, ballot):
            if ballot.signed:
                if ballot.verify(key_ring):
                    statuses[i] = BallotStatus.VERIFIED
                else:
                    statuses[i] = BallotStatus.SIG_INVALID
            else:
                statuses[i] = BallotStatus.UNSIGNED
        else:
            statuses[i] = BallotStatus.FMT_INVALID

    duplicate_names: list[str | None] = [None for _ in range(len(ballots))]
    name_lookup = {voter.public_key: voter.name for voter in poll.voters}
    for i, ballot_i in enumerate(ballots):
        for j, ballot_j in enumerate(ballots):
            if statuses[i] == statuses[j] == BallotStatus.VERIFIED:
                is_dup, traced_key = ballot_i.trace(key_ring, ballot_j)
                if is_dup:
                    duplicate_names[i] = name_lookup[traced_key]
                    duplicate_names[j] = name_lookup[traced_key]

    statuses = [
        BallotStatus.DUPLICATE if duplicate_names[i] else statuses[i]
        for i in range(len(ballots))
    ]
    return statuses, duplicate_names
