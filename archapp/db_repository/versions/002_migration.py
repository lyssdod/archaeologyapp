from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
site = Table('site', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=250)),
    Column('toponim', String(length=250)),
    Column('type_of_site', String(length=250), nullable=False),
    Column('oblast', String(length=250), nullable=False),
    Column('rajon', String(length=250), nullable=False),
    Column('punkt', String(length=250), nullable=False),
    Column('pryvjazka', String(length=250), nullable=False),
    Column('kultnal', String(length=250), nullable=False),
    Column('localgr', String(length=250), nullable=False),
    Column('chron', String(length=250), nullable=False),
    Column('nadijnist', String(length=250), nullable=False),
    Column('rozkop', String(length=1000), nullable=False),
    Column('zvit', String(length=1000), nullable=False),
    Column('publicacii', String(length=1500), nullable=False),
    Column('kartograph', String(length=20), nullable=False),
    Column('coord', String(length=50), nullable=False),
    Column('tochkart', String(length=20), nullable=False),
    Column('basejn', String(length=50), nullable=False),
    Column('toppotype', String(length=30), nullable=False),
    Column('geomorform', String(length=250), nullable=False),
    Column('vysotnadrm', String(length=250), nullable=False),
    Column('ploshch', String(length=50), nullable=False),
    Column('dovz', String(length=50), nullable=False),
    Column('shyr', String(length=50), nullable=False),
    Column('prymitky', String(length=3000)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['site'].columns['basejn'].create()
    post_meta.tables['site'].columns['chron'].create()
    post_meta.tables['site'].columns['coord'].create()
    post_meta.tables['site'].columns['dovz'].create()
    post_meta.tables['site'].columns['geomorform'].create()
    post_meta.tables['site'].columns['kartograph'].create()
    post_meta.tables['site'].columns['kultnal'].create()
    post_meta.tables['site'].columns['localgr'].create()
    post_meta.tables['site'].columns['nadijnist'].create()
    post_meta.tables['site'].columns['oblast'].create()
    post_meta.tables['site'].columns['ploshch'].create()
    post_meta.tables['site'].columns['prymitky'].create()
    post_meta.tables['site'].columns['pryvjazka'].create()
    post_meta.tables['site'].columns['publicacii'].create()
    post_meta.tables['site'].columns['punkt'].create()
    post_meta.tables['site'].columns['rajon'].create()
    post_meta.tables['site'].columns['rozkop'].create()
    post_meta.tables['site'].columns['shyr'].create()
    post_meta.tables['site'].columns['tochkart'].create()
    post_meta.tables['site'].columns['toppotype'].create()
    post_meta.tables['site'].columns['type_of_site'].create()
    post_meta.tables['site'].columns['vysotnadrm'].create()
    post_meta.tables['site'].columns['zvit'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['site'].columns['basejn'].drop()
    post_meta.tables['site'].columns['chron'].drop()
    post_meta.tables['site'].columns['coord'].drop()
    post_meta.tables['site'].columns['dovz'].drop()
    post_meta.tables['site'].columns['geomorform'].drop()
    post_meta.tables['site'].columns['kartograph'].drop()
    post_meta.tables['site'].columns['kultnal'].drop()
    post_meta.tables['site'].columns['localgr'].drop()
    post_meta.tables['site'].columns['nadijnist'].drop()
    post_meta.tables['site'].columns['oblast'].drop()
    post_meta.tables['site'].columns['ploshch'].drop()
    post_meta.tables['site'].columns['prymitky'].drop()
    post_meta.tables['site'].columns['pryvjazka'].drop()
    post_meta.tables['site'].columns['publicacii'].drop()
    post_meta.tables['site'].columns['punkt'].drop()
    post_meta.tables['site'].columns['rajon'].drop()
    post_meta.tables['site'].columns['rozkop'].drop()
    post_meta.tables['site'].columns['shyr'].drop()
    post_meta.tables['site'].columns['tochkart'].drop()
    post_meta.tables['site'].columns['toppotype'].drop()
    post_meta.tables['site'].columns['type_of_site'].drop()
    post_meta.tables['site'].columns['vysotnadrm'].drop()
    post_meta.tables['site'].columns['zvit'].drop()
