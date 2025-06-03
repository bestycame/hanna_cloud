# HannaCloud Python Client

A Python client library for interacting with the HannaCloud API. This client provides methods for authentication and device data retrieval.

## Installation

You can install the package using pip:

```bash
pip install hanna-cloud
```

## Usage

Here's a basic example of how to use the client:

```python
from hanna_cloud import HannaCloudClient

# Initialize the client
client = HannaCloudClient()

# Authenticate with your email and password
access_token, refresh_token = client.authenticate(email="your-email", password="your-password")
print(f"Access token: {access_token}")

# Get devices
devices = client.GetDevices()
print(f"Devices: {devices}")

# Get user info
user_info = client.getUser()
print(f"User info: {user_info}")

# Get last device reading
last_reading = client.GetLastDeviceReading()
print(f"Last device reading: {last_reading}")

# Get dashboard firmware details
firmware_details = client.GetDashboardFirmwareDetails()
print(f"Firmware details: {firmware_details}")

# Get device log history (example)
from datetime import datetime
log_history = client.getDeviceLogHistory(
    device_id="BL132_7A67F4",
    from_date=datetime(2025, 6, 3, 0, 0, 0),
    to_date=datetime(2025, 6, 3, 23, 59, 59)
)
print(f"Device log history: {log_history}")
```

### Authentication

The client uses email and password authentication. Use the `authenticate` method to obtain and set the access token for subsequent requests.

### API Methods

- `authenticate(email: str, password: str) -> (access_token, refresh_token)`
- `GetDevices()`
- `getUser()`
- `GetLastDeviceReading()`
- `GetDashboardFirmwareDetails()`
- `getDeviceLogHistory(device_id: str, from_date: datetime, to_date: datetime)`

## Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
