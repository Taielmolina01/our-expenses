MESSAGE_PAYMENT_HAVE_NOT_CATEGORY = "Payment must have a category"
MESSAGE_PAYMENT_HAVE_MORE_DISTRIBUTIONS_THAN_GROUP_USERS = "Payment have more distributions than group's users"
MESSAGE_PAYMENT_HAVE_LESS_DISTRIBUTIONS_THAN_GROUP_USERS = "Payment have less distributions than group's users"
MESSAGE_PAYMENT_NOT_REGISTERED = "Payment with id {payment_id} does not exist"
MESSAGE_PAYMENT_DATE_IS_INVALID = "Payment date does not have the required format"

class PaymentNotRegistered(Exception):
    def __init__(self, payment_id):
        self.message = MESSAGE_PAYMENT_NOT_REGISTERED.format(payment_id)
        super().__init__(self.message)

class PaymentWithoutCategory(Exception):
    def __init__(self):
        self.message = MESSAGE_PAYMENT_HAVE_NOT_CATEGORY
        super().__init__(self.message)

class PaymentWithMoreDistributionsThanGroupUsers(Exception):
    def __init__(self):
        self.message = MESSAGE_PAYMENT_HAVE_MORE_DISTRIBUTIONS_THAN_GROUP_USERS
        super().__init__(self.message)

class PaymentWithLessDistributionsThanGroupUsers(Exception):
    def __init__(self):
        self.message = MESSAGE_PAYMENT_HAVE_LESS_DISTRIBUTIONS_THAN_GROUP_USERS
        super().__init__(self.message)

class PaymentDateIsInvalid(Exception):
    def __init__(self):
        self.message = MESSAGE_PAYMENT_DATE_IS_INVALID
        super().__init__(self.message)