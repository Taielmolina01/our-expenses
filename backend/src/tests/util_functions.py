import datetime
from datetime import date, datetime
from sqlalchemy.future import select
from src.models.debt import DebtState
from src.models.user import UserModel
from src.models.group import GroupModel, GroupUpdate
from src.models.user_invitation import UserInvitationModel
from src.tables.debt_base import DebtBase
from src.tables.payment_base import PaymentBase
from src.tables.user_base import UserBase
from src.tables.group_base import GroupBase
from src.tables.user_in_group_base import UserInGroupBase
from src.models.user_in_group import UserInGroupModel
from src.models.payment import PaymentModel, Category, PaymentUpdate
from src.tables.user_invitation_base import UserInvitationBase

def create_group_model():
    return GroupModel(name="MyGroup")

def create_group_model_2():
    return GroupModel(name="MyGroup2")

def create_user_model():
    return UserModel(
        email="test@example.com",
        name="MyUser1",
        password="securepassword1"
    )

def create_user_model_2():
    return UserModel(
        email="test2@example.com",
        name="MyUser2",
        password="securepassword2"
    )

def create_user_model_not_registered():
    return UserModel(
        email="non_member@example.com", 
        name="Single User", 
        password="password"
    )

def create_group_model_without_name():
    return GroupModel(name="")

def create_user_in_group_model(user: UserModel, 
                               group: GroupBase):
    myId = group.group_id
    return UserInGroupModel(    
            group_id=myId,
            user_email=user.email)

def create_payment_model(payer: UserBase, group: GroupBase, category: Category):
    email = payer.email
    myId = group.group_id
    return PaymentModel(
        group_id=myId,
        description="MyPayment",
        payer_email=email,
        payment_date="2024-10-21",
        category=category,
        amount=200
    )

def create_update_payment_model(amount: int):
    return PaymentUpdate(
        amount=amount
    )

def create_debt_model(payment_id: int, group_id: int, debtor_email: str, creditor_email: str, percentage: float):
    return DebtBase(
        payment_id=payment_id,
        group_id=group_id,
        debtor_email=debtor_email,
        creditor_email=creditor_email,
        percentage=percentage
    )

def create_invitation_model(host_email, guest_email):
    return UserInvitationModel(
        invitator_email=host_email,
        guest_email=guest_email,
        group_id=1,
        send_date=date(2024, 10, 21),
        expire_date=date(2024, 10, 28)
    )

def update_debt_to_json(state: DebtState):
    return {
        "state": state.value
    }

async def log_in_user(client, user: UserModel):
    data = {
        "username": user.email,
        "password": user.password
    }
    return await client.post("/login", data=data)

def payment_to_json(payment: PaymentBase, dict: dict[str, float]):
    return {
        "payment": {
            "group_id": payment.group_id,
            "description": payment.description,
            "payer_email": payment.payer_email,
            "payment_date": payment.payment_date,
            "category": payment.category.value,
            "amount": payment.amount,
        },
        "percentages": dict
    }

def json_to_payments(json_list):
    payments = []
    for json in json_list:
        payment = PaymentBase(
        group_id=json["group_id"],
        description=json["description"],
        payer_email=json["payer_email"],
        payment_date=datetime.strptime(json["payment_date"], "%Y-%m-%d").date(),
        category=json["category"],
        amount=json["amount"]
    )
        payments.append(payment)
    return payments

def json_to_balances(json_list):
    balances = []
    for json in json_list:
        balances.append(UserInGroupBase(
            group_id=json["group_id"],
            user_email=json["user_email"],
            balance=json["balance"]
        ))
    return balances

def invitation_to_json(invitation: UserInvitationModel):
    return {
        "invitator_email": invitation.invitator_email,
        "guest_email": invitation.guest_email,
        "group_id": invitation.group_id,
        "send_date": invitation.send_date.strftime("%Y-%m-%d"),
        "expire_date": invitation.expire_date.strftime("%Y-%m-%d")
    }

def json_to_invitation(json_list):
    invitations = []
    for json in json_list:
        invitation = UserInvitationBase(
            invitation_id=int(json["invitation_id"]),
            invitator_email=json["invitator_email"],
            guest_email=json["guest_email"],
            group_id=int(json["group_id"]),
            send_date=datetime.strptime(json["send_date"], "%Y-%m-%d").date(),
            expire_date=datetime.strptime(json["expire_date"], "%Y-%m-%d").date()
        )
        invitations.append(invitation)
    return invitations

def json_to_groups(json_list):
    groups = []
    for json in json_list:
        group = GroupModel(
            name=json["name"],
        )
        groups.append(group)
    return groups

def user_to_json(user: UserBase):
    return {
        "email": user.email,
        "name": user.name,
        "password": user.password
    }

def json_to_user(json):
    return UserBase(
        email=json["email"],
        name=json["name"],
        password=json["password"]
    )

def group_to_json(group: GroupBase):
    return {
        "name": group.name
    }

def group_update_to_json(group: GroupUpdate):
    return {
        "name": group.name
    }

def json_to_group(json):
    return GroupBase(
        name=json["name"],
        group_id=int(json["group_id"]) 
    )

def user_in_group_to_json(user_in_group: UserInGroupModel):
    return {
        "group_id": user_in_group.group_id,
        "user_email": user_in_group.user_email
    }

def json_to_debts(json_list):
    debts = []
    for json in json_list:
        debt = DebtBase(
            debt_id=json["debt_id"],
            payment_id=json["payment_id"],
            group_id=json["group_id"],
            debtor_email=json["debtor_email"],
            creditor_email=json["creditor_email"],
            percentage=json["percentage"]
        )
        debts.append(debt)
    return debts
