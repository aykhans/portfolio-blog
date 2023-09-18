from contextlib import contextmanager
from typing import Optional

from pydantic import (
    EmailStr,
    ValidationError,
    ConfigDict
)

from sys import path
path.append('.')

from app import crud
from app.schemas import UserCreate
from app.views.depends import get_db


class UserCreateCommand(UserCreate):
    model_config = ConfigDict(validate_assignment=True)

    email: Optional[EmailStr] = None
    password: Optional[str] = None


if __name__ == "__main__":
    user_in = UserCreateCommand()

    while 1:
        email = input('*Email: ')

        if not email:
            print('Email is required\n')
            continue

        try:
            user_in.email = email

        except ValidationError as e:
            print('\n', e, end='\n\n')
            continue

        with contextmanager(get_db)() as db:
            user = crud.user.sync_get_by_email(
                db,
                email=user_in.email
            )

        if user:
            print('User already exists\n')
            continue

        break

    while 1:
        username = input('Username: ')

        if username:
            try:
                user_in.username = username

            except ValidationError as e:
                print('\n', e, end='\n\n')
                continue

        break

    while 1:
        password = input('*Password: ')

        if not password:
            print('Password is required\n')
            continue

        try:
            user_in.password = password

        except ValidationError as e:
            print('\n', e, end='\n\n')
            continue

        break

    while 1:
        is_active = input('Is active? y/n (y): ') or 'y'

        if is_active == 'y':
            user_in.is_active = True

        elif is_active == 'n':
            user_in.is_active = False

        else:
            print('Invalid input\n')
            continue

        break

    while 1:
        is_superuser = input('Is superuser? y/n (n): ') or 'n'

        if is_superuser == 'y':
            user_in.is_superuser = True

        elif is_superuser == 'n':
            user_in.is_superuser = False

        else:
            print('Invalid input\n')
            continue

        break

    with contextmanager(get_db)() as db:
        user = crud.user.sync_create(
                db,
                obj_in=user_in
            )

    print(f'\nUser created:\n{user_in}\n')