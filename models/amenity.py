#!/usr/bin/python3
"""Defines the Amenity class."""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Represents an Amenity for a MySQL database.

    Inherits from BaseModel and Base.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store amenities.
        name (sqlalchemy String): The amenity name.
        place_amenities (sqlalchemy relationship): The Amenity-Place relationship.
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place",
                                   secondary="place_amenity",
                                   back_populates="amenities")
