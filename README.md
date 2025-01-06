# HITBOT SDK

This repository contains the HITBOT SDK for controlling and monitoring the ZEFG60150 robotic gripper. The SDK provides functionalities to initialize the gripper, set its position, speed, and current, and retrieve its status, position, and current.

## Requirements

- Python 3.x
- `pyserial` library
- `modbus-tk` library

## Installation

Install the required libraries using pip:

```bash
pip install pyserial modbus-tk
```

## Usage

### Importing the SDK

```python
from zefg60150_sdk import ZEFG60150Tool
```

### Creating an Instance

```python
gripper = ZEFG60150Tool()
```

### Searching for Available Serial Ports

```python
ports = gripper.searchCom()
print(ports)
```

### Opening and Closing Serial Connection

```python
# Open connection
result = gripper.serialOperation(com='COM3', baudRate=115200, status=True)
print(result)

# Close connection
result = gripper.serialOperation(com='COM3', status=False)
print(result)
```

### Initializing the Gripper

```python
result = gripper.initialize(salveId=1)
print(result)
```

### Setting Position, Speed, and Current

```python
# Set position to 30mm
result = gripper.setPosition(salveId=1, position=30)
print(result)

# Set speed to 100mm/s
result = gripper.setSpeed(salveId=1, speed=100)
print(result)

# Set current to 0.4A
result = gripper.setCurrent(salveId=1, current=0.4)
print(result)
```

### Retrieving Status, Position, and Current

```python
# Get status
status = gripper.getStatus(salveId=1)
print(status)

# Get current position
position = gripper.getPosition(salveId=1)
print(position)

# Get current
current = gripper.getCurrent(salveId=1)
print(current)
```

### Configuring Parameters

```python
# Change slave ID from 1 to 2
result = gripper.setSalveId(oldId=1, newId=2)
print(result)

# Set baud rate to 115200
result = gripper.setBaudRate(salveId=2, baudrate=4)
print(result)

# Save parameters
result = gripper.saveParams(salveId=2)
print(result)

# Restore default parameters
result = gripper.restoreDefault(salveId=2)
print(result)
```

## License

This project is licensed under the MIT License.
