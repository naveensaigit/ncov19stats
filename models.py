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

    def __init__(self,statename,date,dailyconf,dailyrec,dailydec,cumconf,cumact,cumrec,cumdec):
        self.statename=statename
        self.date=date
        self.dailyconf=dailyconf
        self.dailyrec=dailyrec
        self.dailydec=dailydec
        self.cumconf=cumconf
        self.cumact=cumact
        self.cumrec=cumrec
        self.cumdec=cumdec

    def __repr__(self):
        return "state "+self.statename+" "+str(self.date) 

    def print(self):
        print(self.statename,self.date,self.dailyconf,self.dailyrec,self.dailydec,self.cumconf,self.cumact,self.cumrec,self.cumdec)
    
    def values(self):
        return [self.statename,self.date,self.dailyconf,self.dailyrec,self.dailydec,self.cumconf,self.cumact,self.cumrec,self.cumdec]