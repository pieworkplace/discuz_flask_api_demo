from sqlalchemy import Table, create_engine, MetaData
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

# Here changed the default database name ultrax -> discuz
DB_URL = "mysql+pymysql://root:@localhost/discuz"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL

db = SQLAlchemy(app)

base = declarative_base()
engine = create_engine(DB_URL)
metadata = MetaData(bind=engine)


class Member(base):
    __table__ = Table('pre_ucenter_members', metadata, autoload=True)

    def __repr__(self):
        return json.dumps({"Member Info": {'name': self.username, 'email': self.email}})



if __name__ == '__main__':
    # new_common_member = Member(username='pieworkplace', password='12345678', email='pieworkplace@gmail.com', salt='123')
    # db.session.add(new_common_member)
    # db.session.commit()
    print(db.session.query(Member).all())
