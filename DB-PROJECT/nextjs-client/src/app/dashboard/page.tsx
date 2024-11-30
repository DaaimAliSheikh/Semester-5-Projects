"use client";
import { useAuthStore } from "@/stores/authStore";
import { Typography } from "@mui/material";
import React from "react";
import Grid from "@mui/material/Grid2";

const Overview = () => {
  const user = useAuthStore((state) => state.user);

  return (
    <>
      <Typography variant="h5" sx={{ color: "primary.main" }}>
        Welcome to the Dashboard {user?.username}
      </Typography>
      <Grid
        container
        spacing={{ xs: 2, md: 3 }}
        columns={{ xs: 4, sm: 8, md: 12 }}
      >
        {Array.from(Array(6)).map((_, index) => (
          <Grid key={index} size={{ xs: 2, sm: 4, md: 4 }}>
            hey
          </Grid>
        ))}
      </Grid>
    </>
  );
};

export default Overview;
