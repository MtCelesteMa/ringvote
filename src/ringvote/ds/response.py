"""Objects representing responses."""

from .response_pb2 import Response as Response_
from .question import QuestionType

import typing


class Response:
    """An object representing a response."""
    def __init__(
            self,
            response_type: QuestionType,
            int_field: typing.Optional[int] = None,
            dec_field: typing.Optional[float] = None,
            string_field: typing.Optional[str] = None,
            bytes_field: typing.Optional[bytes] = None
    ) -> None:
        """Constructs a Response object.

        :param response_type: The type of the response.
        :param int_field: An integer. Optional
        :param dec_field: A float. Optional.
        :param string_field: A string. Optional.
        :param bytes_field: A bytestring. Optional.
        """
        self.response_type = response_type
        self.int_field = int_field
        self.dec_field = dec_field
        self.string_field = string_field
        self.bytes_field = bytes_field

    def dump(self) -> Response_:
        """Exports the response to a protocol buffer.

        :return: A protocol buffer containing the response's information.
        """
        return Response_(
            type=self.response_type.value,
            int_field=self.int_field,
            double_field=self.dec_field,
            string_field=self.string_field,
            bytes_field=self.bytes_field
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
            int_field=response.int_field,
            dec_field=response.double_field,
            string_field=response.string_field,
            bytes_field=response.bytes_field
        )

    @classmethod
    def loads(cls, response: bytes) -> typing.Self:
        """Imports the response from a bytestring.

        :param response: A bytestring containing the response's information.
        :return: A Response object.
        """
        return cls.load(Response_.FromString(response))

