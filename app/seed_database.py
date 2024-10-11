import os
import sys
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import random
import hashlib
from faker import Faker
from werkzeug.security import generate_password_hash

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine
from app.model import *
from app.schemas.ult.position import Position

load_dotenv()

DATABASR_URT = os.getenv("URL_DATABASE")
Base.metadata.create_all(bind=engine)

fake = Faker()

def generate_research_topic():
    topics = [
        "Artificial Intelligence", "Machine Learning", "Quantum Computing",
        "Bioinformatics", "Renewable Energy", "Nanotechnology",
        "Neuroscience", "Climate Change Modeling", "Cybersecurity",
        "Robotics", "Genomics", "Data Science"
    ]
    return f"{random.choice(topics)}: {fake.bs()}"

def generate_publication_title():
    return f"{' '.join(word.capitalize() for word in fake.words(nb=3))}: {fake.catch_phrase()}"

def generate_unique_image_data(identifier):
    # Create a unique hash based on the identifier
    unique_hash = hashlib.md5(str(identifier).encode()).hexdigest()
    # Convert the hash to bytes
    return unique_hash.encode('utf-8')

def seed_database():
    with Session(engine) as session:
        # Create 100 researchers
        researchers = []
        for _ in range(100):
            researcher_id = uuid4()
            researcher = Researcher(
                user_id=researcher_id,
                full_name=fake.name(),
                image_high=generate_unique_image_data(f"{researcher_id}_high"),
                image_low=generate_unique_image_data(f"{researcher_id}_low"),
                gmail=fake.email(),
                highest_role=random.choice(list(Position)),
                admin=random.choices([True, False], weights=[0.1, 0.9])[0],
                active=random.choices([True, False], weights=[0.95, 0.05])[0]
            )
            session.add(researcher)
            researchers.append(researcher)

            # Create user credentials for the researcher
            user_credentials = UserCredentials(
                user_id=researcher.user_id,
                password_hash=generate_password_hash(fake.password())
            )
            session.add(user_credentials)
        
        session.commit()

        # Create 5-10 laboratories
        labs = []
        for _ in range(random.randint(5, 10)):
            lab_id = uuid4()
            lab = Laboratory(
                lab_id=lab_id,
                lab_name=f"{fake.company()} {random.choice(['Lab', 'Research Center', 'Institute'])}",
                image_high=generate_unique_image_data(f"{lab_id}_high"),
                image_low=generate_unique_image_data(f"{lab_id}_low"),
                body=fake.paragraph(nb_sentences=5)
            )
            session.add(lab)
            labs.append(lab)
        
        session.commit()


        # Associate researchers with labs
        for researcher in researchers:
            lab = random.choice(labs)
            lab_association = person_lab(user_id=researcher.user_id, lab_id=lab.lab_id, role=researcher.highest_role)
            session.add(lab_association)
        
        session.commit()

        # Create 15-25 research projects
        researches = []
        for _ in range(random.randint(15, 25)):
            research_id = uuid4()
            research = Research(
                research_id=research_id,
                research_name=generate_research_topic(),
                image_high=generate_unique_image_data(f"{research_id}_high"),
                image_low=generate_unique_image_data(f"{research_id}_low"),
                body=fake.paragraph(nb_sentences=7),
                lab_id=random.choice(labs).lab_id
            )
            session.add(research)
            researches.append(research)

            # Associate 3-8 random researchers with each research project
            for researcher in random.sample(researchers, random.randint(3, 8)):
                research_association = person_research(user_id=researcher.user_id, research_id=research.research_id, role=researcher.highest_role)
                session.add(research_association)
        
        session.commit()

        # Create 30-50 publications
        for _ in range(random.randint(30, 50)):
            publication_id = uuid4()
            publication = Publication(
                publication_id=publication_id,
                publication_name=generate_publication_title(),
                image_high=generate_unique_image_data(f"{publication_id}_high"),
                image_low=generate_unique_image_data(f"{publication_id}_low"),
                body=fake.paragraph(nb_sentences=10),
                url=fake.url(),
                lab_id=random.choice(labs).lab_id
            )
            session.add(publication)
        
        session.commit()

        # Create 40-60 news items
        for _ in range(random.randint(40, 60)):
            news_id = uuid4()
            news = News(
                news_id=news_id,
                news_name=fake.catch_phrase(),
                image_high=generate_unique_image_data(f"{news_id}_high"),
                image_low=generate_unique_image_data(f"{news_id}_low"),
                body=fake.paragraph(nb_sentences=5),
                date=fake.date_time_between(start_date="-2y", end_date="now"),
                posted=random.choices([True, False], weights=[0.9, 0.1])[0],
                lab_id=random.choice(labs).lab_id,
                research_id=random.choice(researches).research_id if random.random() > 0.3 else None
            )
            session.add(news)
        
        session.commit()

        # Create 20-30 events
        for _ in range(random.randint(20, 30)):
            event_start = fake.future_datetime(end_date="+1y")
            event_id = uuid4()
            event = Event(
                event_id=event_id,
                event_name=f"{fake.word().capitalize()} {random.choice(['Conference', 'Symposium', 'Workshop', 'Seminar'])}",
                image_high=generate_unique_image_data(f"{event_id}_high"),
                image_low=generate_unique_image_data(f"{event_id}_low"),
                body=fake.paragraph(nb_sentences=6),
                location=f"{fake.city()}, {fake.country()}",
                date_start=event_start,
                date_end=event_start + timedelta(days=random.randint(1, 5)),
                posted=random.choices([True, False], weights=[0.8, 0.2])[0],
                lab_id=random.choice(labs).lab_id,
                research_id=random.choice(researches).research_id if random.random() > 0.5 else None
            )
            session.add(event)
        
        session.commit()

if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully with realistic data!")