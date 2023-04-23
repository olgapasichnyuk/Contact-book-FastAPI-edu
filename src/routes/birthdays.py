from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository.contacts import get_birthdays_week
from src.schemas import ContactResponseModel
from src.services.auth import auth_service

router = APIRouter(prefix='/birthdays', tags=['birthdays'])


@router.get('/', response_model=List[ContactResponseModel])
async def get_birthdays(current_user: User = Depends(auth_service.get_current_user),
                        db: Session = Depends(get_db)):
    contacts = await get_birthdays_week(db, current_user)
    return contacts
