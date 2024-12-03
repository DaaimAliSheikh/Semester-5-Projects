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
import api from "@/services/apiService"; // Ensure this is set up for your dish API
import { DishModel } from "@/types"; // Assuming your types are already imported
import { useQuery } from "react-query";

// Fetch dish data
const fetchDishes = async (): Promise<DishModel[]> => {
  const { data } = await api.get("/caterings/dishes"); // Replace with your API endpoint for dishes
  return data;
};

const DishCarousel = () => {
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: false });

  const {
    data: dishes,
    isLoading,
    isError,
  } = useQuery(["dishes"], fetchDishes, {
    onError: (error: any) => {
      console.error("Error fetching dishes");
    },
  });

  if (isLoading) {
    return (
      <Typography variant="h6" color="primary" align="center">
        Loading Dishes...
      </Typography>
    );
  }

  if (isError) {
    return (
      <Typography variant="h6" color="error" align="center">
        Failed to load dishes.
      </Typography>
    );
  }

  return (
    <Box sx={{ mt: 5 }}>
      <Typography variant="h4" color="primary" align="center" gutterBottom>
        Explore Our Delicious Dishes
      </Typography>
      <Box
        sx={{ overflow: "hidden", width: "100%" }}
        className="embla"
        ref={emblaRef}
      >
        <Box sx={{ display: "flex", gap: 2 }} className="embla__container">
          {dishes?.map((dish) => {
            return (
              <Card
                key={dish.dish_id}
                sx={{ flex: "0 0 40%", padding: 2, border: "1px solid #ccc" }}
              >
                <CardHeader title={dish.dish_name} />
                {dish.dish_image && (
                  <CardMedia
                    component="img"
                    alt={dish.dish_name}
                    height="140"
                    image={dish.dish_image}
                  />
                )}
                <CardContent>
                  <Typography variant="body2" color="text.secondary">
                    Type: {dish.dish_type}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Description: {dish.dish_description}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Cost per Serving: {dish.dish_cost_per_serving} PKR
                  </Typography>
                </CardContent>
              </Card>
            );
          })}
        </Box>
      </Box>
    </Box>
  );
};

export default DishCarousel;
