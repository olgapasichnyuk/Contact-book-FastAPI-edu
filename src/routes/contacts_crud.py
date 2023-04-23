from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from starlette import status

from src.database.db import get_db
from src.database.models import User
from src.repository.contacts import get_contacts, get_contact, post_contact, put_contact, delete_contact
from src.schemas import ContactResponseModel, ContactInputModel
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])



@router.get('/', response_model=List[ContactResponseModel], dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def read_contacts(skip: int = 0,
                        limit: int = 10,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await get_contacts(skip, limit, current_user, db)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponseModel)
async def read_contact(contact_id: int,
                       db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):

    contact = await get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post('/', response_model=ContactInputModel)
async def create_contact(body: ContactInputModel,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    return await post_contact(body, current_user, db)


@router.put('/update/{contact_id}', response_model=ContactResponseModel)
async def update_contact(contact_id: int,
                         body: ContactInputModel,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    return await put_contact(contact_id, body, current_user, db)


@router.delete('/del/{contact_id}', response_model=ContactResponseModel)
async def remove_contact(contact_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await delete_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
