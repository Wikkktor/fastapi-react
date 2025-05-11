from sqlalchemy import Integer, String, Column, Boolean

from db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    surname = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    is_admin = Column(Boolean, default=False)

    hashed_password = Column(String, nullable=False)

    def __repr__(self) -> str:
        """Return a string representation of the user."""
        return f"<User(id={self.id}, email={self.email})>"

    def get_full_name(self) -> str:
        """Get the full name of the user."""
        return f"{self.first_name} {self.surname}"
