#from flask.ext.sqlalchemy import SQLAlchemy
#import sqlexpr 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thetest.db'
from sqlexpr import db, User
#'sqlite:///thetest.db'
db.create_all()

admin = User('theadmin', 'theadmin@example.com')
guest = User('theguest', 'theguest@example.com')

db.session.add(admin)
db.session.add(guest)
db.session.commit()


