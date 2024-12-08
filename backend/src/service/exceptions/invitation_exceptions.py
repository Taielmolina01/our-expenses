MESSAGE_USER_ALREADY_REGISTERED_IN_GROUP = "User with email {user_email} already belongs to the groups"
MESSAGE_INVITATION_NOT_REGISTERED = "Invitation with id {invitation_id} does not exists"
MESSAGE_USER_ALREADY_INVITED_TO_GROUP = "User with email {user_email} was already invited"

class UserAlreadyRegisteredInGroup(Exception):
    def __init__(self, user_email):
        self.message = MESSAGE_USER_ALREADY_REGISTERED_IN_GROUP.format(user_email=user_email)
        super().__init__(self.message)

class InvitationNotRegistered(Exception):
    def __init__(self, invitation_id):
        self.message = MESSAGE_INVITATION_NOT_REGISTERED.format(invitation_id=invitation_id)
        super().__init__(self.message)

class UserAlreadyInvitedToGroup(Exception):
    def __init__(self, guest_email):
        self.message = MESSAGE_USER_ALREADY_INVITED_TO_GROUP.format(user_email=guest_email)
        super().__init__(self.message)
