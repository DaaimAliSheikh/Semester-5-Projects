import React, { useEffect, useState } from "react";
import useEmblaCarousel from "embla-carousel-react";
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  CardMedia,
  Dialog,
  Paper,
  Rating,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import Accordion from "@mui/material/Accordion";
import AccordionActions from "@mui/material/AccordionActions";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import api from "@/services/apiService";
import { Venue } from "@/types";
import { useQuery, useQueryClient } from "react-query";

const fetchVenues = async (): Promise<Venue[]> => {
  const { data } = await api.get("/venues"); // Replace with your API endpoint.
  return data;
};

const VenueCarousel = () => {
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: false });
  const [open, setOpen] = React.useState(false);

  const handleClose = () => {
    setOpen(false);
  };
  const queryClient = useQueryClient();
  const {
    data: venues,
    isLoading,
    isError,
  } = useQuery(["venues"], fetchVenues, {
    onError: (error: any) => {
      console.error("Error fetching venues");
    },
  });

  const [value, setValue] = useState(1); // Rating state
  const [comment, setComment] = useState(""); // Text input state

  const handleCommentChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setComment(event.target.value);
  };

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
              <>
                <Card
                  key={venue.venue_id}
                  sx={{
                    flex: "0 0 40%",
                    padding: 2,
                    border: "1px solid #ccc",
                    cursor: "pointer",
                    ":hover": {
                      boxShadow: 10,
                      bgcolor: "#f5f5f5",
                    },
                  }}
                  onClick={() => setOpen(true)}
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
                <Dialog
                  sx={(theme) => ({
                    color: "#fff",
                    zIndex: theme.zIndex.drawer + 1,
                  })}
                  open={open}
                  onClose={handleClose}
                >
                  <Card
                    key={venue.venue_id}
                    sx={{
                      flex: "0 0 40%",
                      padding: 2,
                      border: "1px solid #ccc",
                      width: "90vw",
                      maxWidth: "500px",
                    }}
                  >
                    <CardHeader color="primary.main" title={venue.venue_name} />

                    <Typography
                      variant="h5"
                      sx={{ mt: 3 }}
                      gutterBottom
                      align="center"
                    >
                      Add review
                    </Typography>
                    <form
                      onSubmit={async (event) => {
                        event.preventDefault();
                        if (!comment) return;
                        await api.post("/venues/reviews/" + venue.venue_id, {
                          venue_rating: value,
                          venue_review_text: comment,
                        });
                        queryClient.invalidateQueries(["venues"]);
                      }}
                    >
                      {/* Text Input */}
                      <TextField
                        fullWidth
                        label="Your Comment"
                        multiline
                        rows={4}
                        variant="outlined"
                        value={comment}
                        onChange={handleCommentChange}
                        sx={{ mb: 3 }}
                      />

                      {/* Rating */}
                      <Box display="flex" alignItems="center" sx={{ mb: 3 }}>
                        <Typography variant="body1" sx={{ mr: 2 }}>
                          Your Rating:
                        </Typography>
                        <Rating
                          value={value}
                          onChange={(_, newValue) => setValue(newValue || 1)}
                          size="large"
                        />
                      </Box>

                      {/* Submit Button */}
                      <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        fullWidth
                        sx={{
                          padding: "10px 0",
                          fontSize: "16px",
                          fontWeight: "bold",
                          borderRadius: "5px",
                          backgroundColor: "#007bff",
                          "&:hover": {
                            backgroundColor: "#0056b3",
                          },
                        }}
                      >
                        Submit
                      </Button>
                    </form>
                    <Accordion sx={{ mt: 3 }}>
                      <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1-content"
                        id="panel1-header"
                      >
                        Reviews
                      </AccordionSummary>
                      {venue.venue_reviews.map((review) => (
                        <AccordionDetails>
                          <Stack
                            direction="row"
                            justifyContent={"space-between"}
                            spacing={2}
                          >
                            <Box>
                              <Typography
                                variant="body1"
                                sx={{ py: 0, my: 0, fontWeight: "bold" }}
                              >
                                {review.user.username}
                              </Typography>
                              <Typography
                                variant="caption"
                                color="text.secondary"
                                sx={{ mb: 2 }}
                              >
                                {new Date(
                                  review.venue_review_created_at
                                ).toLocaleString()}
                              </Typography>
                            </Box>
                            <Rating
                              value={review.venue_rating}
                              onChange={(_, newValue) =>
                                setValue(newValue || 1)
                              }
                              readOnly
                              size="small"
                            />
                          </Stack>
                          <Typography variant="subtitle2">
                            {review.venue_review_text}
                          </Typography>
                        </AccordionDetails>
                      ))}
                    </Accordion>
                  </Card>
                </Dialog>
              </>
            );
          })}
        </Box>
      </Box>
    </Box>
  );
};

export default VenueCarousel;
