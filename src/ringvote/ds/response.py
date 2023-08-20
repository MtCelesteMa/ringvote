"""Objects representing responses."""

from .response_pb2 import Response as Response_
from .question import QuestionType

import typing
import enum
import hashlib


class FieldType(enum.Enum):
    UNKNOWN = "UNKNOWN"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    STRING = "STRING"
    BYTES = "BYTES"
    NONE = "NONE"


class Field:
    """An object representing a field."""
    def __init__(self, data: int | float | str | bytes | None) -> None:
        """Constructs a Field object.

        :param data: The data contained within the field.
        """
        self.data = data

    @property
    def field_type(self) -> FieldType:
        if isinstance(self.data, int):
            return FieldType.INTEGER
        elif isinstance(self.data, float):
            return FieldType.DECIMAL
        elif isinstance(self.data, str):
            return FieldType.STRING
        elif isinstance(self.data, bytes):
            return FieldType.BYTES
        elif isinstance(self.data, type(None)):
            return FieldType.NONE
        return FieldType.UNKNOWN

    def dump(self) -> Response_.Field:
        """Exports the field to a protocol buffer.

        :return: A protocol buffer containing the field's information.
        """
        if self.field_type == FieldType.INTEGER:
            return Response_.Field(int_field=self.data)
        elif self.field_type == FieldType.DECIMAL:
            return Response_.Field(decimal_field=self.data)
        elif self.field_type == FieldType.STRING:
            return Response_.Field(string_field=self.data)
        elif self.field_type == FieldType.BYTES:
            return Response_.Field(bytes_field=self.data)
        elif self.field_type == FieldType.NONE:
            return Response_.Field()
        raise NotImplementedError("field type unsupported.")

    def dumps(self) -> bytes:
        """Exports the field to a bytestring.

        :return: A bytestring containing the field's information.
        """
        return self.dump().SerializeToString()

    @classmethod
    def load(cls, field: Response_.Field) -> typing.Self:
        """Imports the field from a protocol buffer.

        :param field: A protocol buffer containing the field's information.
        :return: A Field object.
        """
        if field.HasField("int_field"):
            return cls(field.int_field)
        elif field.HasField("decimal_field"):
            return cls(field.decimal_field)
        elif field.HasField("string_field"):
            return cls(field.string_field)
        elif field.HasField("bytes_field"):
            return cls(field.bytes_field)
        return cls(None)

    @classmethod
    def loads(cls, field: bytes) -> typing.Self:
        """Imports the field from a bytestring.

        :param field: A bytestring containing the field's information.
        :return: A Field object.
        """
        return cls.load(Response_.Field.FromString(field))


class Response:
    """An object representing a response to a question."""
    def __init__(self, response_type: QuestionType, fields: list[Field]) -> None:
        """Constructs a Response object.

        :param response_type: The type of response.
        :param fields: A list of Fields.
        """
        self.response_type = response_type
        self.fields = fields

    def __bytes__(self) -> bytes:
        hasher = hashlib.sha256()
        for field in self.fields:
            if field.field_type == FieldType.BYTES:
                hasher.update(field.data)
            else:
                hasher.update(str(field.data).encode())
        return hasher.digest()

    def dump(self) -> Response_.Field:
        """Exports the response to a protocol buffer.

        :return: A protocol buffer containing the response's information.
        """
        return Response_(
            type=self.response_type.value,
            fields=[field.dump() for field in self.fields]
        )

    def dumps(self) -> bytes:
        """Exports the response to a bytestring.

        :return: A bytestring containing the response's information.
        """
        return self.dump().SerializeToString()

    @classmethod
    def load(cls, response: Response_) -> typing.Self:
        """Imports the response from a protocol buffer.

        :param response: A protocol buffer containing the response's information.
        :return: A Response object.
        """
        return cls(
            response_type=QuestionType(response.type),
            fields=[Field.load(field) for field in response.fields]
        )

    @classmethod
    def loads(cls, response: bytes) -> typing.Self:
        """Imports the response from a bytestring.

        :param response: A bytestring containing the response's information.
        :return: A Response object.
        """
        return cls.load(Response_.FromString(response))
