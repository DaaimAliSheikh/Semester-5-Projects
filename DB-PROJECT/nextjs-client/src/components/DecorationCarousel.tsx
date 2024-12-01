import React from "react";
import useEmblaCarousel from "embla-carousel-react";
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  CardMedia,
  Typography,
} from "@mui/material";
import api from "@/services/apiService"; // Ensure this is set up for your decoration API
import { DecorationModel } from "@/types"; // Assuming your types are already imported
import { useQuery } from "react-query";

// Fetch decoration data
const fetchDecorations = async (): Promise<DecorationModel[]> => {
  const { data } = await api.get("/decorations"); // Replace with your API endpoint for decorations
  return data;
};

const DecorationCarousel = () => {
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: false });

  const {
    data: decorations,
    isLoading,
    isError,
  } = useQuery(["decorations"], fetchDecorations, {
    onError: (error: any) => {
      console.error("Error fetching decorations");
    },
  });

  if (isLoading) {
    return (
      <Typography variant="h6" color="primary" align="center">
        Loading Decorations...
      </Typography>
    );
  }

  if (isError) {
    return (
      <Typography variant="h6" color="error" align="center">
        Failed to load decorations.
      </Typography>
    );
  }

  return (
    <Box sx={{ mt: 5 }}>
      <Typography variant="h4" color="primary" align="center" gutterBottom>
        Our Decorations Services Partners
      </Typography>
      <Box
        sx={{ overflow: "hidden", width: "100%" }}
        className="embla"
        ref={emblaRef}
      >
        <Box sx={{ display: "flex", gap: 2 }} className="embla__container">
          {decorations?.map((decoration) => {
            return (
              <Card
                key={decoration.decoration_id}
                sx={{ flex: "0 0 40%", padding: 2, border: "1px solid #ccc" }}
              >
                <CardHeader title={decoration.decoration_name} />
                {decoration.decoration_image && (
                  <CardMedia
                    component="img"
                    alt={decoration.decoration_name}
                    height="140"
                    image={decoration.decoration_image}
                  />
                )}
                <CardContent>
                  <Typography variant="body2" color="text.secondary">
                    Description: {decoration.decoration_description}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Price: {decoration.decoration_price} PKR
                  </Typography>
                  <Box mt={2}>
                    {/* Optional: Add a rating system for decorations */}
                    {/* <Rating value={decoration.averageRating} readOnly /> */}
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

export default DecorationCarousel;
