# Heat Pump Control API

This project provides a FastAPI-based API to control a Tuya-based or Smart Life heat pump. It allows users to turn the device on/off, adjust temperatures, change modes, and retrieve status information. The API is designed to be easily integrated with automation systems like Homey, homeassistant or ifttt.

You can deploy this easily to a server or Raspberry Pi using Docker. The API communicates with the heat pump using the Tuya API and local key, so no cloud connection is required after the initial setup.

## Features

- **Turn On/Off**: Control the power state of the heat pump.
- **Adjust Temperatures**: Set water, cold, heat, and auto temperatures.
- **Change Modes**: Switch between different operating modes (e.g., heat, cold, auto).
- **Retrieve Status**: Get current status including temperatures and mode.

## Prerequisites

- **Python 3.7+**: Ensure Python is installed on your system.
- **Docker & Docker Compose**: Required for containerized deployment.
- **jq**: A command-line JSON processor used in setup scripts.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/paalr/heatpump-control-api.git
   cd heatpump-control-api
   ```
2. **Create a Tuya Developer Account**

   - Go to the [Tuya IoT Platform](https://iot.tuya.com/) and create an account.
   - Create a new project and add a new "Cloud Development" application.
   - Note down the `Access ID` and `Access Secret` from the application.

3. Run the setup script to configure the environment:

   ```bash
   ./setup.sh
   ```
   This script will:
    - Check for Python and jq installation.
    - Create a virtual environment and install dependencies.
    - Set up environment variables for the Tuya API.

4. **Configure the Environment Variables**

   - Open the `.env` file and verify that the following variables are set:
     ```text
     DEVICE_ID=your_device_id
     IP_ADDRESS=your_device_ip
     LOCAL_KEY=your_local_key
     VERSION=3.4 # Tuya API version
     ```

   - Ensure these values match the configuration of your Tuya device.

5. **Build and Run with Docker**

   ```bash
   docker-compose up -d
   ```
   This will build the Docker image and start the FastAPI server on port 8000.

    **Usage**
    Once the server is running, you can access the API at `http://localhost:8000/docs` to view the Swagger documentation and test the endpoints.

## API Endpoints
example of the API endpoints
- **GET /status**: Get the current status of the heat pump.
- **GET /mode**: Get the current mode of the heat pump.
- **GET /temperature**: Get the current temperatures from the heat pump.
- **POST /turn_on**: Turn on the heat pump.
- **POST /turn_off**: Turn off the heat pump.
- **POST /set_water_temperture/{temperature}**: Set the water temperature.
- **POST /set_mode/{mode}**: Set the operating mode.



| Endpoint                      | Method | Parameter          | Allowed Values / Description                                                                 |
|-------------------------------|--------|--------------------|----------------------------------------------------------------------------------------------|
| `/turn_on`                    | POST   | N/A                | No parameters required; turns the heat pump on.                                              |
| `/turn_off`                   | POST   | N/A                | No parameters required; turns the heat pump off.                                             |
| `/temperature`                | GET    | N/A                | Returns current and water tank temperatures.                                                 |
| `/set_water_temperature/{temperature}` | POST   | `temperature`      | Integer between -100000 and 100000; sets the water temperature.                              |
| `/set_cold_temperature/{temperature}`  | POST   | `temperature`      | Integer between -100000 and 100000; sets the cold temperature.                               |
| `/set_heat_temperature/{temperature}`  | POST   | `temperature`      | Integer between -100000 and 100000; sets the heat temperature.                               |
| `/set_auto_temperature/{temperature}`  | POST   | `temperature`      | Integer between -100000 and 100000; sets the auto temperature.                               |
| `/mode`                       | GET    | N/A                | Returns the current mode of the heat pump.                                                   |
| `/set_mode/{mode}`            | POST   | `mode`             | `"water"`, `"cold"`, `"heat"`, `"auto"`, `"wac"`, `"wah"`, `"waa"`; sets the operating mode. |
| `/status`                     | GET    | N/A                | Returns full status including all [DPS values](#DPS-Parameters-Documentation).                |
| `/error`                      | GET    | N/A                | Returns error code if any errors are reported by the device.                                 |

# DPS Parameters Documentation

| DPS ID | Function Point     | Type     | Range / Description                                                                 | Units   | Comment                                  |
|--------|--------------------|----------|-------------------------------------------------------------------------------------|---------|------------------------------------------|
| 1      | switch             | boolean  | `{true, false}`                                                                     | N/A     | Data Transfer Type: Send & report        |
| 2      | mode               | enum     | `"water"`, `"cold"`, `"heat"`, `"auto"`, `"wac"`, `"wah"`, `"waa"`                  | N/A     | Data Transfer Type: Send & report        |
| 5      | work_mode          | enum     | `"none"`, `"power"`, `"smart"`, `"silent"`                                          | N/A     | Data Transfer Type: Send & report        |
| 16     | temp_current       | int      | Inlet temperature in Celsius                                                        | Celsius | Data Transfer Type: Report only          |
| 17     | work_state         | enum     | `heat`, `water`, `cold`                                                             | N/A     | Data Transfer Type: Report only    |
| 25     | temp_effluent      | int      | Water tank temperature in Celsius                                                   | Celsius | Data Transfer Type: Report only          |
| 101    | water_settemp      | int      | Set temperature for water                                                           | Celsius | Data Transfer Type: Send & report        |
| 102    | cold_settemp       | int      | Cooling set temperature in Celsius                                                  | Celsius | Data Transfer Type: Send & report        |
| 103    | heat_settemp       | int      | Heating set temperature in Celsius                                                  | Celsius | Data Transfer Type: Send & report        |
| 104    | auto_settemp       | int      | Auto set temperature in Celsius                                                     | Celsius | Data Transfer Type: Send & report        |
| 111    | water_settempup    | int      | Upper limit for water set temperature                                               | Celsius | Data Transfer Type: Report only          |
| 112    | water_settemplow   | int      | Lower limit for water set temperature                                               | Celsius | Data Transfer Type: Report only          |
| 113    | cold_settempup     | int      | Upper limit for cold set temperature                                                | Celsius | Data Transfer Type: Report only          |
| 114    | cold_settemplow    | int      | Lower limit for cold set temperature                                                | Celsius | Data Transfer Type: Report only          |
| 115    | heat_settempup     | int      | Upper limit for heat set temperature                                                | Celsius | Data Transfer Type: Report only          |
| 116    | heat_settemplow    | int      | Lower limit for heat set temperature                                                | Celsius | Data Transfer Type: Report only          |
| 117    | auto_settempup     | int      | Upper limit for auto set temperature                                                | Celsius | Data Transfer Type: Report only          |
| 118    | auto_settemplow    | int      | Lower limit for auto set temperature                                                | Celsius | Data Transfer Type: Report only          |
| 121    | error_code         | string   | Error code                                                                          | N/A     | Data Transfer Type: Report only          |
| 122    | tempsign           | boolean  | `{true, false}`                                                                     | N/A     | Data Transfer Type: Send & report        |
| 123    | type               | enum     | ?                                                                                   | N/A     | Data Transfer Type: Report only          |
| 124    | lang_sign          | enum     | `{"range": ["zh", "en"]}`                                                           | N/A     | Data Transfer Type: Send & report        |

## Notes
When setting temperatures, the range is limited by the `up` and `low` values. If the set temperature is outside this range, the heat pump will not accept the command.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request if you have any improvements or suggestions.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/) for providing an excellent framework for building APIs.
- [TinyTuya](https://github.com/jasonacox/tinytuya) for enabling interaction with Tuya devices.