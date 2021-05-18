from db import db

class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)

    def __repr__(self):
        return '<Item %r>' % self.name

    def __str__(self):
        return "User(id='%s')" % self.id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @staticmethod
    def get(name):
        item = Items.query.filter_by(name=name).first()
        return item

    @staticmethod
    def get_all():
        items = Items.query.all()
        return items

    @staticmethod
    def post(name, price):
        db.session.add(Items(name=name, price=price))
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(name):
        item = Items.get(name)
        db.session.delete(item)
        db.session.commit()

