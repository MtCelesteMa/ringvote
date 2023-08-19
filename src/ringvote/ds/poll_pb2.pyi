"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
from . import question_pb2
import sys
from . import voter_pb2

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Poll(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TITLE_FIELD_NUMBER: builtins.int
    QUESTIONS_FIELD_NUMBER: builtins.int
    VOTERS_FIELD_NUMBER: builtins.int
    title: builtins.str
    @property
    def questions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[question_pb2.Question]: ...
    @property
    def voters(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[voter_pb2.Voter]: ...
    def __init__(
        self,
        *,
        title: builtins.str | None = ...,
        questions: collections.abc.Iterable[question_pb2.Question] | None = ...,
        voters: collections.abc.Iterable[voter_pb2.Voter] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_title", b"_title", "title", b"title"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_title", b"_title", "questions", b"questions", "title", b"title", "voters", b"voters"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_title", b"_title"]) -> typing_extensions.Literal["title"] | None: ...

global___Poll = Poll
