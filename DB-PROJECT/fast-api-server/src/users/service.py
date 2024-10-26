from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from src.users.schemas import CreateUserModel, UpdateUserModel
from uuid import UUID


class UserService:
    async def get_all_users(self, session: AsyncSession):
        s = select(User).order_by(desc(User.created_at))
        result = await session.exec(s)
        return result.all()

    async def get_user(self, user_id: UUID, session: AsyncSession):
        s = select(User).where(User.id == user_id).order_by(
            desc(User.created_at))
        result = await session.exec(s)
        user = result.first()
        return user if user else None

    async def create_user(
        self, user_data: CreateUserModel,  session: AsyncSession
    ):
        new_user = User(**user_data.model_dump())
        session.add(new_user)
        # transaction, so can perform multiple actions, and commit all at once
        await session.commit()
        return new_user

    async def update_user(
        self, user_id: UUID, user_data: UpdateUserModel, session: AsyncSession
    ):
        old_user = await self.get_user(user_id, session)
        if not old_user:
            return None
        # exclude_unset=True only creates dict of non-None entries
        
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(old_user, key, value)

        await session.commit()
        # If you retrieve an existing object (like old_user) from the database and then modify its attributes,
        # the instance is tracked by the session
        # so just modify the retrieved object and commit the session to save changes
        return old_user   # old_user is the updated user at this point

    async def delete_user(self, user_id: UUID, session: AsyncSession):
        old_user = await self.get_user(user_id, session)
        if not old_user:
            return None
        await session.delete(old_user)
        await session.commit()
        return old_user  # object still exists in memory so we can return it
