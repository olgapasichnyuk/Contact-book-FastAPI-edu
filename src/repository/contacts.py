from datetime import date, timedelta, datetime
from typing import List

from pydantic import EmailStr
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactInputModel


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.

    :param skip: int: Skip over a certain number of contacts
    :param limit: int: Limit the number of contacts returned
    :param user: User: Get the user_id from the database
    :param db: Session: Access the database
    :return: A list of contacts

    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact function takes in a contact_id and user, and returns the contact with that id.
    Args:
        contact_id (int): The id of the desired Contact object.
        user (User): The User object associated with this Contact.

    :param contact_id: int: Specify the contact id of the contact to be retrieved
    :param user: User: Get the user_id from the user object
    :param db: Session: Access the database
    :return: The contact object

    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def post_contact(body: ContactInputModel, user: User, db: Session) -> Contact:
    """
    The post_contact function creates a new contact in the database.

    :param body: ContactInputModel: Get the data from the request body
    :param user: User: Get the user id from the token that is passed in
    :param db: Session: Access the database
    :return: The contact object that was added

    """
    contact = Contact(name=body.name,
                      surname=body.surname,
                      birthday=body.birthday,
                      email=body.email,
                      phone=body.phone,
                      user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def put_contact(contact_id: int, body: ContactInputModel, user: User, db: Session) -> Contact:
    """
    The put_contact function updates a contact in the database.
    Args:
    contact_id (int): The id of the contact to update.
    body (ContactInputModel): A ContactInputModel object containing all fields that can be updated for a given user's contacts.

    :param contact_id: int: Identify the contact that is being updated
    :param body: ContactInputModel: Get the data from the request body
    :param user: User: Check if the user is logged in
    :param db: Session: Access the database
    :return: The contact object

    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.birthday = body.birthday
        contact.email = body.email
        contact.phone = body.phone

        db.commit()
    return contact


async def delete_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The delete_contact function deletes a contact from the database.
    Args:
    contact_id (int): The id of the contact to be deleted.
    user (User): The user who is deleting the contact.  This is used to ensure that only contacts belonging to this user are deleted, and not contacts belonging to other users with similar IDs.
    db (Session): A connection object for interacting with our database using SQLAlchemy's ORM methods.

    :param contact_id: int: Identify the contact to be deleted
    :param user: User: Identify the user that is making the request
    :param db: Session: Access the database
    :return: The deleted contact

    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_everywhere_contacts(parameter: str, user: User, db: Session):
    """
    The search_everywhere_contacts function searches for contacts in the database that match a given parameter.
    The function takes three parameters:
    - parameter: A string containing the search term to be used when searching for contacts.
    - user: An object of type User, representing the user who is currently logged in and using this function.
    This is needed because we want to return only those contacts that belong to this particular user,
    not all users' contacts from the database. We can get it from our request's context (see below).

    :param parameter: str: Search for a contact in the database
    :param user: User: Get the user id of the current logged in user
    :param db: Session: Access the database and perform queries on it
    :return: A list of contacts that match the parameter

    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).filter(or_(Contact.name.contains(parameter),
                                                                               Contact.surname.contains(parameter),
                                                                               Contact.email.contains(parameter))).all()
    return contacts


async def filter_contacts(name: str, surname: str, email: str, user: User, db: Session):

    """
    The filter_contacts function filters contacts by name, surname and email.
    Args:
    name (str): The contact's first name.
    surname (str): The contact's last name.
    email (str): The contact's email address.

    :param name: str: Filter the contacts by name
    :param surname: str: Filter contacts by surname
    :param email: str: Filter the contacts by email address
    :param user: User: Get the user id from the token
    :param db: Session: Pass the database session to the function
    :return: A list of contacts that match the criteria

    """

    contacts = db.query(Contact).filter(and_(Contact.user_id == user.id,
                                             Contact.name.contains(name),
                                             Contact.surname.contains(surname),
                                             Contact.email.contains(email))).all()
    return contacts


# async def match_by_name(name: str, user: User, db: Session) -> List[Contact]:
#     return db.query(Contact).filter(and_(Contact.name == name, Contact.user_id == user.id)).all()
#
#
# async def match_by_surname(surname: str, user: User, db: Session) -> List[Contact]:
#     return db.query(Contact).filter(and_(Contact.surname == surname, Contact.user_id == user.id)).all()
#
#
# async def match_by_email(email: EmailStr, user: User, db: Session) -> Contact:
#     return db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).first()


async def get_birthdays_week(db: Session, user: User):

    """
    The get_birthdays_week function returns a list of contacts whose birthdays are within the next 7 days.
    Args:
    db (Session): The database session to use for querying.
    user (User): The user who's contacts we want to query.

    :param db: Session: Connect to the database
    :param user: User: Get the user id from the user object
    :return: A list of contacts whose birthdays are in the next week

    """

    today = date.today()


    if today.day <= 21:
        next_week_days = [str(today.day + x) for x in range(7)]
        next_week_days = list(map((lambda x: '0' + x if len(x) < 2 else x), next_week_days))

        current_month = str(today.month)
        if len(current_month) < 2:
            current_month = '0' + current_month

        contacts = db.query(Contact).filter(and_(Contact.user_id == user.id, func.date_part('month', Contact.birthday) == current_month,
                                            func.date_part('day', Contact.birthday).in_(next_week_days))).all()

    else:
        next_week = [((today + timedelta(x)).day, (today + timedelta(x)).month) for x in range(7)]

        contacts = []
        for day, month in next_week:
            contacts.extend(db.query(Contact).filter(and_(Contact.user_id == user.id, func.date_part('month', Contact.birthday) == month,
                                                     func.date_part('day', Contact.birthday) == day)).all())

    return contacts

