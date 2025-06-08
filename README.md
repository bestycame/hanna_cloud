# HannaCloud Python Client
## NOT OFFICIALLY SUPPORTED BY HANNA --

A Python client library for interacting with the HannaCloud API.
This client provides methods for authentication and device data retrieval.
Developped solely for the HannaCloud HomeAssistant integration. At least for now.

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
access_token = client.authenticate(email="your-email", password="your-password")
print(f"Access token: {access_token}")

# Get devices
devices = client.get_devices()
print(f"Devices: {devices}")

# Get user info
user_info = client.get_user()
print(f"User info: {user_info}")

# Get last device reading
last_reading = client.get_last_device_reading(device_id)
print(f"Last device reading: {last_reading}")

# Get device log history (example)
log_history = client.get_device_log_history(device_id=device_id)
print(f"Device log history: {log_history}")

# Disable Cl and pH pumps
client.set_remote_hold(device_id=device_id, setting: True)

# Enable Cl and pH pumps
client.set_remote_hold(device_id=device_id, setting: False)
```

### Authentication

The client uses email and password authentication. Use the `authenticate` method to obtain and set the access token for subsequent requests.

### API Methods

- `authenticate(email: str, password: str, key_base64) -> access_token`
- `get_devices()`
- `get_user()`
- `get_last_device_reading(device_id: str)`
- `set_remote_hold(device_id: str, setting: bool)`

## License
This project is licensed under the MIT License - see the LICENSE file for details. 
