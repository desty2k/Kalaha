from .CMaximax import CMaximax
from .CMinimax import CMinimax
from .Minimax import Minimax
from .Random import Random

import sys
import inspect
from kalaha.models import Algorithm


def get_algorithms():
    for name, member in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(member, Algorithm) and member is not Algorithm:
            yield member
