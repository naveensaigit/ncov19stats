from app import db

class state(db.Model):
    statename=db.Column(db.VARCHAR(50),primary_key=True)
    date=db.Column(db.DATE,primary_key=True)
    dailyconf=db.Column(db.BIGINT)
    dailyrec=db.Column(db.BIGINT)
    dailydec=db.Column(db.BIGINT)
    cumconf=db.Column(db.BIGINT)
    cumact=db.Column(db.BIGINT)
    cumrec=db.Column(db.BIGINT)
    cumdec=db.Column(db.BIGINT) 