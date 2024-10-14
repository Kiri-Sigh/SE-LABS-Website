import os
import sys
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import random
import hashlib
from faker import Faker
from passlib.context import CryptContext
from PIL import Image, ImageDraw, ImageFont
import io

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine
from app.model import *
from app.schemas.ult.position import Position

load_dotenv()

DATABASE_URL = os.getenv("URL_DATABASE")
INITIAL_ADMIN_EMAIL = os.getenv("INITIAL_ADMIN_EMAIL")
INITIAL_ADMIN_PASSWORD = os.getenv("INITIAL_ADMIN_PASSWORD")
INITIAL_LEAD_RESEARCHER_EMAIL = os.getenv("INITIAL_LEAD_RESEARCHER_EMAIL")
INITIAL_LEAD_RESEARCHER_PASSWORD = os.getenv("INITIAL_LEAD_RESEARCHER_PASSWORD")
INITIAL_RESEARCHER_EMAIL = os.getenv("INITIAL_RESEARCHER_EMAIL")
INITIAL_RESEARCHER_PASSWORD = os.getenv("INITIAL_RESEARCHER_PASSWORD")
Base.metadata.create_all(bind=engine)

fake = Faker()

# Set up the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def generate_placeholder_image(text, size=(800, 600), bg_color=(200, 200, 200), text_color=(0, 0, 0)):
    image = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    # Get the bounding box of the text
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_width = right - left
    text_height = bottom - top
    
    # Calculate the position to center the text
    position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2)
    
    draw.text(position, text, fill=text_color, font=font)
    
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    return buffer.getvalue()

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

def recalculate_highest_role(researcher, session):
    lab_roles = session.query(person_lab).filter(person_lab.user_id == researcher.user_id).all()
    research_roles = session.query(person_research).filter(person_research.user_id == researcher.user_id).all()
    
    all_roles = [role.role for role in lab_roles + research_roles]
    
    if Position.Admin in all_roles:
        highest_role = Position.Admin
    elif Position.LeadResearcher in all_roles:
        highest_role = Position.LeadResearcher
    elif Position.Researcher in all_roles:
        highest_role = Position.Researcher
    else:
        highest_role = Position.Free
    
    researcher.highest_role = highest_role
    session.add(researcher)

def seed_database():
    with Session(engine) as session:
        # Create initial admin
        admin_id = uuid4()
        admin = Researcher(
            user_id=admin_id,
            full_name="Admin User",
            image_high=generate_placeholder_image("Admin User", (800, 600)),
            image_low=generate_placeholder_image("Admin User", (400, 300)),
            gmail=INITIAL_ADMIN_EMAIL,
            highest_role=Position.Admin,
            admin=True,
            active=True
        )
        session.add(admin)

        # Create user credentials for the admin using the correct hashing method
        admin_credentials = UserCredentials(
            user_id=admin.user_id,
            password_hash=get_password_hash(INITIAL_ADMIN_PASSWORD)
        )
        session.add(admin_credentials)

        lead_researcher_id = uuid4()
        lead_researcher = Researcher(
            user_id=lead_researcher_id,
            full_name="Lead Researcher",
            image_high=generate_placeholder_image("Lead Researcher", (800, 600)),
            image_low=generate_placeholder_image("Lead Researcher", (400, 300)),
            gmail=INITIAL_LEAD_RESEARCHER_EMAIL,
            highest_role=Position.LeadResearcher,
            admin=False,
            active=True
        )
        session.add(lead_researcher)

        # Create user credentials for the lead researcher using the correct hashing method
        lead_researcher_credentials = UserCredentials(
            user_id=lead_researcher.user_id,
            password_hash=get_password_hash(INITIAL_LEAD_RESEARCHER_PASSWORD)
        )
        session.add(lead_researcher_credentials)

        researcher_id = uuid4()
        researcher_init = Researcher(
            user_id=researcher_id,
            full_name="Researcher",
            image_high=generate_placeholder_image("Researcher", (800, 600)),
            image_low=generate_placeholder_image("Researcher", (400, 300)),
            gmail=INITIAL_RESEARCHER_EMAIL,
            highest_role=Position.Researcher,
            admin=False,
            active=True
        )
        session.add(researcher_init)

        # Create user credentials for the researcher using the correct hashing method
        researcher_credentials = UserCredentials(
            user_id=researcher_init.user_id,
            password_hash=get_password_hash(INITIAL_RESEARCHER_PASSWORD)
        )
        session.add(researcher_credentials)
        
        session.commit()

        # Create 47 more researchers (50 total including admin)
        researchers = [admin]
        for i in range(47):
            researcher_id = uuid4()
            is_admin = i < 2  # Next 2 researchers are admins (3 total)
            researcher = Researcher(
                user_id=researcher_id,
                full_name=fake.name(),
                image_high=generate_placeholder_image(f"Researcher {i+2}", (800, 600)),
                image_low=generate_placeholder_image(f"Researcher {i+2}", (400, 300)),
                gmail=fake.email(),
                highest_role=Position.Admin if is_admin else Position.Free,
                admin=is_admin,
                active=True
            )
            session.add(researcher)
            researchers.append(researcher)

            # Create user credentials for the researcher using the correct hashing method
            user_credentials = UserCredentials(
                user_id=researcher.user_id,
                password_hash=get_password_hash(fake.password())
            )
            session.add(user_credentials)
        
        session.commit()

        # Create 3-5 laboratories
        labs = []
        for i in range(random.randint(3, 5)):
            lab_id = uuid4()
            lab = Laboratory(
                lab_id=lab_id,
                lab_name=f"{fake.company()} {random.choice(['Lab', 'Research Center', 'Institute'])}",
                image_high=generate_placeholder_image(f"Lab {i+1}", (800, 600)),
                image_low=generate_placeholder_image(f"Lab {i+1}", (400, 300)),
                body=fake.paragraph(nb_sentences=5)
            )
            session.add(lab)
            labs.append(lab)
        
        session.commit()

        # Associate lead researcher with a lab
        lab_association = person_lab(user_id=lead_researcher.user_id, lab_id=labs[0].lab_id, role=Position.LeadResearcher)
        session.add(lab_association)

        # Associate Lead Researchers with labs
        for lab in labs:
            lead_researcher = random.choice([r for r in researchers if not r.admin and r is not researcher_init])
            lab_association = person_lab(user_id=lead_researcher.user_id, lab_id=lab.lab_id, role=Position.LeadResearcher)
            session.add(lab_association)
        
        # Associate admins with all labs
        admin_researchers = [r for r in researchers if r.admin]
        for admin in admin_researchers:
            for lab in labs:
                lab_association = person_lab(user_id=admin.user_id, lab_id=lab.lab_id, role=Position.Admin)
                session.add(lab_association)
        
        session.commit()

        # Create 15-20 research projects
        researches = []
        for i in range(random.randint(15, 20)):
            research_id = uuid4()
            research = Research(
                research_id=research_id,
                research_name=generate_research_topic(),
                image_high=generate_placeholder_image(f"Research {i+1}", (800, 600)),
                image_low=generate_placeholder_image(f"Research {i+1}", (400, 300)),
                body=fake.paragraph(nb_sentences=7),
                lab_id=random.choice(labs).lab_id
            )
            session.add(research)
            researches.append(research)

            # Associate researcher_init with the first research project only
            if i == 0:
                research_association = person_research(user_id=researcher_init.user_id, research_id=research.research_id, role=Position.Researcher)
                session.add(research_association)

            # Associate 2-5 random researchers with each research project
            available_researchers = [r for r in researchers if not r.admin and r is not researcher_init]
            for researcher in random.sample(available_researchers, min(random.randint(2, 5), len(available_researchers))):
                research_association = person_research(user_id=researcher.user_id, research_id=research.research_id, role=Position.Researcher)
                session.add(research_association)

            # Associate admins with all researches
            for admin in admin_researchers:
                research_association = person_research(user_id=admin.user_id, research_id=research.research_id, role=Position.Admin)
                session.add(research_association)

        session.commit()

        # Create news items and events for ongoing research
        for research in researches:
            # Create 1-2 news items for each research
            for _ in range(random.randint(1, 2)):
                news_id = uuid4()
                news = News(
                    news_id=news_id,
                    news_name=fake.catch_phrase(),
                    image_high=generate_placeholder_image(f"News for Research {research.research_id}", (800, 600)),
                    image_low=generate_placeholder_image(f"News for Research {research.research_id}", (400, 300)),
                    body=fake.paragraph(nb_sentences=5),
                    date=fake.date_time_between(start_date="-5y", end_date="now"),
                    posted=random.random() > 0.2,
                    lab_id=research.lab_id,
                    research_id=research.research_id
                )
                session.add(news)

            # Create 0-1 events for each research
            if random.random() > 0.5:
                event_start = fake.date_time_between(start_date="-5y", end_date="+1y")
                event_id = uuid4()
                event = Event(
                    event_id=event_id,
                    event_name=f"{fake.word().capitalize()} {random.choice(['Conference', 'Symposium', 'Workshop', 'Seminar'])}",
                    image_high=generate_placeholder_image(f"Event for Research {research.research_id}", (800, 600)),
                    image_low=generate_placeholder_image(f"Event for Research {research.research_id}", (400, 300)),
                    body=fake.paragraph(nb_sentences=6),
                    location=f"{fake.city()}, {fake.country()}",
                    date_start=event_start,
                    date_end=event_start + timedelta(days=random.randint(1, 3)),
                    posted=random.random() > 0.2,
                    lab_id=research.lab_id,
                    research_id=research.research_id
                )
                session.add(event)

        session.commit()

        # Create 5-10 publications (finished research)
        for i in range(random.randint(5, 10)):
            if not researches:
                break
            finished_research = random.choice(researches)
            publication_id = uuid4()
            publication = Publication(
                publication_id=publication_id,
                publication_name=generate_publication_title(),
                image_high=finished_research.image_high,
                image_low=finished_research.image_low,
                body=finished_research.body,
                url=fake.url(),
                lab_id=finished_research.lab_id
            )
            session.add(publication)

            # Migrate news and events from research to publication
            news_items = session.query(News).filter(News.research_id == finished_research.research_id).all()
            events = session.query(Event).filter(Event.research_id == finished_research.research_id).all()

            for news in news_items:
                news.research_id = None
                if news.posted:
                    news.publication_id = publication_id
                    session.add(news)
                else:
                    session.delete(news)

            for event in events:
                event.research_id = None
                if event.posted:
                    event.publication_id = publication_id
                    session.add(event)
                else:
                    session.delete(event)

            # Remove researcher associations with the finished research
            session.query(person_research).filter(person_research.research_id == finished_research.research_id).delete()

            # Remove the finished research
            session.delete(finished_research)
            researches.remove(finished_research)
        
        session.commit()

        # Recalculate highest roles for all researchers
        for researcher in researchers:
            recalculate_highest_role(researcher, session)
        
        session.commit()

        # Create additional news items and events for labs
        for i in range(random.randint(5, 10)):
            news_id = uuid4()
            news = News(
                news_id=news_id,
                news_name=fake.catch_phrase(),
                image_high=generate_placeholder_image(f"Additional News {i+1}", (800, 600)),
                image_low=generate_placeholder_image(f"Additional News {i+1}", (400, 300)),
                body=fake.paragraph(nb_sentences=5),
                date=fake.date_time_between(start_date="-5y", end_date="now"),
                posted=False if i == 0 else random.random() > 0.2,
                lab_id=labs[0].lab_id if i == 1 else random.choice(labs).lab_id
            )
            session.add(news)

        for i in range(random.randint(3, 5)):
            event_start = fake.date_time_between(start_date="-5y", end_date="+1y")
            event_id = uuid4()
            event = Event(
                event_id=event_id,
                event_name=f"{fake.word().capitalize()} {random.choice(['Conference', 'Symposium', 'Workshop', 'Seminar'])}",
                image_high=generate_placeholder_image(f"Additional Event {i+1}", (800, 600)),
                image_low=generate_placeholder_image(f"Additional Event {i+1}", (400, 300)),
                body=fake.paragraph(nb_sentences=6),
                location=f"{fake.city()}, {fake.country()}",
                date_start=event_start,
                date_end=event_start + timedelta(days=random.randint(1, 3)),
                posted=False if i == 0 else random.random() > 0.2,
                lab_id=labs[0].lab_id if i == 0 else random.choice(labs).lab_id
            )
            session.add(event)
        
        # Create general news and events (not associated with any lab, research, or publication)
        for i in range(random.randint(5, 10)):
            news_id = uuid4()
            news = News(
                news_id=news_id,
                news_name=fake.catch_phrase(),
                image_high=generate_placeholder_image(f"General News {i+1}", (800, 600)),
                image_low=generate_placeholder_image(f"General News {i+1}", (400, 300)),
                body=fake.paragraph(nb_sentences=5),
                date=fake.date_time_between(start_date="-5y", end_date="now"),
                posted=True
            )
            session.add(news)

        for i in range(random.randint(3, 5)):
            event_start = fake.date_time_between(start_date="-5y", end_date="+1y")
            event_id = uuid4()
            event = Event(
                event_id=event_id,
                event_name=f"{fake.word().capitalize()} {random.choice(['Conference', 'Symposium', 'Workshop', 'Seminar'])}",
                image_high=generate_placeholder_image(f"General Event {i+1}", (800, 600)),
                image_low=generate_placeholder_image(f"General Event {i+1}", (400, 300)),
                body=fake.paragraph(nb_sentences=6),
                location=f"{fake.city()}, {fake.country()}",
                date_start=event_start,
                date_end=event_start + timedelta(days=random.randint(1, 3)),
                posted=True
            )
            session.add(event)
        
        session.commit()

if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully with realistic data, placeholder images, and general news/events!")