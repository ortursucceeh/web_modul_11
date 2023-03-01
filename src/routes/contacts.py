from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.services.auth import auth_service
from src.database.connect_db import get_db
from src.schemas import ContactModel, ContactResponse
from src.database.models import User
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user,  db)
    return contacts


@router.get("/{first_name}", response_model=List[ContactResponse])
async def read_contacts_with_name(first_name: str, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts_by_fname(first_name, current_user,  db)
    return contacts


@router.get("/{last_name}", response_model=List[ContactResponse])
async def read_contacts_with_lname(last_name: str, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts_by_lname(last_name, current_user,  db)
    return contacts


@router.get("/{email}", response_model=List[ContactResponse])
async def read_contacts_with_email(email: str, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts_by_email(email, current_user,  db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user,  db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
    
    
@router.get("//birthday", response_model=List[ContactResponse])
async def read_contact_by_birthday(db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contacts_by_birthday( current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
    

@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user,  db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user,  db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user,  db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact