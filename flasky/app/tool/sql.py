from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from config import sql_route

engine = create_engine(sql_route, max_overflow=5)

Base = declarative_base()


class Netflow(Base):

    __tablename__ = 'netflow'
    id = Column(Integer, primary_key=True)

    f1 = Column(Float)
    f2 = Column(String(16))
    f3 = Column(String(16))
    f4 = Column(String(16))
    f5 = Column(Float)
    f6 = Column(Float)
    f7 = Column(Float)
    f8 = Column(Float)
    f9 = Column(Float)

    f23 = Column(Float)
    f24 = Column(Float)
    f25 = Column(Float)
    f26 = Column(Float)
    f27 = Column(Float)
    f28 = Column(Float)
    f29 = Column(Float)
    f30 = Column(Float)
    f31 = Column(Float)

    f32 = Column(Float)
    f33 = Column(Float)
    f34 = Column(Float)
    f35 = Column(Float)
    f36 = Column(Float)
    f37 = Column(Float)
    f38 = Column(Float)
    f39 = Column(Float)
    f40 = Column(Float)
    f41 = Column(Float)

    fromIP = Column(String(32))
    fromPort = Column(Integer)

    toIP = Column(String(32))
    toPort = Column(Integer)

    timestamp = Column(DateTime())

    evalue = Column(Float)
    error = Column(Boolean)


class Sysinfo(Base):

    __tablename__ = 'sysinfo'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime())
    mem_free = Column(Integer)
    mem_used = Column(Float)
    net_reci = Column(Float)
    net_send = Column(Float)
    process = Column(Integer)
    cpu_used = Column(Float)
    disk_writ = Column(Float)
    disk_read = Column(Float)
#
# class Config:
#     __tablename__ = 'config'
#     name = Column(String(32), primary_key=True)
#     value = Column(String(128))
#


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    drop_db()
    init_db()