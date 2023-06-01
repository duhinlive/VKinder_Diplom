# импорты
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session


from config import db_url_object

metadata = MetaData()
Base = declarative_base()


class Viewed(Base):
    __tablename__ = 'viewed'
    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)


# добавление записи в бд


def add_user(engine, profile_id, worksheet_id):
    with Session(engine) as session:
        to_bd = Viewed(profile_id=profile_id, worksheet_id=worksheet_id)
        session.add(to_bd)
        session.commit()


# извлечение записей из БД

def check_user(engine, profile_id, worksheet_id):
    with Session(engine) as session:
        from_bd = session.query(Viewed).filter(
            Viewed.profile_id == profile_id,
            Viewed.worksheet_id == worksheet_id
        ).first()
        return True if from_bd else False


if __name__ == '__main__':
    engine = create_engine(db_url_object)
    Base.metadata.create_all(engine)
    # add_user(engine, 2113, 124512)
    res = check_user(engine, 2113, 1245121)
    print(res)