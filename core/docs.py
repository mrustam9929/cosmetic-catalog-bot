import secrets
from fastapi import Depends, HTTPException, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from core.config import settings
from core.app import app

# region API DOCS VIEWS

router = APIRouter(prefix="api/")

# endregion
