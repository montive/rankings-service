#from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()
#migrate = Migrate(app, db)
class QSRankingModel(db.Model):
    __tablename__ = "qsranking"
    id = db.Column(db.Integer, primary_key=True)
    university = db.Column(db.String, nullable=False)
    university_location = db.Column(db.String, nullable=False)
    university_location_code = db.Column(db.String)
    position = db.Column(db.Integer)
    score = db.Column(db.Float)
    ranking_year = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'university': self.university,
            'university_location': self.university_location,
            'university_location_code': self.university_location_code,
            'position': self.position,
            'score': self.score,
            'ranking_year': self.ranking_year
        }