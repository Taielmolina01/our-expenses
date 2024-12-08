MESSAGE_GROUP_NOT_REGISTERED = "Group does not exists"
MESSAGE_GROUP_HAVE_NOT_NAME = "Groupname can not be empty"
MESSAGE_USER_NOT_AUTHORIZED = "User is not authorized to do this action"

class GroupNotRegistered(Exception):
    def __init__(self):
        self.message = MESSAGE_GROUP_NOT_REGISTERED
        super().__init__(self.message)

class UserNotAuthorized(Exception):
    def __init__(self):
        self.message = MESSAGE_USER_NOT_AUTHORIZED
        super().__init__(self.message)

class GroupWithoutName(Exception):
    def __init__(self):
        self.message = MESSAGE_GROUP_HAVE_NOT_NAME
        super().__init__(self.message)