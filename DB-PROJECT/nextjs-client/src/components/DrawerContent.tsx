"use client";

import React from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  Box,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
} from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import PersonIcon from "@mui/icons-material/Person";
import SettingsIcon from "@mui/icons-material/Settings";
import LogoutIcon from "@mui/icons-material/Logout";

const DrawerContent = ({
  setMobileOpen,
}: {
  setMobileOpen: React.Dispatch<React.SetStateAction<boolean>>;
}) => {
  const pathname = usePathname(); // Get the current path
  const router = useRouter();

  // Menu items with corresponding routes
  const menuItems = [
    { text: "Dashboard", icon: <DashboardIcon />, path: "/dashboard" },
    { text: "Profile", icon: <PersonIcon />, path: "/dashboard/profile" },
    { text: "Settings", icon: <SettingsIcon />, path: "/dashboard/settings" },
    { text: "Logout", icon: <LogoutIcon />, path: "/logout" },
  ];
  const handleListItemClick = () => {
    setMobileOpen(false);
    router.push(pathname);
  };

  return (
    <Box sx={{ width: "100%", bgcolor: "background.paper", height: "100%" }}>
      <List component="nav" aria-label="main menu">
        {menuItems.map((item) => (
          <ListItemButton
            key={item.text}
            component={Link}
            href={item.path} // Use Next.js `Link` for navigation
            selected={pathname === item.path} // Highlight if the current path matches
            onClick={handleListItemClick}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItemButton>
        ))}
      </List>
      <Divider />
    </Box>
  );
};

export default DrawerContent;
