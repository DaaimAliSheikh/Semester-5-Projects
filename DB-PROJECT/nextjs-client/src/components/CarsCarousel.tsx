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
import api from "@/services/apiService"; // Ensure this is set up for your car API
import { CarModel } from "@/types"; // Assuming your types are already imported
import { useQuery } from "react-query";

// Fetch car data
const fetchCars = async (): Promise<CarModel[]> => {
  const { data } = await api.get("/cars"); // Replace with your API endpoint for cars
  return data;
};

const CarsCarousel = () => {
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: false });

  const {
    data: cars,
    isLoading,
    isError,
  } = useQuery(["cars"], fetchCars, {
    onError: (error: any) => {
      console.error("Error fetching cars");
    },
  });

  if (isLoading) {
    return (
      <Typography variant="h6" color="primary" align="center">
        Loading Cars...
      </Typography>
    );
  }

  if (isError) {
    return (
      <Typography variant="h6" color="error" align="center">
        Failed to load cars.
      </Typography>
    );
  }

  return (
    <Box sx={{ mt: 5 }}>
      <Typography variant="h4" color="primary" align="center" gutterBottom>
        Explore Our Car Rental Services
      </Typography>
      <Box
        sx={{ overflow: "hidden", width: "100%" }}
        className="embla"
        ref={emblaRef}
      >
        <Box sx={{ display: "flex", gap: 2 }} className="embla__container">
          {cars?.map((car) => {
            return (
              <Card
                key={car.car_id}
                sx={{ flex: "0 0 40%", padding: 2, border: "1px solid #ccc" }}
              >
                <CardHeader title={`${car.car_make} ${car.car_model}`} />
                {car.car_image && (
                  <CardMedia
                    component="img"
                    alt={`${car.car_make} ${car.car_model}`}
                    height="140"
                    image={car.car_image}
                  />
                )}
                <CardContent>
                  <Typography variant="body2" color="text.secondary">
                    Year: {car.car_year}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Rental Price: {car.car_rental_price} PKR / day
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Available Quantity: {car.car_quantity}
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

export default CarsCarousel;
