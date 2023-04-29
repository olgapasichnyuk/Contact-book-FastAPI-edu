from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session, then returns the user with that email.

    :param email: str: Specify the email address of the user to be retrieved
    :param db: Session: Pass the database session to the function
    :return: The user with the given email address

    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
    Args:
    body (UserModel): The UserModel object containing the data to be inserted into the database.
    db (Session): The SQLAlchemy Session object used to interact with our PostgreSQL database.

    :param body: UserModel: Pass the user data to the function
    :param db: Session: Access the database
    :return: The new user object

    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user in the database
    :param token: str | None: Pass in the new token
    :param db: Session: Access the database
    :return: None, meaning it doesn't return anything
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()


async def mark_email_confirmed(email: str, db: Session) -> None:
    """
    The mark_email_confirmed function marks a user's email as confirmed in the database.

    :param email: str: Get the user's email
    :param db: Session: Pass the database session into the function
    :return: None

    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:

    """
    The update_avatar function updates the avatar of a user in the database.

    :param email: Identify the user
    :param url: str: Specify the type of data that is being passed into the function
    :param db: Session: Pass the database session to the function
    :return: The updated user object

    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user