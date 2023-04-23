from datetime import date, timedelta, datetime
from typing import List

from pydantic import EmailStr
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactInputModel


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def post_contact(body: ContactInputModel, user: User, db: Session) -> Contact:
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
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def match_by_name(name: str, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(and_(Contact.name == name, Contact.user_id == user.id)).all()


async def match_by_surname(surname: str, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(and_(Contact.surname == surname, Contact.user_id == user.id)).all()


async def match_by_email(email: EmailStr, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).first()


async def get_birthdays_week(db: Session, user: User):

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

