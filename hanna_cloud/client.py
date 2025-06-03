import base64
import random
import requests
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime
import logging


class HannaCloudClient:
    """Client for interacting with the HannaCloud API."""

    def __init__(self):
        """
        Initialize the HannaCloud API client.
        """
        self.base_url = "https://www.hannacloud.com/api"
        self.key_base64 = "MzJmODBmMDU0ZTAyNDFjYWM0YTVhOGQxY2ZlZTkwMDM="
        self.headers = {'Accept': '*/*',
                        'content-type': 'application/json'}
        logging.basicConfig(level=logging.INFO)

    def _make_request(self, method, endpoint, **kwargs):
        """
        Internal method to make HTTP requests to the HannaCloud API.
        Args:
            method (str): HTTP method (e.g., 'POST').
            endpoint (str): API endpoint.
            **kwargs: Additional arguments for requests.request.
        Returns:
            dict: The 'data' field from the API response, or an empty dict if not present.
        Raises:
            requests.HTTPError: If the HTTP request fails.
        """
        headers = {**self.headers, **kwargs.get('headers', {})}
        url = f'{self.base_url}/{endpoint}'
        response = requests.request(method=method,
                                    url=url,
                                    headers=headers,
                                    **kwargs)
        logging.info(f"{method} {url} {response.status_code}")
        response.raise_for_status()
        return response.json().get('data', {})

    def hanna_encrypt(self, plaintext: str) -> str:
        """
        Encrypts the given plaintext using AES CBC mode with a random IV and a base64-encoded key.
        Args:
            plaintext (str): The text to encrypt.
        Returns:
            str: The IV (as a string) and the encrypted data (as hex), separated by a colon.
        """
        # Decode the base64-encoded key to bytes
        key = base64.b64decode(self.key_base64)
        iv = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16)).encode()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = pad(plaintext.encode(), AES.block_size)
        encrypted = cipher.encrypt(padded)
        return f"{iv.decode()}:{encrypted.hex()}"

    def authenticate(self, email: str, password: str) -> tuple[str, str]:
        """
        Authenticates the user with the given email and password.
        Args:
            email (str): The user's email address.
            password (str): The user's password.
        Returns:
            Tuple[str, str]: The access token and refresh token.
        Raises:
            ValueError: If authentication fails or tokens are missing.
        """
        json_data = {
            'operationName': 'Login',
            'variables': {
                'email': self.hanna_encrypt(email),
                'password': self.hanna_encrypt(password),
                'userLanguage': 'English',
                'source': 'web',
            },
            'query': (
                """
                query Login($email: String!, $password: String!, $userLanguage: String!, $source: String) {
                  login(
                    email: $email
                    password: $password
                    language: $userLanguage
                    source: $source
                  ) {
                    token
                    tokenType
                    __typename
                  }
                }
                """
            ),
        }

        response = self._make_request('POST', 'auth', json=json_data)
        if 'login' not in response:
            logging.error(
                "'login' key missing in authentication response: %s",
                response
            )
            raise ValueError(
                "Authentication failed: 'login' key missing in response."
            )
        access_token = None
        refresh_token = None
        for token in response['login']:
            if token.get('tokenType') == 'accessToken':
                self.headers['authorization'] = (
                    f"Bearer {token.get('token', '')}"
                )
                access_token = token.get('token')
            elif token.get('tokenType') == 'refreshToken':
                refresh_token = token.get('token')
        if not access_token or not refresh_token:
            logging.error(
                "Tokens missing in authentication response: %s",
                response
            )
            raise ValueError(
                "Authentication failed: tokens missing in response."
            )
        self.access_token = access_token
        self.refresh_token = refresh_token
        return self.access_token, self.refresh_token

    def GetDashboardFirmwareDetails(self):
        """
        Retrieves firmware details for the dashboard devices.
        Returns:
            dict: Firmware details for the specified devices.
        """
        json_data = {
            'operationName': 'GetDashboardFirmwareDetails',
            'variables': {
                'deviceList': [
                    {
                        'DID': 'BL132_7A67F4',
                        'DM': 'BL132',
                        'mainBoard': '1.02',
                        'ethernetBoard': '1.09'
                    }
                ]
            },
            'query': (
                """
                query GetDashboardFirmwareDetails($deviceList: [JSONObject]) {
                  getDashboardFirmwareDetails(deviceList: $deviceList) {
                    deviceFirmware
                    __typename
                  }
                }
                """
            )
        }
        return self._make_request('POST', 'graphql', json=json_data)

    def GetLastDeviceReading(self):
        """
        Retrieves the last reading for the specified device(s).
        Returns:
            dict: Last device readings.
        """
        json_data = {
            'operationName': 'GetLastDeviceReading',
            'variables': {'deviceIds': ['BL132_7A67F4']},
            'query': (
                'query GetLastDeviceReading($deviceIds: [String!]) {'
                '\n  lastDeviceReadings(deviceIds: $deviceIds) {'
                '\n    DID\n    DT\n    messages\n    __typename\n  }\n}'
            )
        }
        response = self._make_request('POST', 'graphql', json=json_data)
        return response

    def GetDevices(self):
        """
        Retrieves a list of devices for the user.
        Returns:
            dict: Device information.
        """
        json_data = {
            "operationName": "Devices",
            "variables": {
                "modelGroups": [
                    "BL12x", "BL13x", "HALO", "photoMeter", "multiParameter", "BL13xs"
                ],
                "deviceLogs": True
            },
            "query": (
                """
                query Devices($modelGroups: [String!], $deviceLogs: Boolean!) {
                  devices(modelGroups: $modelGroups, deviceLogs: $deviceLogs) {
                    _id
                    DID
                    DM
                    modelGroup
                    DT
                    DINFO {
                      deviceName
                      deviceVersion
                      userId
                      emailId
                      assignedUsers {
                        emailId
                        __typename
                      }
                      tankId
                      tankName
                      __typename
                    }
                    parentId
                    childDevices {
                      DID
                      __typename
                    }
                    dashboardViewStatus
                    deviceOrder
                    secondaryUser
                    reportedSettings
                    status
                    lastUpdated
                    message
                    deviceName
                    batteryStatus
                    __typename
                  }
                }
                """
            )
        }
        return self._make_request('POST', 'graphql', json=json_data)

    def getUser(self):
        """
        Retrieves information about the current user.
        Returns:
            dict: User information.
        """
        json_data = {
            "operationName": "getUser",
            "variables": {},
            "query": (
                """
                query getUser {
                  currentUser {
                    _id
                    fName
                    lName
                    regDate
                    emailId
                    notificationSetting
                    aesObjectId
                    lang
                    tempUnit
                    timeFormat
                    dateFormat
                    dashboardView
                    blDeviceSorting
                    __typename
                  }
                }
                """
            )
        }
        return self._make_request('POST', 'graphql', json=json_data)

    def getDeviceLogHistory(self, device_id: str, from_date: datetime, to_date: datetime):
        """
        Retrieves the device log history for a given device and date range.
        Args:
            device_id (str): The device ID.
            from_date (datetime): Start date for log history.
            to_date (datetime): End date for log history.
        Returns:
            dict: Device log history data.
        """
        json_data = {
            "operationName": "deviceLogHistory",
            "variables": {
                "deviceId": device_id,
                "from": from_date.isoformat(),
                "to": to_date.isoformat(),
                "count": 10000
            },
            "query": (
                """
                query deviceLogHistory($deviceId: String!, $from: String!, $to: String!) {
                  deviceLogHistory(deviceId: $deviceId, from: $from, to: $to) {
                    data
                    endDate
                    startDate
                    parameterNames
                    __typename
                  }
                }
                """
            )
        }
        return self._make_request('POST', 'graphql', json=json_data)
