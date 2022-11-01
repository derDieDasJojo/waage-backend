# coding=utf-8

from sqlalchemy import Column, String

from .entity import Entity, Base


class Product(Entity, Base):
    __tablename__ = 'exams'

    name = Column(String)
    description = Column(String)

    def __init__(self, name, description, created_by):
        Entity.__init__(self, created_by)
        self.name = name
        self.description = description