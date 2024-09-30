from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from .people import People

class Credentials(Base):
    __tablename__ = "credentials"

    credential_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("people.user_id"), unique=True)
    hashed_password: Mapped[str]

    user: Mapped["People"] = relationship(back_populates="credentials")