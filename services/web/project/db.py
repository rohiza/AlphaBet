from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_tables(database):
    try:
        database.create_all()
    except Exception as e:
        print(e)

    database.session.commit()
