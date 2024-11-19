from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.users.schemas import UserModel
from src.venues.service import VenueService
from src.venues.schemas import VenueModel, CreateVenueModel, VenueReviewModel, CreateVenueReviewModel
from uuid import UUID
from src.users.JWTAuthMiddleware import JWTAuthMiddleware

venue_router = APIRouter(prefix="/venues")
venue_service = VenueService()


@venue_router.get("/", response_model=list[VenueModel], status_code=status.HTTP_200_OK)
async def get_all_venues( session: AsyncSession = Depends(get_session)):
    venues = await venue_service.get_all_venues( session)
    return venues


@venue_router.get("/{venue_id}", response_model=VenueModel, status_code=status.HTTP_200_OK)
async def get_venue(venue_id: UUID, session: AsyncSession = Depends(get_session)):
    venue = await venue_service.get_venue(venue_id, session)
    if venue:
        return venue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Venue not found")


@venue_router.get("/{venue_id}/reviews", response_model=list[VenueReviewModel], status_code=status.HTTP_200_OK)
async def get_venue_reviews(venue_id: UUID, session: AsyncSession = Depends(get_session)):
    reviews = await venue_service.get_venue_reviews(venue_id, session)
    if reviews is not None:
        return reviews
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Venue not found")


@venue_router.post("/{venue_id}/reviews", status_code=status.HTTP_201_CREATED)
async def create_review(
    venue_id: UUID,
    venue_review_data: CreateVenueReviewModel,
    # This will give us the user details
    user: UserModel = Depends(JWTAuthMiddleware),
    session: AsyncSession = Depends(get_session)
):
    if user.is_admin:  # only users can submit reviews
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admins cannot submit reviews")
    venue_review = await venue_service.create_review(venue_id, venue_review_data, session)
    return venue_review


@venue_router.post("/", response_model=VenueModel, status_code=status.HTTP_201_CREATED)
async def create_venue(
    venue_data: CreateVenueModel,
    # This will give us the user details
    user: UserModel = Depends(JWTAuthMiddleware),
    session: AsyncSession = Depends(get_session),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    venue = await venue_service.create_venue(venue_data, session)
    return venue


@venue_router.delete("/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_venue(
    venue_id: UUID,
    user: UserModel = Depends(JWTAuthMiddleware),
    session: AsyncSession = Depends(get_session),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    deleted = await venue_service.delete_venue(venue_id, session)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")
    return deleted
