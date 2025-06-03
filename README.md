# HannaCloud Python Client
-- NOT OFFICIALLY SUPPORTED BY HANNA --
A Python client library for interacting with the HannaCloud API. This client provides methods for authentication and device data retrieval.
Developped for the HannaCloud HomeAssistant integration.

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
last_reading = client.GetLastDeviceReading(device_id)
print(f"Last device reading: {last_reading}")

# Get device log history (example)
from datetime import datetime
log_history = client.getDeviceLogHistory(device_id=device_id)
print(f"Device log history: {log_history}")
```

### Authentication

The client uses email and password authentication. Use the `authenticate` method to obtain and set the access token for subsequent requests.

### API Methods

- `authenticate(email: str, password: str) -> (access_token, refresh_token)`
- `GetDevices()`
- `getUser()`
- `GetLastDeviceReading(device_id: str)`
- `getDeviceLogHistory(device_id: str)`

## License
This project is licensed under the MIT License - see the LICENSE file for details. 
