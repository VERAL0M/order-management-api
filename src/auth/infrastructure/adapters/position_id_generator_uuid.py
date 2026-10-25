from uuid import UUID, uuid4

from auth.application.interfaces.position_id_generator import PositionIdGenerator

class PositionIdGeneratorImpl(PositionIdGenerator):
    def __call__(self) -> UUID:
        return uuid4()
        