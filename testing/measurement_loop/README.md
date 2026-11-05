# Measurements Loop

Sends simulated measurments to a local InfluxDB instance and checks if app can read them.

## To Run This

1. Set up and start a local InfluxDB instance.

2. Start the AI-NNC Docker containers.

3. Start the SrsranReader application.

4. Run measurements.py to generate measurements.

5. Check the application output using: docker logs --tail 80 srsran_reader