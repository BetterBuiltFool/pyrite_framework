from __future__ import annotations

from abc import ABC
import typing

from .. import game

if typing.TYPE_CHECKING:
    from .system import System


class SystemManagable(ABC):

    def add_to_system(self, system_type: type[System]):

        if system := self.get_system(system_type):
            system.register(self)

    def remove_from_system(self, system_type: type[System]):

        if system := self.get_system(system_type):
            system.deregister(self)

    def get_system(self, system_type: type[System]) -> System | None:

        system_manager = game.get_system_manager()
        return system_manager.get_system(system_type)
