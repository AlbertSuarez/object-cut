from enum import Enum

from src.u2_net.model import U2NET
from src.bas_net.model import BASNet


class Model(Enum):

    u2net = U2NET  # Full size version 173.6 MB
    basnet = BASNet  # Small version u2net 4.7 MB

    def __str__(self):
        return self.name

    @staticmethod
    def list():
        return [m.name for m in Model]