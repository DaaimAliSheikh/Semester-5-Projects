import React, { useEffect } from "react";
import useEmblaCarousel from "embla-carousel-react";
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  CardMedia,
  IconButton,
  Typography,
} from "@mui/material";
import api from "@/services/apiService";
import { CateringModel, CateringMenuItemModel, DishModel } from "@/types"; // Import the appropriate types
import { useQuery } from "react-query";

// Fetch catering data
const fetchCateringsAndDishes = async (): Promise<
  {
    catering: CateringModel;
    dishes: DishModel[];
  }[]
> => {
  const { data } = await api.get("/caterings"); // Replace with your API endpoint
  const cateringPromises = data.map(async (catering: CateringModel) => {
    const dishPromises = catering.catering_menu_items.map(
      async (item: CateringMenuItemModel) => {
        const { data } = await api.get(`/caterings/dishes/${item.dish_id}`);
        return data;
      }
    );

    const dishes = await Promise.all(dishPromises);
    return { catering, dishes };
  });
  return await Promise.all(cateringPromises);
};

const CateringCarousel = () => {
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: false });

  const {
    data: cateringsAndDishes,
    isLoading,
    isError,
  } = useQuery(["caterings"], fetchCateringsAndDishes, {
    onError: (error: any) => {
      console.error("Error fetching caterings");
    },
  });

  if (isLoading) return <Typography>Loading...</Typography>;
  if (isError) return <Typography>Error fetching data</Typography>;

  return (
    <Box sx={{ mt: 5 }}>
      <Typography
        variant="h4"
        sx={{ my: 2 }}
        color="primary"
        align="center"
        gutterBottom
      >
        Our Catering Services Partners
      </Typography>
      <Box
        sx={{ overflow: "hidden", position: "relative", width: "100%" }}
        className="embla"
        ref={emblaRef}
      >
        <Box sx={{ display: "flex", gap: 2 }} className="embla__container">
          {cateringsAndDishes?.map((cateringAndDishes) => {
            return (
              <Card
                key={cateringAndDishes.catering.catering_id}
                sx={{ flex: "0 0 40%", padding: 2, border: "1px solid #ccc" }}
              >
                <CardHeader title={cateringAndDishes.catering.catering_name} />
                {cateringAndDishes.catering.catering_image && (
                  <CardMedia
                    component="img"
                    alt={cateringAndDishes.catering.catering_name}
                    height="140"
                    image={cateringAndDishes.catering.catering_image}
                  />
                )}
                <CardContent>
                  <Typography variant="body2" color="text.secondary">
                    Description:{" "}
                    {cateringAndDishes.catering.catering_description}
                  </Typography>
                  <Box mt={2}>
                    <Typography variant="h6" color="text.primary">
                      Menu Items:
                    </Typography>
                    <ul>
                      {cateringAndDishes.dishes.map((dish, index) => (
                        <li key={index}>
                          <Typography variant="body2" color="text.secondary">
                            {dish.dish_name}: ${dish.dish_cost_per_serving} per
                            serving
                          </Typography>
                        </li>
                      ))}
                    </ul>
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

export default CateringCarousel;
