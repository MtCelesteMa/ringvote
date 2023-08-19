"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
from . import questions_pb2
import sys
import typing

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Ballot(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    POLL_TITLE_FIELD_NUMBER: builtins.int
    RESPONSES_FIELD_NUMBER: builtins.int
    SIGNATURE_FIELD_NUMBER: builtins.int
    poll_title: builtins.str
    @property
    def responses(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[questions_pb2.Response]: ...
    signature: builtins.bytes
    def __init__(
        self,
        *,
        poll_title: builtins.str | None = ...,
        responses: collections.abc.Iterable[questions_pb2.Response] | None = ...,
        signature: builtins.bytes | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_poll_title", b"_poll_title", "_signature", b"_signature", "poll_title", b"poll_title", "signature", b"signature"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_poll_title", b"_poll_title", "_signature", b"_signature", "poll_title", b"poll_title", "responses", b"responses", "signature", b"signature"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_poll_title", b"_poll_title"]) -> typing_extensions.Literal["poll_title"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_signature", b"_signature"]) -> typing_extensions.Literal["signature"] | None: ...

global___Ballot = Ballot
