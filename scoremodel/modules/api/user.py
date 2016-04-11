from sqlalchemy.orm import load_only
from copy import copy, deepcopy
from scoremodel.modules.api.generic import GenericApi
from scoremodel.modules.api.role import RoleApi
from scoremodel.models.user import User
from scoremodel.models.public import UserReport
from scoremodel import db, login_manager
from scoremodel.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist,\
    InvalidPassword


class UserApi(GenericApi):
    complex_params = ['questions', 'reports', 'roles']  # List of role_ids
    simple_params = ['email', 'password', 'username']
    required_params = ['email', 'password']
    possible_params = simple_params + complex_params

    def __init__(self):
        self.a_role = RoleApi()

    def create(self, input_data):
        """
        Add a new user. See TagApi.create().
        :param input_data:
        :return:
        """
        cleaned_data = self.clean_input(input_data)
        try:
            existing_user = self.get_by_user(cleaned_data['email'])
        except DatabaseItemDoesNotExist:
            existing_user = None
        if existing_user:
            raise DatabaseItemAlreadyExists('A user called {0} already exists.'.format(input_data['email']))
        new_user = User(email=cleaned_data['email'], password=input_data['password'])
        db.session.add(new_user)
        db.session.commit()
        # Add the roles
        for role_id in cleaned_data['roles']:
            new_user.roles.append(self.a_role.read(role_id))
        db.session.commit()
        return new_user

    def read(self, user_id):
        """
        Return a user by its id.
        :param user_id:
        :return:
        """
        existing_user = User.query.filter(User.id == user_id).first()
        if existing_user is None:
            raise DatabaseItemDoesNotExist('No user with id {0}'.format(user_id))
        return existing_user

    def update(self, user_id, input_data, update_password=True):
        """
        Update an existing user. See TagApi.update()
        If update_password is true, the password will be updated,
        even if it is empty. Otherwise, it will not be changed,
        even if it has changed from what we have in the DB.
        :param user_id:
        :param input_data:
        :param update_password:
        :return:
        """
        cleaned_data = self.clean_input(input_data)
        existing_user = self.read(user_id)
        # Update simple attributes
        existing_user = self.update_user(existing_user, cleaned_data, update_password=update_password)
        # Update roles
        existing_user = self.remove_roles(existing_user)
        for role_id in cleaned_data['roles']:
            existing_user.roles.append(self.a_role.read(role_id))
        db.session.commit()
        return existing_user

    def delete(self, user_id):
        """
        Delete a user identified by user_id. See TagApi.delete()
        :param user_id:
        :return:
        """
        existing_user = self.read(user_id)
        db.session.delete(existing_user)
        db.session.commit()
        return True

    def get_by_user(self, user_name):
        """
        Get a user by its user_name
        :param user_name:
        :return:
        """
        existing_user = User.query.filter(User.username == user_name).first()
        if existing_user is None:
            raise DatabaseItemDoesNotExist('No user called {0}'.format(user_name))
        return existing_user

    def check_password(self, user_id, user_password):
        """
        Check whether the password for a user_id is correct. If it is, return the user, otherwise, raise InvalidPassword
        :param user_id:
        :param user_password:
        :return:
        """
        existing_user = self.read(user_id)
        if existing_user.verify_password(user_password):
            return existing_user
        else:
            raise InvalidPassword

    def list(self):
        """
        List all users
        :return:
        """
        all_users = User.query.all()
        return all_users

    def clean_input(self, unclean_data):
        cleaned_data = self.clean_input_data(User, unclean_data, complex_params=self.complex_params,
                                             possible_params=self.possible_params, required_params=self.required_params)
        cleaned_data['username'] = cleaned_data['email']
        return cleaned_data

    def remove_roles(self, entity):
        for role in entity.roles:
            entity.roles.remove(role)
        db.session.commit()
        return entity

    def update_user(self, existing_user, cleaned_data, update_password=True):
        """
        Update an existing user with cleaned_data, but instead of directly setting user.password (which is impossible),
        it uses user.set_password(). However, we need to remove the item 'password' from simple_params or otherwise
        self.update_simple_attributes() will try to set it and fail. We will however, not call user.set_password()
        if update_password is false.
        :param existing_user:
        :param cleaned_data:
        :param update_password:
        :return:
        """
        unhashed_password = cleaned_data['password']
        simple_params = deepcopy(self.simple_params)
        simple_params.remove('password')
        # We can't set password via this method, because the database object only has password_hash
        existing_user = self.update_simple_attributes(existing_user, simple_params, cleaned_data)
        # Update password
        if update_password is True:
            existing_user.set_password(unhashed_password)
        return existing_user

    def get_user_reports(self, user_id):
        user = self.read(user_id)
        return user.reports

    def add_user_report(self, user_id, report):
        user = self.read(user_id)
        user.reports.append(report)
        db.commit()
        return user


@login_manager.user_loader
def load_user(user_id):
    a_user = UserApi()
    try:
        user = a_user.read(int(user_id))
    except DatabaseItemDoesNotExist:
        user = None
    return user
