MESSAGE_USER_NOT_REGISTERED = "User with email {user_email} is not registered"
MESSAGE_USER_HAVE_NOT_NAME = "Username cannot be empty"
MESSAGE_USER_ALREADY_REGISTERED = "User with email {user_email} is already registered"
MESSAGE_WRONG_PASSWORD = "Wrong password"
MESSAGE_PASSWORD_CANT_BE_EMPTY = "Password cannot be empty"

class UserNotRegistered(Exception):
    def __init__(self, user_email):
        self.message = MESSAGE_USER_NOT_REGISTERED.format(user_email=user_email)
        super().__init__(self.message)

class UserWithoutName(Exception):
    def __init__(self):
        self.message = MESSAGE_USER_HAVE_NOT_NAME
        super().__init__(self.message)

class UserAlreadyRegistered(Exception):
    def __init__(self, user_email):
        self.message = MESSAGE_USER_ALREADY_REGISTERED.format(user_email=user_email)
        super().__init__(self.message)

class WrongPassword(Exception):
    def __init__(self):
        self.message = MESSAGE_WRONG_PASSWORD
        super().__init__(self.message)

    
class PasswordCanNotBeEmpty(Exception):
    def __init__(self):
        self.message = MESSAGE_PASSWORD_CANT_BE_EMPTY
        super().__init__(self.message)