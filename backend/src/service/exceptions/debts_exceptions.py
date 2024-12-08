MESSAGE_DEBT_IS_NEGATIVE = "Debt can not be a natural number"
MESSAGE_DEBT_NOT_REGISTERED = "Debt with id {debt_id} does not exists"
MESSAGE_DEBT_ALREADY_REGISTERED = "Debt with id {debt_id} already exists"

class DebtIsInvalid(Exception):
    def __init__(self):
        self.message = MESSAGE_DEBT_IS_NEGATIVE
        super().__init__(self.message)

class DebtNotRegistered(Exception):
    def __init__(self, debt_id):
        self.message = MESSAGE_DEBT_NOT_REGISTERED.format(debt_id=debt_id)
        super().__init__(self.message)

class DebtAlreadyRegistered(Exception):
    def __init__(self, debt_id):
        self.message = MESSAGE_DEBT_ALREADY_REGISTERED.format(debt_id=debt_id)
        super().__init__(self.message)