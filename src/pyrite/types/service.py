from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class ServiceProvider(ABC):
    """
    Class for providing access to a given service. The ServiceProvider will delegate
    out to the active version of the service. This way, services are runtime swappable,
    without changing the access point for users of that service.
    """

    _service: Service

    @abstractmethod
    def hotswap(cls, service: Service):
        """
        Changes the ServiceProvider's active service, transferring vital data to the
        new service instance.

        :param service: The new instance of the service used by the service provider.
        """


class Service(ABC):
    """
    Controls data and provides methods for various objects in a way that is runtime
    swappable. Objects use the appropriate ServiceProvider to access a service.
    """

    @abstractmethod
    def transfer(self, target_service: Service):
        """
        Packages and transmits all pertinent stored data from the current service to
        the target service.

        __init__ should take no parameters, as it may be spawned automatically.

        :param target_service: A Service that is compatible with the current service,
            usually by a shared parent.
        """
