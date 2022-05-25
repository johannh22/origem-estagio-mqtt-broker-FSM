# Origem: Web Development Intern Challenge - Bonus

This repository contains the code for the **Origem's web development intern challenge**. The usage instructions and so on are below.

This project was developed using Python 3.9 and in MacOS Monterrey (12.3.1). There should be no problem using another Python version and/or a different OS.

The base version can be found at [Github](https://github.com/johannh22/origem-estagio-mqtt-broker). This implements the Finite State Machine.

## Usage Instructions

To connect to the broker, please fill your info in the [env_codes.py](./env_codes.py) file. The script at [mqtt_client.py](./mqtt_client.py) handles the rest.

Requirements for the code are located in [requirements.txt](./requirements.txt). To install them, use the following:

```bash
pip install -r requirements.txt
```

Then, to run the script, simply use `python3 main.py`.
