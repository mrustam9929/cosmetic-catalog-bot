import os
import time

from fastapi import FastAPI
from fastapi.security import HTTPBasic
from fastapi_pagination import add_pagination

from core.config import settings
from core.cors import CORSMiddleware

os.environ["TZ"] = settings.tz
time.tzset()

# if settings.sentry_dsn and settings.sentry_env:
#     sentry_sdk.init(
#         environment=settings.sentry_env,
#         dsn=settings.sentry_dsn,
#         traces_sample_rate=1.0,
#     )

app = FastAPI(debug=settings.debug, openapi_url=None, docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
add_pagination(app)

security = HTTPBasic()
