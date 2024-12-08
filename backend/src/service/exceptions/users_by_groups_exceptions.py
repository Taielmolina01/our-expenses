MESSAGE_USER_NOT_REGISTERED_IN_GROUP = "User with email {user_email} does not belong to the group"

class UserNotRegisteredInGroup(Exception):
    def __init__(self, user_email):
        self.message = MESSAGE_USER_NOT_REGISTERED_IN_GROUP.format(user_email=user_email)
        super().__init__(self.message)