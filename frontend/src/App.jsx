import { useEffect, useState } from 'react';
import axios from 'axios';
import {
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Container
} from '@mui/material';

const App = () => {
    const [latestSensorData, setLatestSensorData] = useState([]);
    const [lastUpdated, setLastUpdated] = useState(null);

    useEffect(() => {
        const fetchLatestData = () => {
            axios.get('http://localhost:5000/latest_data')
                .then(response => {
                    if (response.data && Object.keys(response.data).length > 0) {
                        setLatestSensorData(response.data);
                        setLastUpdated(new Date().toLocaleTimeString());
                    }
                })
                .catch(error => {
                    console.error('Error fetching the data: ', error);
                });
        };

        fetchLatestData()

        const fetchInterval = setInterval(fetchLatestData, 100);

        return () => clearInterval(fetchInterval);
    }, []);

    return (
        <Container>
            <Typography variant="h4" component="h1" sx={{ textAlign: 'center', margin: '20px 0' }}>
                Latest Sensor Data
            </Typography>
            {lastUpdated && (
                <Typography variant="subtitle1" gutterBottom>
                    Last Updated: {lastUpdated}
                </Typography>
            )}
            {Object.keys(latestSensorData).length === 0 ? (
                <Typography variant="h6" component="p" sx={{ textAlign: 'center' }}>
                    No data available
                </Typography>
            ) : (
                <TableContainer component={Paper} sx={{ maxWidth: '100%', margin: 'auto' }}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>Sensor Name</TableCell>
                                <TableCell>Attribute</TableCell>
                                <TableCell>Value</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {Object.entries(latestSensorData).map(([sensorName, attributes]) => (
                                Object.entries(attributes).map(([attrKey, attrValue]) => (
                                    <TableRow key={`${sensorName}-${attrKey}`}>
                                        <TableCell component="th" scope="row">
                                            {sensorName}
                                        </TableCell>
                                        <TableCell>{attrKey}</TableCell>
                                        <TableCell>{attrValue.toString()}</TableCell>
                                    </TableRow>
                                ))
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}
        </Container>
    );
};

export default App;