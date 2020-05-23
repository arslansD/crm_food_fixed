from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field, user_email

from users.utils import login_creator


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_number = data.get("phone")
        role_id = data.get("role_id")

        user_email(user, email)

        if first_name:
            user_field(user, 'first_name', first_name)
        if last_name:
            user_field(user, 'last_name', last_name)
        if phone_number:
            user_field(user, 'phone', phone_number)

        user_field(user, 'login', login_creator(last_name, first_name))
        user.role_id = role_id
        user.set_password(phone_number)

        self.populate_username(request, user)

        if commit:
            user.save()

        return user
