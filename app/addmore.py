from sqlexpr import db, User

eadmin = User('admin', 'admin@example.com')
eguest = User('guest', 'guest@example.com')

db.session.add(eadmin)
db.session.add(eguest)
db.session.commit()


