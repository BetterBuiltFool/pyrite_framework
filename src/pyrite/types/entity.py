from ._base_type import _BaseType


class Entity(_BaseType):

    def pre_update(self, delta_time: float) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def post_update(self, delta_time: float) -> None:
        pass

    def const_update(self, delta_time: float) -> None:
        pass
