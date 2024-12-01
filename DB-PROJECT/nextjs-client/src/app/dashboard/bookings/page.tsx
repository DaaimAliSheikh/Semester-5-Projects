"use client";
import * as React from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import Paper from "@mui/material/Paper";
import {
  Chip,
  Fab,
  MenuItem,
  Select,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
  Typography,
} from "@mui/material";
import DeleteForeverIcon from "@mui/icons-material/DeleteForever";

import DoneIcon from "@mui/icons-material/Done";
import CloseIcon from "@mui/icons-material/Close";
import AutorenewIcon from "@mui/icons-material/Autorenew";
import { useQuery, useQueryClient } from "react-query";
import api from "@/services/apiService";
import { AdminBookingModel, CarReservationModel } from "@/types";

const paginationModel = { page: 0, pageSize: 5 };

const updateBooking = async (booking_id: string, status: string) => {
  await api.patch("/bookings/" + booking_id, {
    booking: { booking_status: status },
    payment: {},
  });
};

const deleteBooking = async (booking_id: string) => {
  await api.delete("/bookings/" + booking_id);
};

const fetchBookings = async (): Promise<AdminBookingModel[]> => {
  const { data } = await api.get("/bookings");

  const bookingPromises = data.map(async (booking: any) => {
    const reservationPromises = booking.car_reservations.map(
      async (reservation: CarReservationModel) => {
        const { data } = await api.get(`/cars/${reservation.car_id}`);
        return data;
      }
    );
    const cars = await Promise.all(reservationPromises);

    return {
      ...booking,
      booking_date: new Date(booking.booking_date).toLocaleDateString(),
      booking_event_date: new Date(
        booking.booking_event_date
      ).toLocaleDateString(),
      id: booking.booking_id,
      venue: booking.venue.venue_name,
      user: booking.user.username,
      payment: booking.payment?.payment_id || "",
      catering: booking.catering?.catering_name || "",
      decoration: booking.decoration?.decoration_name || "",
      promo: booking.promo?.promo_name || "",
      cars: cars.map(
        (car) => car.car_make + " " + car.car_model + " " + car.car_year
      ),
    };
  });
  return await Promise.all(bookingPromises);
};

const actions = [
  { icon: <DoneIcon color="success" />, name: "Confirm" },
  { icon: <CloseIcon color="error" />, name: "Decline" },
  { icon: <AutorenewIcon color="warning" />, name: "Set as pending" },
];

export default function Bookings() {
  const [selectedId, setSelectedId] = React.useState<string[]>([]);
  const queryClient = useQueryClient();
  const {
    data: bookings,
    isLoading,
    error,
  } = useQuery(["bookings"], fetchBookings, {
    onError: (error: any) => {
      console.error("Error fetching bookings");
    },
  });

  const handleSelectionChange = (id: any) => {
    setSelectedId(id);
    console.log("Selected ID:", id);
  };
  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 320 },
    { field: "booking_date", headerName: "booking_date", width: 160 },
    {
      field: "booking_event_date",
      headerName: "booking_event_date",
      width: 160,
    },
    {
      field: "booking_guest_count",
      headerName: "guest_count",
      type: "number",
      width: 100,
    },
    {
      field: "booking_status",
      headerName: "booking_status",
      sortable: false,
      width: 160,
      renderCell: (params) => {
        return params.value === "declined" ? (
          <Chip label="Declined" color="error" deleteIcon={<CloseIcon />} />
        ) : params.value === "pending" ? (
          <Chip
            label="Pending"
            color="warning"
            deleteIcon={<AutorenewIcon />}
          />
        ) : (
          <Chip label="Confirmed" color="success" deleteIcon={<DoneIcon />} />
        );
      },
    },
    {
      field: "cars",
      headerName: "Cars",
      width: 120,
      renderCell: (params) => (
        <Select
          value={params?.value?.[0] || ""}
          displayEmpty
          sx={{ width: "100%", mx: 0, fontSize: "0.875rem" }}
        >
          {params.value?.length > 0 ? (
            params.value?.map((role: string, index: number) => (
              <MenuItem key={index} value={role}>
                {role}
              </MenuItem>
            ))
          ) : (
            <MenuItem value="" disabled>
              No Cars
            </MenuItem>
          )}
        </Select>
      ),
    },
    { field: "user", headerName: "user", width: 160 },
    { field: "venue", headerName: "venue", width: 160 },
    { field: "payment", headerName: "payment ID", width: 320 },
    { field: "catering", headerName: "catering", width: 160 },
    { field: "decoration", headerName: "decoration", width: 160 },
    { field: "promo", headerName: "promo", width: 160 },
  ];
  return (
    <Paper sx={{ height: 400, width: "100%" }}>
      <DataGrid
        rows={bookings}
        columns={columns}
        initialState={{ pagination: { paginationModel } }}
        onRowSelectionModelChange={handleSelectionChange}
        pageSizeOptions={[5, 10]}
        checkboxSelection
        disableMultipleRowSelection
        sx={{ border: 0 }}
      />
      {selectedId.length > 0 && (
        <>
          <SpeedDial
            ariaLabel="SpeedDial basic example"
            sx={{
              position: "fixed",
              bottom: 16,
              right: 16,
            }}
            icon={<SpeedDialIcon />}
          >
            {actions.map((action) => (
              <SpeedDialAction
                key={action.name}
                icon={action.icon}
                tooltipTitle={action.name}
                onClick={async () => {
                  await updateBooking(
                    selectedId[0],
                    action.name === "Confirm"
                      ? "confirmed"
                      : action.name == "Decline"
                        ? "declined"
                        : "pending"
                  );
                  queryClient.invalidateQueries(["bookings"]);
                }}
              />
            ))}
          </SpeedDial>
          <Fab
            sx={{
              position: "fixed",
              bottom: 16,
              right: 90,
            }}
            onClick={async () => {
              await deleteBooking(selectedId[0]);
              queryClient.invalidateQueries(["bookings"]);
            }}
            aria-label="delete"
          >
            <DeleteForeverIcon color="error" />
          </Fab>
        </>
      )}
    </Paper>
  );
}
