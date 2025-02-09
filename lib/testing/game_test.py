import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conftest import SQLITE_URL
from models import Game, Review

@pytest.fixture(scope="class")
def db_session():
    engine = create_engine(SQLITE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # This will return the session to the test functions
    session.close()

class TestGame:
    '''Class Game in models.py'''

    # start session, reset db
    engine = create_engine(SQLITE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    @classmethod
    def setup_class(cls):
        # add test data
        cls.mario_kart = Game(
            title="Mario Kart",
            platform="Switch",
            genre="Racing",
            price=60
        )

        cls.session.add(cls.mario_kart)
        cls.session.commit()

        mk_review_1 = Review(
            score=10,
            comment="Wow, what a game",
            game_id=cls.mario_kart.id
        )

        mk_review_2 = Review(
            score=8,
            comment="A classic",
            game_id=cls.mario_kart.id
        )

        cls.session.bulk_save_objects([mk_review_1, mk_review_2])
        cls.session.commit()

    def test_game_has_correct_attributes(self):
        '''has attributes "id", "title", "platform", "genre", "price".'''
        assert all(hasattr(self.mario_kart, attr) for attr in ["id", "title", "platform", "genre", "price"])

    def test_has_associated_reviews(self):
        '''has two reviews with scores 10 and 8.'''
        assert (
            len(self.mario_kart.reviews) == 2 and
            self.mario_kart.reviews[0].score == 10 and
            self.mario_kart.reviews[1].score == 8
        )

