#!/usr/bin/env python3

# Script goes here!
from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    
    fake = Faker()
    
    
    companies = []
    for i in range(10):
        company = Company(
            name = fake.catch_phrase(),
            founding_year = fake.year(),
        )
        
        # add and commit individually to get id
        session.add(company)
        session.commit()
        
        companies.append(company)
                         
    devs = [] 
    for i in range(10):
        dev = Dev(
            name = fake.name(),
        )
        
        session.add(dev)
        session.commit()
        
        devs.append(dev)
        
        
    freebies = []
    for company in companies:
        for i in range(random.randint(1,5)):
            dev = random.choice(devs)
            if company not in dev.companies:
                dev.companies.append(company)
                session.add(dev)
                session.commit()
                
            freebie = Freebie(  
                item_name = fake.word(),
                value = fake.random_int(min=1, max=65),
                company_id = random.choice(session.query(Company).all()).id,
                dev_id = random.choice(session.query(Dev).all()).id 
            )    
            
            freebies.append(freebie)
            
    session.bulk_save_objects(freebies)
    session.commit()
    session.close()        
        
    # for i in range(20):
    #     freebie = Freebie(
    #         item_name = fake.word(),
    #         value = fake.random_int(min=1, max=65),
    #         company_id = random.choice(session.query(Company).all()).id,
    #         dev_id = random.choice(session.query(Dev).all()).id
    #     )    
        
    #     session.add(freebie)
    #     session.commit()
        
        
    # session.commit()