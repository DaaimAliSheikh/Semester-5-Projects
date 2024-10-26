'use client';
import { createTheme, responsiveFontSizes } from '@mui/material/styles';


const theme = responsiveFontSizes( createTheme({
  palette: {
    mode: 'dark',		/// default dark style applied
  },
  typography: {
    fontFamily: 'var(--font-inter)'
}
}))
export default theme


