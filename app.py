from sqlalchemy import func
from flask_cors import CORS
from models import db, QSRankingModel
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jmontilva94:postgres@localhost:5432/rankings'
CORS(app)

db.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/get_qs_ranking", methods=["GET"])
def get_qs_ranking():
    year = request.args.get("year") or 2023
    limit = request.args.get("limit")
    group_by = request.args.get("group_by")
    query = QSRankingModel.query
    if year:
        query = query.filter_by(ranking_year=year)
    if group_by:
        if group_by == "country":
            query = query.with_entities(QSRankingModel.university_location,
                                        QSRankingModel.university_location_code,
                                        func.count(QSRankingModel.id).label('count'))\
                .group_by(QSRankingModel.university_location, QSRankingModel.university_location_code)\
                .order_by(func.count(QSRankingModel.id).desc())
    else:
        query = query.order_by(QSRankingModel.position.asc())
    if limit:
        query = query.limit(limit)

    if group_by:
        ranking = [
            {"university_location": row[0], "university_location_code": row[1], "count": row[2]} for row in query.all()]
    else:
        ranking = [row.serialize() for row in query.all()]
    return jsonify(ranking)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
