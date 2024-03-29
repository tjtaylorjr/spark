from .db import db
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils import aggregated
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable
import uuid

make_searchable(db.metadata)


def generate_uuid():
    return str(uuid.uuid4())


class Star_Rating(db.Model):
    __tablename__ = 'star_ratings'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey(
        'cards.id'), primary_key=True)
    stars = db.Column(db.Float(precision=1))
    card = db.relationship('Card', back_populates='card_star_ratings')
    user = db.relationship('User', back_populates='user_star_ratings')

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "user_id": self.user_id,
            "stars": self.stars
        }


class CardQuery(BaseQuery, SearchQueryMixin):
    pass


class Card(db.Model):
    query_class = CardQuery
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    # uuid = db.Column(UUID(as_uuid=True), server_default=db.text("uuid_generate_v4()"), nullable = False, unique = True)
    uuid = db.Column(db.String, default=generate_uuid,
                     nullable=False, unique=True)
    arena_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(200), nullable=False)
    set_code = db.Column(db.String(10), db.ForeignKey(
        'sets.set_code'), nullable=True)
    set_number = db.Column(db.String(10), nullable=True)
    rarity = db.Column(db.String(10), nullable=True)
    type = db.Column(db.String(100), nullable=True)
    power = db.Column(db.String(10), nullable=True)
    toughness = db.Column(db.String(10), nullable=True)
    loyalty = db.Column(db.String(10), nullable=True)
    mana_cost = db.Column(db.String(50), default="")
    conv_mana_cost = db.Column(db.Float(precision=1), default=0.0)
    keywords = db.Column(db.String(150), nullable=True)
    rules_text = db.Column(db.Text, nullable=True)
    flavor_text = db.Column(db.Text, nullable=True)
    is_multifaced = db.Column(db.Boolean, default=False)
    # avg_rating = db.Column(db.Float(precision = 1), nullable = True)
    search_vector = db.Column(TSVectorType('name', 'type', 'keywords',
                              'rules_text', 'set_code', 'rarity',
                              weights={'name': 'A', 'type': 'B', 'keywords': 'C', 'rules_text': 'D', 'set_code': 'E', 'rarity': 'F'}))
    format_list = db.relationship(
        'Format_List', uselist=False, back_populates='card', cascade="delete, delete-orphan")
    illustration = db.relationship(
        'Illustration', uselist=False, back_populates="card", cascade="delete, delete-orphan")
    set = db.relationship('Set', back_populates="cards")
    alternate_cardfaces = db.relationship(
        'Alternate_Cardface', uselist=False, back_populates='card', cascade="delete, delete-orphan")
    card_star_ratings = db.relationship(
        "Star_Rating", back_populates="card", cascade="delete, delete-orphan")
    # deck_list = db.relationship('Deck_Card', back_populates='card', viewonly=True)

    @aggregated('card_star_ratings', db.Column(db.Float(precision=1), nullable=True))
    def avg_rating(self):
        return db.func.avg(Star_Rating.stars)

    def __init__(self, id, uuid, arena_id, name, set_code, set_number, rarity, type, power, toughness, loyalty, mana_cost, conv_mana_cost, keywords, rules_text, flavor_text, is_multifaced):
        self.id = id
        self.uuid = uuid
        self.arena_id = arena_id
        self.name = name
        self.set_code = set_code
        self.set_number = set_number
        self.rarity = rarity
        self.type = type
        self.power = power
        self.toughness = toughness
        self.loyalty = loyalty
        self.mana_cost = mana_cost
        self.conv_mana_cost = conv_mana_cost
        self.keywords = keywords
        self.rules_text = rules_text
        self.flavor_text = flavor_text
        self.is_multifaced = is_multifaced

    def __repr__(self):
        return f'Card({self.id}, {self.uuid}, {self.arena_id}, {self.name}, {self.set_code}, {self.set_number}, {self.rarity}, {self.type}, {self.power}, {self.toughness}, {self.loyalty}, {self.mana_cost}, {self.conv_mana_cost}, {self.keywords}, {self.rules_text}, {self.flavor_text}, {self.is_multifaced}, {self.avg_rating})'

    # def does_format_list_exist(self):
    #     if self.format_list is not None:
    #         return "format_list": self.format_list.to_dict(),
    #     else:
    #         return "format_list": None,

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "arena_id": self.arena_id,
            "name": self.name,
            "set_code": self.set_code,
            "set_number": self.set_number,
            "rarity": self.rarity,
            "type": self.type,
            "power": self.power,
            "toughness": self.toughness,
            "loyalty": self.loyalty,
            "mana_cost": self.mana_cost,
            "conv_mana_cost": self.conv_mana_cost,
            "keywords": self.keywords,
            "rules_text": self.rules_text,
            "flavor_text": self.flavor_text,
            "is_multifaced": self.is_multifaced,
            "avg_rating": self.avg_rating,
            "format_list": self.format_list.to_dict(),
            "illustration": self.illustration.to_dict(),
            **({"alternate_cardfaces": self.alternate_cardfaces.to_dict()} if self.alternate_cardfaces is not None else {}),
            # "card_star_ratings": [star_rating.to_dict() for star_rating in self.card_star_ratings]
            # "illustration": self.illustration,
            # "alternate_cardfaces": self.alternate_cardfaces
            # "format_list": self.format_list.to_dict(),
            # "format_list": [format.to_dict() for format in self.format_list],
            # "illustration": [image.to_dict() for image in self.illustration],
            # "alternate_cardfaces": self.alternate_cardfaces.to_dict()
        }


# db.configure_mappers()
