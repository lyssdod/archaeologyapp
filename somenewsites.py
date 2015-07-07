from archaeologyProject import db, Site

db.create_all()
hey = Site('name', 'toponim')
db.session.add(hey)
db.session.commit()

