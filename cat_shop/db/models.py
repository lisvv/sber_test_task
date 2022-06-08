import sqlalchemy as sa
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy, orm
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Index, func, or_
from sqlalchemy.dialects.postgresql import TSVECTOR

db = SQLAlchemy()
ma = Marshmallow()


class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR


class Breed(db.Model):
    __tablename__ = "breeds"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False)
    kitties = orm.relationship("Kitty", back_populates="breed", passive_deletes=True)

    __ts_vector__ = db.Column(
        TSVector(),
        db.Computed("to_tsvector('russian', coalesce(name,''))", persisted=True),
    )

    __table_args__ = (
        Index("ix_breed___ts_vector__", __ts_vector__, postgresql_using="gin"),
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Kitty(db.Model):
    __tablename__ = "kitties"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    breed_id = db.Column(
        db.Integer, db.ForeignKey("breeds.id", ondelete="CASCADE"), nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(100), nullable=True)
    birthday = db.Column(db.Date(), nullable=False)
    breed = orm.relationship("Breed")

    __ts_vector__ = db.Column(
        TSVector(),
        db.Computed(
            "to_tsvector('russian', coalesce(name,'') || ' ' || coalesce(description,''))",
            persisted=True,
        ),
    )

    __table_args__ = (
        Index("ix_kitty___ts_vector__", __ts_vector__, postgresql_using="gin"),
    )

    @classmethod
    def __plainto_tsquery(cls, value):
        return cls.query.join(Breed).filter(
            or_(
                cls.__ts_vector__.op("@@")(func.plainto_tsquery("russian", value)),
                Breed.__ts_vector__.op("@@")(func.plainto_tsquery("russian", value)),
            )
        )

    @classmethod
    def __to_tsquery(cls, value):
        value += ":*"
        return cls.query.join(Breed).filter(
            or_(cls.__ts_vector__.match(value), Breed.__ts_vector__.match(value))
        )

    @classmethod
    def fulltext_search(cls, value) -> db.Query:
        if len(value.split(" ")) > 1:
            query = cls.__plainto_tsquery(value)
        else:
            query = cls.__to_tsquery(value)
        if query.count() == 0:
            query = cls.__plainto_tsquery(value)
        return query

    def __str__(self) -> str:
        return f"{self.name}"


class KittySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "name", "description", "breed_id", "image", "birthday")
        model = Kitty
        include_fk = True
        load_instance = True


class BreedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = (
            "id",
            "name",
        )
        model = Breed
        include_fk = True
        load_instance = True
