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
