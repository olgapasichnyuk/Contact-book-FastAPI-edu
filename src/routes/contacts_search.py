from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from src.database.db import get_db
from src.database.models import User
from src.repository.contacts import search_everywhere_contacts, filter_contacts
from src.schemas import ContactResponseModel
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts/search', tags=['search contacts'])


@router.get('/', response_model=List[ContactResponseModel])
async def search_contacts(parameter: str,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    contacts = await search_everywhere_contacts(parameter, current_user, db)
    return contacts


@router.get('/filter', response_model=List[ContactResponseModel])
async def search_with_filter_contacts(name: str = '', surname: str = '', email: str = '',
                                      db: Session = Depends(get_db),
                                      current_user: User = Depends(auth_service.get_current_user)):
    contacts = await filter_contacts(name, surname, email, current_user, db)
    return contacts

# @router.get('/name/{name}', response_model=List[ContactResponseModel])
# async def search_by_name(name: str,
#                          db: Session = Depends(get_db),
#                          current_user: User = Depends(auth_service.get_current_user)):
#     contacts = await match_by_name(name, current_user, db)
#     return contacts
#
#
# @router.get('/surname/{surname}', response_model=List[ContactResponseModel])
# async def search_by_surname(surname: str,
#                             db: Session = Depends(get_db),
#                             current_user: User = Depends(auth_service.get_current_user)):
#     contacts = await match_by_surname(surname, current_user, db)
#     return contacts
#
#
# @router.get('/email/{email}', response_model=ContactResponseModel)
# async def search_by_email(email: EmailStr,
#                           db: Session = Depends(get_db),
#                           current_user: User = Depends(auth_service.get_current_user)):
#     contact = await match_by_email(email, current_user, db)
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
#     return contact
