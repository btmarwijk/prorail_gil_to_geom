from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .upload_model import Upload
    from .versie_model import Versie


class Tekening(Base):
    __tablename__ = "tekeningen"

    id: Mapped[int] = mapped_column(primary_key=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("upload.id"))
    naam: Mapped[str] = mapped_column(String(100))

    upload: Mapped["Upload"] = relationship(back_populates="tekeningen")
    versies: Mapped[List["Versie"]] = relationship(back_populates="tekening")
