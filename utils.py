import os
import math
import pycountry
import pandas as pd

from models import db, QSRankingModel

DIR_PATH = os.getcwd()
DATA_PATH = os.path.join(DIR_PATH, "data")

def get_country_code(country_name):
    country_data = pycountry.countries.get(name=country_name)
    if country_data:
        return country_data.alpha_2
    else:
        return ""

def populate_database():
    data = pd.read_csv(os.path.join(DATA_PATH, 'qs_ranking_2023.csv'))
    try:
        for index, row in data.iterrows():
            university = QSRankingModel(
                university=row['institution'].strip(),
                university_location=row["location"].strip(),
                university_location_code=row['location code'].strip(),
                position=int(row["Rank"]),
                score=row["score scaled"] if not math.isnan(row["score scaled"]) else 0.0,
                ranking_year=2023
            )
            db.session.add(university)
    except Exception as error:
        print("Error importing qs_ranking_2023.csv file")
        print(error)

    data = pd.read_csv(os.path.join(DATA_PATH, 'qs_ranking_2017-2022.csv'))
    try:
        for index, row in data.iterrows():
            university = QSRankingModel(
                university=row['university'].strip(),
                university_location=row["country"].strip(),
                university_location_code=get_country_code(row["country"].strip()),
                position=row["rank_display"],
                score=row["score"] if not math.isnan(row["score"]) else 0.0,
                ranking_year=int(row["year"])
            )
            db.session.add(university)
    except Exception as error:
        print("Error importing qs_ranking_2017-2022.csv file")
        print(error)
    db.session.commit()
    print("Database populated successfully")
