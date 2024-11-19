from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Venue, VenueReview
from uuid import UUID


class VenueService:
    async def get_venue(self, venue_id: UUID, session: AsyncSession):
        query = select(Venue).where(Venue.venue_id == venue_id)
        result = await session.exec(query)
        venue = result.first()
        return venue if venue else None

    async def get_venue_reviews(self, venue_id: UUID, session: AsyncSession):
        venue = await self.get_venue(venue_id, session)
        if venue:
            return venue.venue_reviews
        return None

    async def create_venue(self, venue_data: dict, session: AsyncSession):
        new_venue = Venue(**venue_data)
        session.add(new_venue)
        await session.commit()
        return new_venue

    async def delete_venue(self, venue_id: UUID, session: AsyncSession):
        
        query = select(Venue).where(Venue.venue_id == venue_id)
        results = await session.exec(query)
        venue = results.first()
        if not venue:
            return None
        await session.delete(venue)
        await session.commit()
        return venue
