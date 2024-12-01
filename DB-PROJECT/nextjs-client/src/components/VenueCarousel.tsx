import React, { useEffect } from "react";
import useEmblaCarousel from "embla-carousel-react";
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  CardMedia,
  Rating,
  Typography,
} from "@mui/material";
import api from "@/services/apiService";
import { Venue } from "@/types";
import { useQuery } from "react-query";

const fetchVenues = async (): Promise<Venue[]> => {
  const { data } = await api.get("/venues"); // Replace with your API endpoint.
  return data;
};

const VenueCarousel = () => {
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: false });

 
  const {
    data: venues,
    isLoading,
    isError,
  } = useQuery(["venues"], fetchVenues, {
    onError: (error: any) => {
      console.error("Error fetching venues");
    },
  });

  return (
    <Box>
      <Typography variant="h4" color="primary" align="center" gutterBottom>
        Explore Our Venues
      </Typography>
      <Box
        sx={{ overflow: "hidden", width: "100%" }}
        className="embla"
        ref={emblaRef}
      >
        <Box sx={{ display: "flex", gap: 2 }} className="embla__container">
          {venues?.map((venue) => {
            // Calculate average rating
            const totalRatings = venue.venue_reviews.reduce(
              (acc, review) => acc + review.venue_rating,
              0
            );
            const averageRating = venue.venue_reviews.length
              ? Math.round(totalRatings / venue.venue_reviews.length)
              : 0;
            return (
              <Card
                key={venue.venue_id}
                sx={{ flex: "0 0 40%", padding: 2, border: "1px solid #ccc" }}
              >
                <CardHeader title={venue.venue_name} />
                {venue.venue_image && (
                  <CardMedia
                    component="img"
                    alt={venue.venue_name}
                    height="140"
                    image={venue.venue_image}
                  />
                )}
                <CardContent>
                  <Typography variant="body2" color="text.secondary">
                    location: {venue.venue_address}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    venue capacity: {venue.venue_capacity}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    venue price per day: {venue.venue_price_per_day}
                  </Typography>
                  <Box mt={2}>
                    {averageRating > 0 ? (
                      <Rating value={averageRating} readOnly />
                    ) : (
                      "No ratings yet"
                    )}
                  </Box>
                </CardContent>
              </Card>
            );
          })}
        </Box>
     
      </Box>
    </Box>
  );
};

export default VenueCarousel;
