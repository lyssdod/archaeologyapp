import flask.ext.whooshalchemy

app.config['WHOOSH_BASE'] = 'path/to/whoosh/base'

class BlogPost(db.Model):
    __tablename__ = 'blogpost'
    __searchable__ = ['title', 'content']  # these fields will be indexed by whoosh
    __analyzer__ = SimpleAnalyzer()        # configure analyzer; defaults to                                                # StemmingAnalyzer if not specified

    id = app.db.Column(app.db.Integer, primary_key=True)
    title = app.db.Column(app.db.Unicode)  # Indexed fields are either String,
    content = app.db.Column(app.db.Text)   # Unicode, or Text
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    

    def __repr__(self):
        return '{0}(title={1})'.format(self.__class__.__name__, self.title)
    
        
