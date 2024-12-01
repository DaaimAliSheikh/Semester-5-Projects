"use client";
import { useAuthStore } from "@/stores/authStore";
import { Typography } from "@mui/material";
import React from "react";

const Overview = () => {
  const user = useAuthStore((state) => state.user);

  return (
    <>
      <Typography variant="h6" sx={{ color: "primary.main" }}>
        Welcome to the Dashboard {user?.username}
      </Typography>
      stats
    </>
  );
};

export default Overview;
