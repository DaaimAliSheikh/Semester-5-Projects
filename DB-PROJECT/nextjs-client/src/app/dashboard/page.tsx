"use client";
import React, { useState } from "react";
import {
  AppBar,
  Box,
  Drawer,
  IconButton,
  Toolbar,
  Typography,
  Avatar,
  useTheme,
  useMediaQuery,
  MenuItem,
  Tooltip,
  Menu,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import DrawerContent from "@/components/DrawerContent";
import PersonIcon from "@mui/icons-material/Person";
import { pink } from "@mui/material/colors";

const drawerWidth = 240;

const Dashboard = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(
    null
  );
  const settings = ["Profile", "Account", "Dashboard", "Logout"];

  const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <Box sx={{ display: "flex" }}>
      {/* Navbar */}
      <AppBar
        position="fixed"
        sx={{ zIndex: theme.zIndex.drawer + 1, bgcolor: "background.paper" }}
      >
        <Toolbar>
          {isMobile && (
            <IconButton color="inherit" onClick={handleDrawerToggle}>
              <MenuIcon />
            </IconButton>
          )}
          <Typography
            variant="h6"
            color="primary"
            sx={{ flexGrow: 1, display: "flex", alignItems: "center" }}
          >
            <Box component="span" sx={{ fontWeight: "bold" }}>
              LOGO
            </Box>
          </Typography>

          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <Avatar alt="Remy Sharp" sx={{ bgcolor: "primary" }}>
                  <PersonIcon />
                </Avatar>
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: "45px" }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
              {settings.map((setting) => (
                <MenuItem key={setting} onClick={handleCloseUserMenu}>
                  <Typography sx={{ textAlign: "center" }}>
                    {setting}
                  </Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Drawer */}
      <Drawer
        variant={isMobile ? "temporary" : "persistent"}
        open={!isMobile || mobileOpen}
        onClose={handleDrawerToggle}
        sx={{
          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: drawerWidth,
            py: 10,
          },
        }}
      >
        <DrawerContent setMobileOpen={setMobileOpen} />
      </Drawer>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          ml: isMobile ? 0 : `${drawerWidth}px`,
          bgcolor: theme.palette.background.default,
          minHeight: "100vh",
        }}
      >
        <Toolbar />
        <Typography variant="h4" sx={{ color: theme.palette.primary.main }}>
          Welcome to the Dashboard
        </Typography>
        <Typography
          variant="body1"
          sx={{ mt: 2, color: theme.palette.secondary.main }}
        >
          This is where your content will go.
        </Typography>
      </Box>
    </Box>
  );
};

export default Dashboard;
