from pathlib import Path

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel


class EmailSchema(BaseModel):
    email: EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME="ortursucceeh778@meta.ua",
    MAIL_PASSWORD="QWEqweqwe123123123",
    MAIL_FROM="ortursucceeh778@meta.ua",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Example email",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

app = FastAPI()


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    """
    The send_in_background function is a helper function that will send an email in the background.
    It takes two arguments:
        - background_tasks: A BackgroundTasks object from FastAPI, which allows us to run tasks in the background.
        - body: The request body, which contains an email address and a password reset token.  This information is used to populate our template.
    
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param body: EmailSchema: Get the email address of the user
    :return: A dictionary with a message key
    """
    message = MessageSchema(
        subject="Reset a user's password",
        recipients=[body.email],
        template_body={"fullname": "Billy Jones"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

    return {"message": "email has been sent"}


if __name__ == '__main__':
    uvicorn.run('send-email:app', port=8000, reload=True)