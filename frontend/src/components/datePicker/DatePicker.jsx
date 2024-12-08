import React, { useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

const newTheme = createTheme({
  components: {
    MuiInputBase: {
      styleOverrides: {
        root: {
          color: 'var(--input-color)',
          backgroundColor: 'white',
          padding: '0',
          margin: '0'
        },
        input: {
          padding: '0',
          margin: '0'
        },
      },
    },
    MuiInputAdornment: {
      styleOverrides: {
        root: {
          color: 'black',
        },
      },
    },
    MuiSvgIcon: {
      styleOverrides: {
        root: {
          fill: 'black',
          paddingRight: '10px',
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        input: {
          padding: '0',
          paddingLeft: '5px'
        },
        root: {
          padding: '0',
        },
      },
    },
    MuiFormLabel: {
      styleOverrides: {
        root: {
          color: 'var(--text-color)',
        },
      },
    },
    MuiPickersDay: {
      styleOverrides: {
        root: {
          color: 'var(--text-color)',
        },
        today: {
          color: 'var(--text-color)',
        },
      },
    },
    MuiDayCalendar: {
      styleOverrides: {
        weekDayLabel: {
          color: 'var(--text-color)',
          fontWeight: 'bold',
        },
      },
    },
    MuiDateCalendar: {
      styleOverrides: {
        root: {
          color: 'var(--button-background-color)',
          borderRadius: '5px',
          borderWidth: '2px',
          borderColor: 'var(--button-background-color)',
          border: '1px solid',
          backgroundColor: 'var(--footer-background-color)',
        }
      }
    }
  }
});

function BasicDatePicker({ value, onChange }) {
  return (
    <ThemeProvider theme={newTheme}>
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DatePicker
          value={value} 
          onChange={onChange}
        />
      </LocalizationProvider>
    </ThemeProvider>
  );
}

export default BasicDatePicker;
