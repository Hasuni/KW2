import datetime
from sqlalchemy import (
    Text,
    Index,
    Column,
    Integer,
    Unicode,
    DateTime,
    ForeignKey,
    UnicodeText
)
from sqlalchemy.orm import sessionmaker, scoped_session,relationship, backref
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.ext.declarative import declarative_base

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
Session = sessionmaker()


class User(Base):
    __tablename__ = 'users'
    id_U= Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    aboutme = Column(UnicodeText, nullable = True)

    def _repr_(self):
        return self.name+" "+self.password+" "+self.aboutme+str(self.access)
    



class Article(Base):
    __tablename__ = 'articles'
    id_A = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    content = Column(UnicodeText, default=u'')
    u_id = Column(Integer, ForeignKey('users.id_U'), primary_key=True)
    Cdate = Column(DateTime, default=datetime.datetime.utcnow)

class UserArticle(Base):
    __tablename__ = 'art_user'
    id = Column(Integer, ForeignKey('articles.id_A'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id_U'), primary_key=True)
