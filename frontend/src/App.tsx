import React, { useEffect, useState, useCallback } from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme, Typography, Box, Button } from '@mui/material';
import DataTable from './components/DataTable';
import { getDevices, getProtocols, getResults, getUsers, getAndStoreToken } from './services/api';
import { Device, TestProtocol, TestResult, User } from './types';

const theme = createTheme();

function App() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [protocols, setProtocols] = useState<TestProtocol[]>([]);
  const [results, setResults] = useState<TestResult[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Get token on initial load
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        await getAndStoreToken();
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Error getting token:', error);
        setError('Failed to authenticate. Please try again later.');
      }
    };

    initializeAuth();
  }, []);

  const fetchData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const [devicesData, protocolsData, resultsData, usersData] = await Promise.all([
        getDevices(),
        getProtocols(),
        getResults(),
        getUsers(),
      ]);

      // Safely set data with fallback to empty arrays
      setDevices(devicesData?.results || []);
      setProtocols(protocolsData?.results || []);
      setResults(resultsData?.results || []);
      setUsers(usersData?.results || []);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to load data. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const deviceColumns = [
    { id: 'name', label: 'Name', minWidth: 170 },
    { id: 'device_type', label: 'Type', minWidth: 100 },
    { id: 'model_number', label: 'Model Number', minWidth: 100 },
    { id: 'manufacturer', label: 'Manufacturer', minWidth: 100 },
    { id: 'assigned_to_name', label: 'Assigned To', minWidth: 100 },
  ];

  const protocolColumns = [
    { id: 'name', label: 'Name', minWidth: 170 },
    { id: 'version', label: 'Version', minWidth: 100 },
    { id: 'status', label: 'Status', minWidth: 100 },
    { id: 'created_by_name', label: 'Created By', minWidth: 100 },
  ];

  const resultColumns = [
    { id: 'device_name', label: 'Device', minWidth: 170 },
    { id: 'protocol_name', label: 'Protocol', minWidth: 170 },
    { id: 'status', label: 'Status', minWidth: 100 },
    { id: 'performed_by_name', label: 'Performed By', minWidth: 100 },
    { id: 'start_time', label: 'Start Time', minWidth: 170 },
    { id: 'end_time', label: 'End Time', minWidth: 170 },
  ];

  const userColumns = [
    { id: 'username', label: 'Username', minWidth: 170 },
    { id: 'email', label: 'Email', minWidth: 170 },
    { id: 'is_staff', label: 'Is Staff', minWidth: 100 },
    { id: 'is_active', label: 'Is Active', minWidth: 100 },
  ];

  if (!isAuthenticated) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Typography variant="h6" color="error" align="center">
            {error || 'Authenticating...'}
          </Typography>
        </Container>
      </ThemeProvider>
    );
  }

  if (isLoading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Typography variant="h6" align="center">
            Loading data...
          </Typography>
        </Container>
      </ThemeProvider>
    );
  }

  // Safely check if any data exists
  const hasData = Boolean(
    (devices && devices.length > 0) ||
    (protocols && protocols.length > 0) ||
    (results && results.length > 0) ||
    (users && users.length > 0)
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <h1> Vital Bio Mock Frontend </h1>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ textAlign: 'right', mb: 2 }}>
          <Button 
            variant="contained" 
            onClick={fetchData}
            disabled={isLoading}
          >
            Load Data
          </Button>
        </Box>
        {error && (
          <Typography variant="h6" color="error" align="center" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}
        {devices && devices.length > 0 && <DataTable title="Devices" columns={deviceColumns} data={devices} />}
        {protocols && protocols.length > 0 && <DataTable title="Test Protocols" columns={protocolColumns} data={protocols} />}
        {results && results.length > 0 && <DataTable title="Test Results" columns={resultColumns} data={results} />}
        {users && users.length > 0 && <DataTable title="Users" columns={userColumns} data={users} />}
        {!hasData && !isLoading && (
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            <Typography variant="h6" color="text.secondary">
              Click "Load Data" to fetch data
            </Typography>
          </Box>
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
