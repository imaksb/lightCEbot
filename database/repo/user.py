from sqlalchemy import update, select
from sqlalchemy.dialects.postgresql import insert

from database.models.user import User
from database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_user(self, telegram_id):
        select_stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(select_stmt)
        return result.scalar()

    async def get_or_create_user(
        self,
        telegram_id: int, 
        full_name: str,
    ): 
        insert_stmt = (
            insert(User)
            .values(
                telegram_id=telegram_id,
                full_name=full_name,
            )
            .on_conflict_do_update(
                index_elements=[User.telegram_id],
                set_=dict(
                    full_name=full_name, 
                ),
            )
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def change_group(self, telegram_id: int, new_group: int):
        update_stmt = (
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(group=new_group)
        )
        await self.session.execute(update_stmt)
        await self.session.commit()
    
    async def change_getting_update_status(self, telegram_id: int):
        update_stmt = (
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(get_update=1 - User.get_update)
        )
        await self.session.execute(update_stmt)
        await self.session.commit()

    async def get_user_with_getting_update(self):
        select_stmt = (
            select(User)
            .where(User.get_update == 1)
        )
        result = await self.session.execute(select_stmt)
        return result.scalars().all()
