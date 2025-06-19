from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.service import Service as ServiceType

    Service = TypeVar("Service", bound=ServiceType)


class ServiceManager:

    def __init__(self) -> None:
        self.services: dict[type[Service], Service] = {}

    def get_service(self, service_type: type[Service]) -> Service:
        return self.services.get(service_type)

    def start_service(self, service_type: type[Service]) -> Service:
        # TODO Go through the rigamarole of figuring out how to get the specific
        # subclass.
        return service_type()


# Keep one in memory so long as the module is loaded.
service_manager = ServiceManager()


def fetch(service_type: type[Service]) -> Service:
    """
    Gets the active service of the given type. If one does not exist, it will be
    started.

    Use the highest-level type of whatever you need access to. The appropriate subclass
    will be returned.

    :param service_type: The type of the service to be fetched.
    :return: An instance of _service_type_
    """
    if (service := service_manager.get_service(service_type)) is None:
        service = service_manager.start_service(service_type)
    return service
