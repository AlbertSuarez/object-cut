from enum import Enum

from src.u2_net.model import U2NET
from src.bas_net.model import BASNet


class Model(Enum):

    U2NET = U2NET  # U2NET
    BASNet = BASNet  # BASNet

    def __str__(self):
        return self.name

    @staticmethod
    def list():
        return [m.name for m in Model]
