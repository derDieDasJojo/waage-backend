# coding=utf-8

from marshmallow import Schema, fields

from sqlalchemy import Column, String, BigInteger, Integer

from .entity import Entity, Base


class Scale(Entity, Base):
    __tablename__ = 'scale'

    title = Column(String)
    description = Column(String)
    offset = Column(BigInteger)
    reference_unit = Column(BigInteger)

    def __init__(self, offset,referenceUnit,created_by):
        Entity.__init__(self, created_by)
        self.offset = offset
        self.reference_unit = referenceUnit

class ScaleSchema(Schema):
    id = fields.Number()
    reference_unit = fields.Number()
    offset = fields.Number()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    def get_offset(self):
        return self.offset

    def get_reference_unit(self):
        return self.reference_unit
