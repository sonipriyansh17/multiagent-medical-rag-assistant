# backend/app/database/base.py

from sqlalchemy.orm import declarative_base

# This Base class will be inherited by all our database models
Base = declarative_base()
