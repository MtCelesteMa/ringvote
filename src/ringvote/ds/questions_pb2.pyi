"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _QuestionType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _QuestionTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_QuestionType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    QUESTION_TYPE_UNSPECIFIED: _QuestionType.ValueType  # 0
    QUESTION_TYPE_INTEGER: _QuestionType.ValueType  # 1
    QUESTION_TYPE_DECIMAL: _QuestionType.ValueType  # 2
    QUESTION_TYPE_STRING: _QuestionType.ValueType  # 3
    QUESTION_TYPE_BYTES: _QuestionType.ValueType  # 4
    QUESTION_TYPE_SINGLE_CHOICE: _QuestionType.ValueType  # 5
    QUESTION_TYPE_SINGLE_CHOICE_ALLOW_OTHER: _QuestionType.ValueType  # 6
    QUESTION_TYPE_MULTIPLE_CHOICE: _QuestionType.ValueType  # 7
    QUESTION_TYPE_MULTIPLE_CHOICE_ALLOW_OTHER: _QuestionType.ValueType  # 8

class QuestionType(_QuestionType, metaclass=_QuestionTypeEnumTypeWrapper): ...

QUESTION_TYPE_UNSPECIFIED: QuestionType.ValueType  # 0
QUESTION_TYPE_INTEGER: QuestionType.ValueType  # 1
QUESTION_TYPE_DECIMAL: QuestionType.ValueType  # 2
QUESTION_TYPE_STRING: QuestionType.ValueType  # 3
QUESTION_TYPE_BYTES: QuestionType.ValueType  # 4
QUESTION_TYPE_SINGLE_CHOICE: QuestionType.ValueType  # 5
QUESTION_TYPE_SINGLE_CHOICE_ALLOW_OTHER: QuestionType.ValueType  # 6
QUESTION_TYPE_MULTIPLE_CHOICE: QuestionType.ValueType  # 7
QUESTION_TYPE_MULTIPLE_CHOICE_ALLOW_OTHER: QuestionType.ValueType  # 8
global___QuestionType = QuestionType

@typing_extensions.final
class Question(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    QUESTION_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    CHOICES_FIELD_NUMBER: builtins.int
    question: builtins.str
    type: global___QuestionType.ValueType
    @property
    def choices(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        question: builtins.str | None = ...,
        type: global___QuestionType.ValueType | None = ...,
        choices: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_question", b"_question", "_type", b"_type", "question", b"question", "type", b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_question", b"_question", "_type", b"_type", "choices", b"choices", "question", b"question", "type", b"type"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_question", b"_question"]) -> typing_extensions.Literal["question"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_type", b"_type"]) -> typing_extensions.Literal["type"] | None: ...

global___Question = Question

@typing_extensions.final
class Response(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TYPE_FIELD_NUMBER: builtins.int
    INT_FIELD_FIELD_NUMBER: builtins.int
    DOUBLE_FIELD_FIELD_NUMBER: builtins.int
    STRING_FIELD_FIELD_NUMBER: builtins.int
    BYTES_FIELD_FIELD_NUMBER: builtins.int
    type: global___QuestionType.ValueType
    int_field: builtins.int
    double_field: builtins.float
    string_field: builtins.str
    bytes_field: builtins.bytes
    def __init__(
        self,
        *,
        type: global___QuestionType.ValueType | None = ...,
        int_field: builtins.int | None = ...,
        double_field: builtins.float | None = ...,
        string_field: builtins.str | None = ...,
        bytes_field: builtins.bytes | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_bytes_field", b"_bytes_field", "_double_field", b"_double_field", "_int_field", b"_int_field", "_string_field", b"_string_field", "_type", b"_type", "bytes_field", b"bytes_field", "double_field", b"double_field", "int_field", b"int_field", "string_field", b"string_field", "type", b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_bytes_field", b"_bytes_field", "_double_field", b"_double_field", "_int_field", b"_int_field", "_string_field", b"_string_field", "_type", b"_type", "bytes_field", b"bytes_field", "double_field", b"double_field", "int_field", b"int_field", "string_field", b"string_field", "type", b"type"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_bytes_field", b"_bytes_field"]) -> typing_extensions.Literal["bytes_field"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_double_field", b"_double_field"]) -> typing_extensions.Literal["double_field"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_int_field", b"_int_field"]) -> typing_extensions.Literal["int_field"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_string_field", b"_string_field"]) -> typing_extensions.Literal["string_field"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_type", b"_type"]) -> typing_extensions.Literal["type"] | None: ...

global___Response = Response