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
        self.id = None
        self.name = name
        self.founding_year = founding_year

    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self,dev,item_name, value):
        freebie = Freebie(item_name=item_name, value=value, company_id=self.id, dev_id=dev.id)
        return freebie
    
    @classmethod
    def oldest_company(cls, session):
        return session.query(Company).order_by(Company.founding_year).first()        

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
    
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies) 
    
    def give_away(self, dev, freebie):
        if freebie.dev == self.dev:
            freebie.dev == dev
        

class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    
    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')
    
    def __init__(self, item_name, value, company_id, dev_id):
        self.item_name = item_name
        self.value = value
        self.company_id = company_id
        self.dev_id = dev_id
    
    def __repr__(self):
        return f'Freebie(id={self.id}, ' + \
            f'item_name={self.item_name}, ' + \
            f'value={self.value})'

    def print_details(self):
         return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"        
         
# engine = create_engine('sqlite:///freebies.db')            
# Base.metadata.create_all(engine)  

# Session = sessionmaker(bind=engine)
# session = Session()          
