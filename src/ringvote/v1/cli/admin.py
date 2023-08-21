"""Administrative command line interface."""

from ..ds.voters import Voter, Voter_
from ..ds.polls import Poll, Poll_
from ..ds.questions import Question
from ..ds.ballots import Ballot, Ballot_
from ..results import Result, BallotStatus

import argparse
import glob


def cli() -> None:
    arg_parser = argparse.ArgumentParser()
    main_subparser = arg_parser.add_subparsers(title="mode")

    poll_parser = main_subparser.add_parser("poll", help="Administrative actions related to polls.")
    poll_parser.set_defaults(mode="poll")
    poll_parser.add_argument("path", help="The path to the poll.")
    poll_subparser = poll_parser.add_subparsers(title="action")

    poll_create_parser = poll_subparser.add_parser("create", help="Creates a new poll.")
    poll_create_parser.set_defaults(action="create")
    poll_create_parser.add_argument("title", help="The title of the poll.")

    poll_add_parser = poll_subparser.add_parser("add", help="Adds a question or voter to the poll.")
    poll_add_parser.set_defaults(action="add")
    poll_add_subparser = poll_add_parser.add_subparsers(title="item")

    poll_add_question_parser = poll_add_subparser.add_parser("question", help="Adds a question to the poll.")
    poll_add_question_parser.set_defaults(item="question")
    poll_add_question_parser.add_argument("question", help="The question.")
    poll_add_question_parser.add_argument("choices", nargs="+", help="The choices to the question.")

    poll_add_voter_parser = poll_add_subparser.add_parser("voter", help="Adds a voter to the poll.")
    poll_add_voter_parser.set_defaults(item="voter")
    poll_add_voter_parser.add_argument("profile_path", help="The path to the voter's profile.")

    poll_edit_parser = poll_subparser.add_parser("edit", help="Edits a question in a poll.")
    poll_edit_parser.set_defaults(action="edit")
    poll_edit_subparser = poll_edit_parser.add_subparsers(title="item")

    poll_edit_question_parser = poll_edit_subparser.add_parser("question", help="Edits a question in the poll.")
    poll_edit_question_parser.set_defaults(item="question")
    poll_edit_question_parser.add_argument("index", type=int, help="The index of the question to edit.")
    poll_edit_question_parser.add_argument("--question", help="The question.")
    poll_edit_question_parser.add_argument("--choices", nargs="+", help="The choices to the question.")

    poll_remove_parser = poll_subparser.add_parser("remove", help="Removes a question or voter from the poll.")
    poll_remove_parser.set_defaults(action="remove")
    poll_remove_subparser = poll_remove_parser.add_subparsers(title="item")

    poll_remove_question_parser = poll_remove_subparser.add_parser("question", help="Removes a question from the poll.")
    poll_remove_question_parser.set_defaults(item="question")
    poll_remove_question_parser.add_argument("index", type=int, help="The index of the question to remove.")

    poll_remove_voter_parser = poll_remove_subparser.add_parser("voter", help="Removes a voter from the poll.")
    poll_remove_voter_parser.set_defaults(item="voter")
    poll_remove_voter_parser.add_argument("voter_name", help="The name of the voter to remove.")

    poll_results_parser = poll_subparser.add_parser("results", help="Display the results of the poll.")
    poll_results_parser.set_defaults(action="results")
    poll_results_parser.add_argument("ballots_path", help="Glob pattern of the paths to the ballots.")

    args = arg_parser.parse_args()

    if args.mode == "poll":
        if args.action == "create":
            poll = Poll(args.title, [], [])
            with open(args.path, "wb") as f:
                f.write(poll.dump().SerializeToString())
        else:
            with open(args.path, "rb") as f:
                poll = Poll.load(Poll_.FromString(f.read()))
            if args.action == "add":
                if args.item == "question":
                    poll.questions.append(Question(args.question, args.choices))
                elif args.item == "voter":
                    profiles = glob.glob(args.profile_path)
                    for profile in profiles:
                        with open(profile, "rb") as f:
                            voter = Voter.load(Voter_.FromString(f.read()))
                        poll.voters.append(voter)
                with open(args.path, "wb") as f:
                    f.write(poll.dump().SerializeToString())
            elif args.action == "edit":
                if args.item == "question":
                    if args.question:
                        poll.questions[args.index - 1].question = args.question
                    if args.choices:
                        poll.questions[args.index - 1].choices = args.choices
                with open(args.path, "wb") as f:
                    f.write(poll.dump().SerializeToString())
            elif args.action == "remove":
                if args.item == "question":
                    poll.questions.pop(args.index - 1)
                elif args.item == "voter":
                    for i, voter in enumerate(poll.voters):
                        if voter.name == args.voter_name:
                            poll.voters.pop(i)
                            break
                with open(args.path, "wb") as f:
                    f.write(poll.dump().SerializeToString())
            elif args.action == "results":
                ballots = []
                for ballot_path in glob.glob(args.ballots_path):
                    with open(ballot_path, "rb") as f:
                        ballots.append(Ballot.load(Ballot_.FromString(f.read())))
                result = Result(poll, ballots)

                print("Results:")
                tally = result.tally_votes()
                for i, question in enumerate(poll.questions):
                    print("Q{0:d}: {1:s}".format(i + 1, question.question))
                    for j, choice in enumerate(question.choices):
                        print("{0:d}. {1:s} : {2:d} votes".format(j, choice, tally[i][j]))
                    print()

                print("Fraudulent Ballots:\n")
                status, names = result.verify_all()
                for i, ballot in enumerate(result.ballots):
                    if status[i] == BallotStatus.VERIFIED:
                        continue
                    print("Responses: {0:s}".format(str(ballot.responses)))
                    print("Status: {0:s}".format(status[i]))
                    if status[i] == BallotStatus.DUPLICATE:
                        print("Voter name: {0:s}".format(names[i]))
                    print()
