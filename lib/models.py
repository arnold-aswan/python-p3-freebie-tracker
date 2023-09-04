from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

company_dev = Table(
    'company_dev',
    Base.metadata,
    Column('company_id', ForeignKey('companies.id'), primary_key=True),
    Column('dev_id', ForeignKey('devs.id'), primary_key=True),
    extend_existing=True,
)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    devs = relationship('Dev', secondary='company_dev', back_populates='companies')
    freebies = relationship('Freebie', backref=backref('company'), cascade='all, delete-orphan')

    def __init__(self, name, founding_year):
        self.name = name
        self.founding_year = founding_year

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    
    companies = relationship('Company', secondary='company_dev', back_populates='devs')
    freebies = relationship('Freebie', backref=backref('dev'), cascade='all, delete-orphan')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Dev {self.name}>'

class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    
    def __init__(self, item_name, value, company_id, dev_id):
        self.item_name = item_name
        self.value = value
        self.company_id = company_id
        self.dev_id = dev_id
    
    def __repr__(self):
        return f'Freebie(id={self.id}, ' + \
            f'item_name={self.item_name}, ' + \
            f'value={self.value})'
         
         
# engine = create_engine('sqlite:///freebies.db')            
# Base.metadata.create_all(engine)  

# Session = sessionmaker(bind=engine)
# session = Session()          

#  add company
# name = 'optimum'
# founding_year = 2005
# comp = Company(name, founding_year)
# session.add(comp)
# session.commit()
# print('company added')

# add dev
# name = 'daniel'

# dev = Dev(name)
# session.add(dev)
# session.commit()
# print("dev added")

# comp.devs.append(dev)


# add freebie
# item = 'hoodie'
# value = 68
# ci =1
# di = 1
# free = Freebie(item, value, ci, di)
# session.add(free)
# session.commit()
# print('Freebie added')