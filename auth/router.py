from fastapi import APIRouter, Depends, HTTPException
from config import AsyncSession,get_async_session
from fastapi_jwt_auth import AuthJWT

#import auth
from auth.schemas import UserForm, Settings
from auth.ldap import auth_ldap
from auth.models import Users,Groups
#alchemy
from sqlalchemy import select, insert,delete

@AuthJWT.load_config
def get_config():
    return Settings()

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post('/login')
async def login(user: UserForm, Authorize: AuthJWT = Depends(),
                session: AsyncSession = Depends(get_async_session)):
    UUID,user, username, user_groups= auth_ldap(user.username, user.password)
    if not user:
        raise HTTPException(status_code=401,detail="Bad username or password")
    # UUI
    in_db = select(Users.c.UUID).\
    where(Users.c.UUID==UUID)
    result = await session.execute(in_db)
    res = result.all()
    if not res:
        new_user = insert(Users).\
        values(UUID=UUID,
               Login=user,
               DisplayName=username)
        result = await session.execute(new_user)
        await session.commit()    
    old_groups=delete(Groups).where(Groups.c.UID ==UUID)
    result = await session.execute(old_groups)
    await session.commit()
    if user_groups:
        for g in user_groups:
            stmt = insert(Groups).\
            values(UID=UUID,
                G_UID=g)
            result = await session.execute(stmt)
            await session.commit()
    access_token = Authorize.create_access_token(subject=UUID)
    refresh_token = Authorize.create_refresh_token(subject=UUID)
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    
    return {"msg":"OK"}


@router.post('/refresh')
async def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}


@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}


@router.get('/me')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    return {"user": current_user}
