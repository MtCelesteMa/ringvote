"""Computes the results of a poll."""

from .ds.polls import Poll
from .ds.ballots import Ballot

import enum


class BallotStatus(enum.Enum):
    VERIFIED = "VERIFIED"
    UNSIGNED = "UNSIGNED"
    SIG_INVALID = "SIGNATURE INVALID"
    DUPLICATE = "DUPLICATE"
    UNKNOWN = "UNKNOWN"


class Result:
    """An object representing the results of a poll."""
    def __init__(self, poll: Poll, ballots: list[Ballot]) -> None:
        """Constructs a Result object.

        :param poll: A poll.
        :param ballots: A list of ballots.
        """
        self.poll = poll
        self.ballots = ballots

    def verify_all(self) -> tuple[list[BallotStatus], list[str | None]]:
        """Determines which ballots are legitimate, and which are forged.

        :return: A list of statuses and names of duplicate voters.
        """
        status = [BallotStatus.UNKNOWN for i in range(len(self.ballots))]
        for i, ballot in enumerate(self.ballots):
            if ballot.signed:
                if ballot.verify():
                    status[i] = BallotStatus.VERIFIED
                else:
                    status[i] = BallotStatus.SIG_INVALID
            else:
                status[i] = BallotStatus.UNSIGNED

        duplicates: list[str | None] = [None for i in range(len(self.ballots))]
        for i, ballot_i in enumerate(self.ballots):
            for j, ballot_j in enumerate(self.ballots):
                if status[i] == status[j] == BallotStatus.VERIFIED:
                    d, name = ballot_i.trace(ballot_j)
                    if d:
                        duplicates[i] = name
                        duplicates[j] = name

        status = [
            BallotStatus.DUPLICATE if duplicates[i] else status[i]
            for i in range(len(self.ballots))
        ]
        return status, duplicates

    def tally_votes(self, only_verified: bool = True) -> list[list[int]]:
        """Counts the votes.

        :param only_verified: Only include verified ballots.
        :return: A list of votes for each choice on each question.
        """
        tally = [[0 for j in range(len(question.choices))] for question in self.poll.questions]
        status, duplicates = self.verify_all()
        for i, ballot in enumerate(self.ballots):
            if only_verified and status[i] != BallotStatus.VERIFIED:
                continue
            for j in range(len(ballot.responses)):
                tally[j][ballot.responses[j]] += 1
        return tally
