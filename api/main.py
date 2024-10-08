from .routers.admin.event import router as admin_event_router
from .routers.admin.laboratory import router as admin_laboratory_router
from .routers.admin.news import router as admin_news_router
from .routers.admin.publication import router as admin_publication_router
from .routers.admin.research import router as admin_research_router
from .routers.admin.researcher import router as admin_researcher_router

from .routers.lead_researcher.event import router as lead_researcher_event_router
from .routers.lead_researcher.laboratory import router as lead_researcher_laboratory_router
from .routers.lead_researcher.news import router as lead_researcher_news_router
from .routers.lead_researcher.publication import router as lead_researcher_publication_router
from .routers.lead_researcher.research import router as lead_researcher_research_router
from .routers.lead_researcher.researcher import router as lead_researcher_researcher_router

from .routers.researcher.event import router as researcher_folder_event_router
from .routers.researcher.laboratory import router as researcher_folder_laboratory_router
from .routers.researcher.news import router as researcher_folder_news_router
from .routers.researcher.publication import router as researcher_folder_publication_router
from .routers.researcher.research import router as researcher_folder_research_router
from .routers.researcher.researcher import router as researcher_folder_researcher_router

from .routers.user.event import router as user_event_router
from .routers.user.laboratory import router as user_laboratory_router
from .routers.user.news import router as user_news_router
from .routers.user.publication import router as user_publication_router
from .routers.user.research import router as user_research_router
from .routers.user.researcher import router as user_researcher_router

from fastapi import FastAPI
from .database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin_event_router)
app.include_router(admin_laboratory_router)
app.include_router(admin_news_router)
app.include_router(admin_publication_router)
app.include_router(admin_research_router)
app.include_router(admin_researcher_router)

app.include_router(lead_researcher_event_router)
app.include_router(lead_researcher_laboratory_router)
app.include_router(lead_researcher_news_router)
app.include_router(lead_researcher_publication_router)
app.include_router(lead_researcher_research_router)
app.include_router(lead_researcher_researcher_router)

app.include_router(researcher_folder_event_router)
app.include_router(researcher_folder_laboratory_router)
app.include_router(researcher_folder_news_router)
app.include_router(researcher_folder_publication_router)
app.include_router(researcher_folder_research_router)
app.include_router(researcher_folder_researcher_router)

app.include_router(user_event_router)
app.include_router(user_laboratory_router)
app.include_router(user_news_router)
app.include_router(user_publication_router)
app.include_router(user_research_router)
app.include_router(user_researcher_router)