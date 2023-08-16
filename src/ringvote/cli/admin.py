"""Administrative command line interface."""

from ..ds.voters import Voter, Voter_
from ..ds.polls import Poll, Poll_
from ..ds.questions import Question
from ..ds.ballots import Ballot, Ballot_

import os
import argparse


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
