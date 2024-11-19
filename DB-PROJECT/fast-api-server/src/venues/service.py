from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Venue, VenueReview
from src.venues.schemas import CreateVenueModel, CreateVenueReviewModel
from uuid import UUID


class VenueService:
    async def get_all_venues(self, session: AsyncSession):
        query = select(Venue)
        result = await session.exec(query)
        venues = result.all()
        raise Exception("lol")
        return venues

    async def get_venue(self, venue_id: UUID, session: AsyncSession):
        query = select(Venue).where(Venue.venue_id == venue_id)
        result = await session.exec(query)
        venue = result.first()
        return venue if venue else None

    async def create_venue(self, venue_data: CreateVenueModel, session: AsyncSession):
        new_venue = Venue(**venue_data.model_dump())
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

    async def get_venue_reviews(self, venue_id: UUID, session: AsyncSession):
        venue = await self.get_venue(venue_id, session)
        if venue:
            return venue.venue_reviews
        return None

    async def create_review(self, venue_id: UUID, venue_review_data: CreateVenueReviewModel, session: AsyncSession) -> VenueReview:
        # Create a new venue review
        new_review = VenueReview(
            **venue_review_data.model_dump(), venue_id=venue_id)
        # Add the review to the session and commit the transaction
        session.add(new_review)
        await session.commit()
        # Refresh the instance to get the updated data
        await session.refresh(new_review)

        return new_review