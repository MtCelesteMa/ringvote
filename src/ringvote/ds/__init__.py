"""Common data structures."""

from .voter_pb2 import Voter as Voter_
from .question_pb2 import Question as Question_
from .response_pb2 import Response as Response_
from .ballot_pb2 import Ballot as Ballot_
from .poll_pb2 import Poll as Poll_

from .voter import Voter
from .question import QuestionType, Question
from .response import Response
from .ballot import Ballot
from .poll import Poll

