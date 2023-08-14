from app import app, db


class ContatoModels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    message = db.Column(db.Text, nullable=True)


    def __repr__(self):
        return f' <Contato {self.name}>'
   