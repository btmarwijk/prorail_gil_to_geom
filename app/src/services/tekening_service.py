from pydantic import BaseModel


class Tekeningnaam(BaseModel):
    naam: str
    discipline: str


class TekeningnaamService:
    def __init__(self):
        pass

    def _check_existing(self):
        pass

    def parse_file(self):
        pass
