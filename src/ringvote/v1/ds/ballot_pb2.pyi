"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Ballot(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESPONSES_FIELD_NUMBER: builtins.int
    SIGNATURE_FIELD_NUMBER: builtins.int
    @property
    def responses(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    signature: builtins.bytes
    def __init__(
        self,
        *,
        responses: collections.abc.Iterable[builtins.int] | None = ...,
        signature: builtins.bytes | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_signature", b"_signature", "signature", b"signature"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_signature", b"_signature", "responses", b"responses", "signature", b"signature"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_signature", b"_signature"]) -> typing_extensions.Literal["signature"] | None: ...

global___Ballot = Ballot
