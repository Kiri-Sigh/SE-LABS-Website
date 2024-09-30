from fastapi import FastAPI
from .routers import admin, lead_researcher, researcher_folder, user
# from .routers.admin import event, laboratory, news, publication, research, researcher
# from .routers.lead_researcher import event, laboratory, news, publication, research, researcher
# from .routers.researcher_folder import event, laboratory, news, publication, research, researcher
# from .routers.user import event, laboratory, news, publication, research, researcher
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.event.router)
app.include_router(admin.laboratory.router)
app.include_router(admin.news.router)
app.include_router(admin.publication.router)
app.include_router(admin.research.router)
app.include_router(admin.researcher.router)
app.include_router(lead_researcher.event.router)
app.include_router(lead_researcher.laboratory.router)
app.include_router(lead_researcher.news.router)
app.include_router(lead_researcher.publication.router)
app.include_router(lead_researcher.research.router)
app.include_router(lead_researcher.researcher.router)
app.include_router(researcher_folder.event.router)
app.include_router(researcher_folder.laboratory.router)
app.include_router(researcher_folder.news.router)
app.include_router(researcher_folder.publication.router)
app.include_router(researcher_folder.research.router)
app.include_router(researcher_folder.researcher.router)
app.include_router(user.event.router)
app.include_router(user.laboratory.router)
app.include_router(user.news.router)
app.include_router(user.publication.router)
app.include_router(user.research.router)
app.include_router(user.researcher.router)