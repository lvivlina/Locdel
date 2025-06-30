from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    driver = db.Column(db.String(100))
    truck_number = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Заплановано')
    notes = db.Column(db.Text)
    date = db.Column(db.Date, default=datetime.date.today)
