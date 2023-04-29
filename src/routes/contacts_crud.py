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
    """
    The read_contacts function returns a list of contacts.

    :param skip: int: Skip a number of records in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass a database session to the function
    :param current_user: User: Get the user who is making the request
    :return: A list of contacts, which is the same as the return type of get_contacts
    """
    contacts = await get_contacts(skip, limit, current_user, db)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponseModel)
async def read_contact(contact_id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact function is used to read a single contact from the database.
    It takes in an integer representing the ID of the contact, and returns a Contact object.

    :param contact_id: int: Specify the contact id
    :param db: Session: Pass a database session to the function
    :param current_user: User: Pass the current user to the function
    :return: A contact object
    """
    contact = await get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post('/', response_model=ContactInputModel)
async def create_contact(body: ContactInputModel,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactInputModel: Define the body of the request
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    """
    return await post_contact(body, current_user, db)


@router.put('/update/{contact_id}', response_model=ContactResponseModel)
async def update_contact(contact_id: int,
                         body: ContactInputModel,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
    The function takes three arguments:
        - contact_id: an integer representing the id of the contact to be updated.
        - body: a ContactInputModel object containing information about what fields are being updated and their new values.  This is passed as JSON data in the request body, so it must be deserialized into a ContactInputModel object before it can be used by this function.  See https://fastapi.tiangolo.com/tutorial/body-parameters/#pydantic-models for more details on how to do this with Fast

    :param contact_id: int: Identify the contact to be updated
    :param body: ContactInputModel: Define the body of the request
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user that is currently logged in
    :return: The updated contact

    """
    return await put_contact(contact_id, body, current_user, db)


@router.delete('/del/{contact_id}', response_model=ContactResponseModel)
async def remove_contact(contact_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the contact to be deleted
    :param db: Session: Access the database
    :param current_user: User: Get the user that is currently logged in
    :return: The contact that was deleted

    """
    contact = await delete_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
