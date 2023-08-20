"""Processor for processing finished polls."""

from .ds import QuestionType, Poll, Ballot

import enum


class SignatureStatus(enum.Enum):
    UNKNOWN = "UNKNOWN"
    VERIFIED = "VERIFIED"
    UNSIGNED = "UNSIGNED"
    SIG_INVALID = "SIGNATURE INVALID"
    DUPLICATE = "DUPLICATE"


class Postprocessor:
    """A processor for processing finished polls."""

    def __init__(self, poll: Poll, ballots: list[Ballot]) -> None:
        """Constructs a Postprocessor object.

        :param poll: A poll.
        :param ballots: A list of ballots.
        """
        self.poll = poll
        self.ballots = ballots

    def check_all(self) -> list[bool]:
        """Determines which ballots have valid formats. THIS DOES NOT DETERMINE WHETHER THE SIGNATURES ARE VALID!

        :return: A list of bools. True if the ballot format is valid, false otherwise.
        """
        statuses = []
        for ballot in self.ballots:
            status = True
            if not ballot.check_format():
                status = False
            if self.poll.title != ballot.poll_title:
                status = False
            for question, response in zip(self.poll.questions, ballot.responses):
                if question.question_type != response.response_type:
                    status = False
                if question.question_type == QuestionType.QUESTION_TYPE_SINGLE_CHOICE \
                        or question.question_type == QuestionType.QUESTION_TYPE_SINGLE_CHOICE_ALLOW_OTHER:
                    if response.fields[0].data < 0 or response.fields[0].data >= len(question.choices):
                        status = False
                elif question.question_type == QuestionType.QUESTION_TYPE_MULTIPLE_CHOICE \
                        or question.question_type == QuestionType.QUESTION_TYPE_MULTIPLE_CHOICE_ALLOW_OTHER:
                    if response.fields[0].data < 0 or response.fields[0].data >= 1 << len(question.choices):
                        status = False
            statuses.append(status)
        return statuses

    def verify_all(self) -> tuple[list[SignatureStatus], list[str | None]]:
        """Determines which ballots are legitimate, and which are forged.

        :return: A list of statuses and names of duplicate voters.
        """
        statuses = [SignatureStatus.UNKNOWN for _ in range(len(self.ballots))]
        key_ring = [voter.public_key for voter in self.poll.voters]
        for i, ballot in enumerate(self.ballots):
            if ballot.signed:
                if ballot.verify(key_ring):
                    statuses[i] = SignatureStatus.VERIFIED
                else:
                    statuses[i] = SignatureStatus.SIG_INVALID
            else:
                statuses[i] = SignatureStatus.UNSIGNED

        duplicate_names: list[str | None] = [None for _ in range(len(self.ballots))]
        name_lookup = {voter.public_key: voter.name for voter in self.poll.voters}
        for i, ballot_i in enumerate(self.ballots):
            for j, ballot_j in enumerate(self.ballots):
                if statuses[i] == statuses[j] == SignatureStatus.VERIFIED:
                    is_dup, traced_key = ballot_i.trace(key_ring, ballot_j)
                    if is_dup:
                        duplicate_names[i] = name_lookup[traced_key]
                        duplicate_names[j] = name_lookup[traced_key]

        statuses = [
            SignatureStatus.DUPLICATE if duplicate_names[i] else statuses[i]
            for i in range(len(self.ballots))
        ]
        return statuses, duplicate_names
