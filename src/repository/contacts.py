from typing import List
from datetime import datetime, timedelta

from sqlalchemy import extract, func
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.
    
    
    :param skip: int: Skip the first n records
    :param limit: int: Limit the number of contacts returned
    :param user: User: Get the user_id from the user model
    :param db: Session: Access the database
    :return: A list of contacts
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact function returns a contact from the database.
        Args:
            contact_id (int): The id of the contact to be returned.
            user (User): The user who owns the requested Contact object.
            db (Session): A database session for querying and updating data in a relational database.
    
    :param contact_id: int: Get the contact with that id
    :param user: User: Get the user_id of the contact
    :param db: Session: Access the database
    :return: A contact object
    """
    return db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()

async def get_contacts_by_fname(first_name: str, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts_by_fname function returns a list of contacts that match the first name provided.
        
    
    :param first_name: str: Filter the contacts by first name
    :param user: User: Get the user_id from the user object
    :param db: Session: Pass the database session to the function
    :return: A list of contacts with the matching first name
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.user_id == user.id, func.lower(Contact.first_name).like(f'%{first_name.lower()}%'))).all()

async def get_contacts_by_lname(last_name: str, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts_by_lname function returns a list of contacts that match the last name provided.
        
    
    :param last_name: str: Define the last name of the contact you are searching for
    :param user: User: Get the user_id from the user object
    :param db: Session: Access the database
    :return: A list of contacts with the last name matching the query
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.user_id == user.id,  func.lower(Contact.last_name).like(f'%{last_name.lower()}%'))).all()

async def get_contacts_by_email(email: str, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts_by_email function returns a list of contacts that match the email provided.
        
    
    :param email: str: Filter the contacts by email
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A list of contacts that match the email
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.user_id == user.id,  Contact.email).like(f'%{email}%')).all()

async def get_contacts_by_birthday(user: User, db: Session) -> List[Contact]:
    """
    The get_contacts_by_birthday function returns a list of contacts whose birthday is within the next week.
    
    
    :param user: User: Get the user's id, which is used to filter out contacts that belong to other users
    :param db: Session: Pass in the database session
    :return: A list of contacts whose birthday is within the next 7 days
    """
    today = datetime.today().date()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(and_(Contact.user_id == user.id, 
        extract('month', Contact.birthday) == next_week.month,
        extract('day', Contact.birthday) <= next_week.day,
        extract('day', Contact.birthday) >= today.day,
    )).all()

    upcoming_birthday_contacts = []
    for contact in contacts:
        bday_this_year = contact.birthday.replace(year=today.year)
        if bday_this_year >= today:
            upcoming_birthday_contacts.append(contact)
    return upcoming_birthday_contacts

async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactModel: Pass in the json data from the request body
    :param user: User: Get the user_id from the user model
    :param db: Session: Connect to the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email, phone=body.phone, birthday=body.birthday, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        Args:
            note_id (int): The id of the contact to update.
            body (ContactUpdate): The updated information for the contact.
            user (User): The user who is updating this contact.
        Returns:
            Contact | None: A Contact object if successful, otherwise None.
    
    :param note_id: int: Identify which contact to update
    :param body: ContactUpdate: Pass the json data to the function
    :param user: User: Get the user id of the current user
    :param db: Session: Pass the database session to the function
    :return: A contact object, which is a model
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact

async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who owns the contacts list.
            db (Session): A session object for interacting with a SQLAlchemy database engine.
        Returns: 
            Contact | None: If successful, returns an instance of Contact; otherwise, returns None.
    
    :param contact_id: int: Identify the contact to be removed
    :param user: User: Get the user_id from the user object
    :param db: Session: Pass the database session to the function
    :return: A contact object
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact



