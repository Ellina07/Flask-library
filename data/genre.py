import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from . import db_session
from .db_session import SqlAlchemyBase


class Genre(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'genre'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    wishlist = orm.relationship("Wishlist", back_populates="genre" )


def createNewGenre(genre):
    session = db_session.create_session()
    g1 = Genre(
        genre=genre
    )
    session.add(g1)
    session.commit()