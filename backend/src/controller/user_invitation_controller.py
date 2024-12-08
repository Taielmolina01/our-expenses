from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_database
from src.models.user_invitation import UserInvitationModel
from src.service.exceptions.users_exceptions import *
from src.service.exceptions.invitation_exceptions import *
from src.service.user_invitation_service import UserInvitationService
from src.controller.login_controller import get_current_active_user
from src.models.user import UserModel

router = APIRouter()

@router.post("/invitations")
async def create_invitation(invitation: UserInvitationModel,
                            db: AsyncSession = Depends(get_database),
                            current_user: UserModel = Depends(get_current_active_user)):
    try: 
        return await UserInvitationService(db).create_invitation(invitation)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UserAlreadyRegisteredInGroup as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except UserAlreadyInvitedToGroup as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
    
@router.get("/invitations/{guest_email}")
async def get_invitations_by_guest(guest_email: str, 
                                   db: AsyncSession = Depends(get_database),
                                   current_user: UserModel = Depends(get_current_active_user)):
    try:
        return await UserInvitationService(db).get_invitations_by_guest(guest_email)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
    

@router.get("/invitations/{guest_email}/data")
async def get_invitations_by_guest_data(guest_email: str, 
                                   db: AsyncSession = Depends(get_database),
                                   current_user: UserModel = Depends(get_current_active_user)):
    try:
        return await UserInvitationService(db).get_invitations_by_guest_data(guest_email)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
    
@router.delete("/invitations/{invitation_id}/accept")
async def accept_invitation(invitation_id: int,
                            db: AsyncSession = Depends(get_database),
                            current_user: UserModel = Depends(get_current_active_user)):
    try:
        await UserInvitationService(db).accept_invitation(invitation_id)
    except InvitationNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

@router.delete("/invitations/{invitation_id}/reject")
async def reject_invitation(invitation_id: int,
                            db: AsyncSession = Depends(get_database),
                            current_user: UserModel = Depends(get_current_active_user)):
    try:
        await UserInvitationService(db).reject_invitation(invitation_id)
    except InvitationNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)