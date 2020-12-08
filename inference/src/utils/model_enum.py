from enum import Enum

from src.u2_net.model import U2NET, U2NETP
from src.bas_net.model import BASNet


class Model(Enum):

    U2NET = U2NET  # U2NET
    U2NETP = U2NETP  # U2NETP
    U2NETPORTRAIT = U2NET  # U2NETPORTRAIT
    BASNet = BASNet  # BASNet

    def __str__(self):
        return self.name

    @staticmethod
    def list():
        return [m for m in Model.__members__.keys()]
