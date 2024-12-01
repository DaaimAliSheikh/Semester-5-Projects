import { z } from "zod";

export interface VenueReview {
  venue_review_id: string;
  venue_id: string;
  user: { id: string; username: string }; // Assuming the `UserModel` includes an `id` and `username`.
  venue_review_text: string;
  venue_rating: number;
  venue_review_created_at: string;
}

export interface Venue {
  venue_id: string;
  venue_name: string;
  venue_address: string;
  venue_capacity: number;
  venue_price_per_day: number;
  venue_image?: string;
  venue_reviews: VenueReview[];
}

export interface CreateVenueModel {
  venue_name: string;
  venue_address: string;
  venue_capacity: number;
  venue_price_per_day: number;
  venue_image?: File | null;
}

export const createVenueSchema = z.object({
  venue_name: z
    .string()
    .min(3, "Venue name must be at least 3 characters long."),
  venue_address: z
    .string()
    .min(5, "Address must be at least 5 characters long."),
  venue_capacity: z.number().min(1, "Capacity must be at least 1."),
  venue_price_per_day: z.number().min(0, "Price per day cannot be negative."),
  venue_image: z
    .instanceof(File)
    .optional()
    .nullable()
    .refine(
      (file) =>
        !file ||
        ["image/jpeg", "image/webp", "image/png", "image/gif"].includes(
          file.type
        ),
      {
        message: "Only JPEG, WEBP, PNG, or GIF images are allowed.",
      }
    ),
});

export type CreateVenueFormValues = z.infer<typeof createVenueSchema>;

export interface CarModel {
  car_id: string;
  car_make: string;
  car_model: string;
  car_year: number;
  car_rental_price: number;
  car_image: string | null;
  car_quantity: number;
}

export const createCarSchema = z.object({
  car_make: z.string().min(1, "Car make is required"),
  car_model: z.string().min(1, "Car model is required"),
  car_year: z
    .number()
    .min(1886, "Car year must be at least 1886")
    .max(
      new Date().getFullYear() + 1,
      `Car year cannot exceed ${new Date().getFullYear() + 1}`
    ),
  car_rental_price: z.number().min(0, "Rental price cannot be negative"),
  car_image: z.instanceof(File).optional().nullable(),
  car_quantity: z.number().min(0, "Quantity cannot be negative"),
});

export type CreateCarFormValues = z.infer<typeof createCarSchema>;

export interface DecorationModel {
  decoration_id: string;
  decoration_name: string;
  decoration_price: number;
  decoration_description: string;
  decoration_image: string | null;
}
export const createDecorationSchema = z.object({
  decoration_name: z.string().min(1, "Decoration name is required"),
  decoration_price: z.number().min(0, "Price cannot be negative"),
  decoration_description: z
    .string()
    .min(5, "Description must be at least 5 characters long"),
  decoration_image: z.instanceof(File).optional().nullable(),
});

export type CreateDecorationFormValues = z.infer<typeof createDecorationSchema>;

export interface DishModel {
  dish_id: string;
  dish_name: string;
  dish_description: string;
  dish_image: string | null;
  dish_type: "starter" | "main" | "dessert"; // Enum type
  dish_cost_per_serving: number;
  catering_menu_items: CateringMenuItemModel[];
}

export interface CateringMenuItemModel {
  catering_id: string;
  dish_id: string;
}

export const createDishSchema = z.object({
  dish_name: z.string().min(1, "Dish name is required"),
  dish_description: z
    .string()
    .min(5, "Description must be at least 5 characters long"),
  dish_type: z.enum(["starter", "main", "dessert"]),
  dish_cost_per_serving: z
    .number()
    .min(0, "Cost per serving cannot be negative"),
  dish_image: z.instanceof(File).optional().nullable(),
});

export type CreateDishFormValues = z.infer<typeof createDishSchema>;

export interface CateringModel {
  catering_id: string;
  catering_name: string;
  catering_description: string;
  catering_image: string | null;
  catering_menu_items: CateringMenuItemModel[];
  bookings: [];
}

export const createCateringSchema = z.object({
  catering_name: z.string().min(1, "Catering name is required"),
  catering_description: z
    .string()
    .min(5, "Description must be at least 5 characters long"),
  catering_image: z.instanceof(File).optional().nullable(),
});

export type CreateCateringFormValues = z.infer<typeof createCateringSchema>;
