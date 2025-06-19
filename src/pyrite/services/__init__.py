from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.service import Service as ServiceType

    Service = TypeVar("Service", bound=ServiceType)


def fetch(service_type: type[Service]) -> Service:
    """
    Gets the active service of the given type. If one does not exist, it will be
    started.

    Use the highest-level type of whatever you need access to. The appropriate subclass
    will be returned.

    :param service_type: The type of the service to be fetched.
    :return: An instance of _service_type_
    """
    pass
