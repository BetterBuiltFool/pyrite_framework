from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Service(ABC):

    @abstractmethod
    def transfer(self, target_service: Service):
        """
        Packages and transmits all pertinent stored data from the current service to
        the target service.

        __init__ should take no parameters, as it may be spawned automatically.

        :param target_service: A Service that is compatible with the current service,
            usually by a shared parent.
        """
