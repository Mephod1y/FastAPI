from datetime import timedelta, datetime

from sqlalchemy import extract, and_
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contact_by_email(email: str, db: Session):
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_name(name: str, db: Session):
    contact = db.query(Contact).filter_by(name=name).first()
    return contact


async def get_contact_by_second_name(second_name: str, db: Session):
    contact = db.query(Contact).filter_by(second_name=second_name).first()
    return contact


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.name = body.name
        contact.second_name = body.second_name
        contact.email = body.email
        contact.phone = body.phone
        contact.born_day = body.born_day
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contacts_by_birthday(db: Session):
    today = datetime.today().date()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(and_(extract('month', Contact.born_day) == next_week.month,
                                             extract('day', Contact.born_day) <= next_week.day,
                                             extract('day', Contact.born_day) >= today.day,
                                             )).all()
    upcoming_birthday_contacts = []
    for contact in contacts:
        bday_this_year = contact.born_day.replace(year=today.year)
        if bday_this_year >= today:
            upcoming_birthday_contacts.append(contact)
    return upcoming_birthday_contacts
