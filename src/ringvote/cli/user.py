"""Voter command line interface."""

from ..ds.voters import Voter, Voter_
from ..ds.polls import Poll, Poll_
from ..ds.ballots import Ballot, Ballot_
from .. import utils

import os
import argparse

from crypto_otrs import ring


def cli() -> None:
    arg_parser = argparse.ArgumentParser()
    main_subparser = arg_parser.add_subparsers(title="mode")

    keygen_parser = main_subparser.add_parser("keygen", help="Generates public/private key pairs.")
    keygen_parser.set_defaults(mode="keygen")
    keygen_parser.add_argument("-o", "--out_dir", default=".", help="The directory to output the keys to.")

    profile_parser = main_subparser.add_parser("profile", help="Actions related to voter profiles.")
    profile_parser.set_defaults(mode="profile")
    profile_parser.add_argument("path", help="The path to the voter profile.")
    profile_subparser = profile_parser.add_subparsers(title="action")

    profile_create_parser = profile_subparser.add_parser("create", help="Creates a new voter profile.")
    profile_create_parser.set_defaults(action="create")
    profile_create_parser.add_argument("name", help="Your name.")
    profile_create_parser.add_argument("extra_infos", nargs="*", help="Extra information in the pattern of [title] [content] [title] [content] ...")
    profile_create_parser.add_argument("--key_dir", required=True, help="The directory containing the public key.")

    profile_view_parser = profile_subparser.add_parser("view", help="Displays the voter profile.")
    profile_view_parser.set_defaults(action="view")

    profile_edit_parser = profile_subparser.add_parser("edit", help="Edits the voter profile.")
    profile_edit_parser.set_defaults(action="edit")
    profile_edit_parser.add_argument("--name", help="Your name.")
    profile_edit_parser.add_argument("--extra_infos", nargs="*", help="Extra information in the pattern of [title] [content] [title] [content] ...")
    profile_edit_parser.add_argument("--key_dir", help="The directory containing the public key.")

    poll_parser = main_subparser.add_parser("poll", help="Actions related to polls.")
    poll_parser.set_defaults(mode="poll")
    poll_parser.add_argument("path", help="The path to the poll.")
    poll_subparser = poll_parser.add_subparsers(title="action")

    poll_view_parser = poll_subparser.add_parser("view", help="Displays the poll.")
    poll_view_parser.set_defaults(action="view")

    ballot_parser = main_subparser.add_parser("ballot", help="Actions related to ballots.")
    ballot_parser.set_defaults(mode="ballot")
    ballot_parser.add_argument("path", help="The path to the ballot.")
    ballot_subparser = ballot_parser.add_subparsers(title="action")

    ballot_create_parser = ballot_subparser.add_parser("create", help="Creates a ballot. Remember to sign the ballot afterwards.")
    ballot_create_parser.set_defaults(action="create")
    ballot_create_parser.add_argument("responses", nargs="*", help="The response to each question.")

    ballot_view_parser = ballot_subparser.add_parser("view", help="Views the ballot.")
    ballot_view_parser.set_defaults(action="view")
    ballot_view_parser.add_argument("--poll_path", help="The path to the corresponding poll.")

    ballot_edit_parser = ballot_subparser.add_parser("edit", help="Edits the ballot. Remember to sign the ballot again afterwards.")
    ballot_edit_parser.set_defaults(action="edit")
    ballot_edit_parser.add_argument("responses", nargs="*", help="The response to each question.")

    ballot_sign_parser = ballot_subparser.add_parser("sign", help="Signs the ballot.")
    ballot_sign_parser.set_defaults(action="sign")
    ballot_sign_parser.add_argument("poll_path", help="The path to the corresponding poll.")
    ballot_sign_parser.add_argument("key_dir", help="The directory containing the public and private keys.")

    args = arg_parser.parse_args()


def cli_() -> None:
    arg_parser = argparse.ArgumentParser()
    subparsers = arg_parser.add_subparsers()

    keygen_parser = subparsers.add_parser("keygen", help="Generates public/private key pairs.")
    keygen_parser.set_defaults(mode="keygen")
    keygen_parser.add_argument("-o", "--out_dir", default=".", help="The directory to output the keys to.")

    register_parser = subparsers.add_parser("register", help="Create a voter profile.")
    register_parser.set_defaults(mode="register")
    register_parser.add_argument("key_dir", help="The directory containing the keys. Only the public key is used.")
    register_parser.add_argument("voter_name", help="Your name.")
    register_parser.add_argument("extra_infos", nargs="+", help="Extra information in the pattern of [title] [content] [title] [content] ...")
    register_parser.add_argument("-o", "--out_path", required=True, help="The path to output the profile to.")

    view_parser = subparsers.add_parser("view", help="View the poll.")
    view_parser.set_defaults(mode="view")
    view_parser.add_argument("poll", help="Path to the poll file.")

    vote_parser = subparsers.add_parser("vote", help="Vote on a poll.")
    vote_parser.set_defaults(mode="vote")
    vote_parser.add_argument("poll", help="Path to the poll file.")
    vote_parser.add_argument("key_dir", help="The directory containing the keys.")
    vote_parser.add_argument("responses", nargs="+", type=int, help="The response to each question.")
    vote_parser.add_argument("-o", "--out_path", required=True, help="The path to output the ballot to.")

    args = arg_parser.parse_args()

    if args.mode == "keygen":
        public_key, private_key = ring.keygen()
        public_key, private_key = utils.list_to_bytes(public_key), utils.list_to_bytes(private_key)
        with open(os.path.join(args.out_dir, "public.key"), "wb") as f:
            f.write(public_key)
        with open(os.path.join(args.out_dir, "private.key"), "wb") as f:
            f.write(private_key)
    elif args.mode == "register":
        with open(os.path.join(args.key_dir, "public.key"), "rb") as f:
            public_key = f.read()
        assert len(args.extra_infos) % 2 == 0
        extra_infos = {}
        for i in range(len(args.extra_infos) // 2):
            extra_infos[args.extra_infos[2 * i]] = args.extra_infos[2 * i + 1]
        voter = Voter(args.voter_name, extra_infos, public_key)
        with open(args.out_path, "wb") as f:
            f.write(voter.dump().SerializeToString())
    elif args.mode == "view":
        with open(args.poll, "rb") as f:
            poll = Poll.load(Poll_.FromString(f.read()))
        print(poll.title)
        print()
        for i, question in enumerate(poll.questions):
            print("Q{0:d}: {1:s}".format(i + 1, question.question))
            for j, choice in enumerate(question.choices):
                print("{0:d}. {1:s}".format(j, choice))
            print()
    elif args.mode == "vote":
        with open(args.poll, "rb") as f:
            poll = Poll.load(Poll_.FromString(f.read()))
        with open(os.path.join(args.key_dir, "public.key"), "rb") as f:
            public_key = f.read()
        with open(os.path.join(args.key_dir, "private.key"), "rb") as f:
            private_key = f.read()
        ballot = Ballot(args.responses)
        ballot.sign(poll, public_key, private_key)
        with open(args.out_path, "wb") as f:
            f.write(ballot.dump().SerializeToString())
