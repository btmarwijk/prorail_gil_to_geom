from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import TimestampMixin
from .spoorkabel_versie_relation import SpoorkabelVersieDetail

if TYPE_CHECKING:
    from .tekening_model import Tekening


class Versie(Base):
    __tablename__ = "versies"

    id: Mapped[int] = mapped_column(primary_key=True)
    tekening_id: Mapped[int] = mapped_column(
        ForeignKey("tekeningen.id"), nullable=False
    )
    versie_type: Mapped[str] = mapped_column(String(32))

    # Relaties
    tekening: Mapped["Tekening"] = relationship("Tekening", back_populates="versies")
    spoorkabel_details: Mapped[list["SpoorkabelVersieDetail"]] = relationship(
        "SpoorkabelVersieDetail", back_populates="versie"
    )

    __mapper_args__ = {"polymorphic_on": "versie_type", "polymorphic_identity": "base"}


class VersieBestaand(TimestampMixin, Versie):
    __tablename__ = "versie_bestaand"

    id: Mapped[int] = mapped_column(ForeignKey("versies.id"), primary_key=True)
    versie_code: Mapped[str] = mapped_column(String(8))
    aantal_regels: Mapped[int | None] = mapped_column(Integer)
    hoogste_gil: Mapped[int | None] = mapped_column(Integer)
    is_reversed_engineerd: Mapped[bool] = mapped_column(Boolean, default=False)

    versie_ontwerpen: Mapped[list["VersieOntwerp"]] = relationship(
        back_populates="parent_versie_bestaand",
        foreign_keys="VersieOntwerp.parent_versie_bestaand_id",
        cascade="all, delete-orphan",  # If the Bestaand is deleted, its Ontwerpen go too
    )

    __mapper_args__ = {"polymorphic_identity": "bestaand"}
    pass


class VersieOntwerp(TimestampMixin, Versie):
    __tablename__ = "versie_ontwerp"

    id: Mapped[int] = mapped_column(ForeignKey("versies.id"), primary_key=True)
    versie_ini: Mapped[str] = mapped_column(String(8))

    parent_versie_bestaand_id: Mapped[int | None] = mapped_column(
        ForeignKey("versie_bestaand.id")
    )
    parent_versie_bestaand: Mapped[VersieBestaand | None] = relationship(
        back_populates="versie_ontwerpen", foreign_keys=[parent_versie_bestaand_id]
    )

    fases: Mapped[list["VersieOntwerpFase"]] = relationship(
        back_populates="versie_ontwerp"
    )

    __mapper_args__ = {"polymorphic_identity": "ontwerp"}


class VersieOntwerpFase(TimestampMixin, Base):
    __tablename__ = "versie_ontwerp_fase"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    versie_ontwerp_id = mapped_column(ForeignKey("versie_ontwerp.id"))

    # AB, RR, TB
    fase_code: Mapped[str] = mapped_column(String(8))

    versie_code: Mapped[str | None] = mapped_column(String(10))
    aantal_regels: Mapped[int | None] = mapped_column(Integer)
    hoogste_gil: Mapped[int | None] = mapped_column(Integer)

    prorail_projectnr: Mapped[str | None] = mapped_column(String(50))

    versie_ontwerp: Mapped["VersieOntwerp"] = relationship(back_populates="fases")
