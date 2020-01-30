<p align="center">
  <br /><img
    width="600"
    src="logo.png"
    alt="Darkness – NeoPixels Controller"
  />
</p>

***

![Build - Documentation](https://github.com/RangerDigital/darkness/workflows/Build%20-%20Documentation/badge.svg?branch=master)
![Build - Dev](https://github.com/RangerDigital/darkness/workflows/Build%20-%20Dev/badge.svg?branch=dev)
![Build - Production](https://github.com/RangerDigital/darkness/workflows/Build%20-%20Production/badge.svg?branch=master)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Darkness** is a simple **Flask API** used to control **NeoPixels** strip connected to **Raspberry Pi**.

## Setup

**Darkness** is currently run as Docker container, you can try it out with commands below.

This runs a container with minimal setup required.

```bash
docker run --name darkness --cap-add SYS_RAWIO --device /dev/mem --device /dev/vcio -p 5001:8000 rangerdigital/darkness
```

You can also specify LED count (**-e LED_COUNT=16**, Default: 16) and GPIO port (**-e LED_GPIO=18**, Default: 18).

Or in case It doesn't work:

```bash
docker run --name darkness --privileged -p 5001:8000 rangerdigital/darkness
```

>The privileged flag is seriously **insecure**, I wouldn't trust me if I were you!

## Usage

**Darkness** is currently in the **development stage** so the whole documentation is incomplete.

For now, the easiest way to try it out is to run **GET** requests against **/state** endpoint,
with **POST** or **PUT** you can update these values to control still ambient light.

```json
{
"hue":  360,
"saturation":  1,
"status":  true,
"value":  1
}
```
You can also control Darkness with **darkness.py** command-line client! You can find a prototype in darkness-cli directory.

## Testing

You can run basic py.test **functional tests** inside the **/tests** directory.
You can specify URL of the running app inside py.test fixture.

## License
[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
