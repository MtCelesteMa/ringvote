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
