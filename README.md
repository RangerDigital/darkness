# Darkness
![Build - Production](https://github.com/RangerDigital/darkness/workflows/Build%20-%20Production/badge.svg?branch=master)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Darkness is a simple Flask API used to control NeoPixels strip connected to Raspberry Pi.

>Don't Use! Currently in active development!

## Setup

Darkness is currently run as Docker container, you can try it out with commands below.

This runs a container with minimal setup required (Using PWM0 as a method of control).

```bash
docker run --name darkness --cap-add SYS_RAWIO --device /dev/mem --device /dev/vcio -p 5001:8000 rangerdigital/darkness
```

Or in case It doesn't work:

```bash
docker run --name darkness --privileged -p 5001:8000 rangerdigital/darkness
```

>The privileged flag is seriously insecure, I wouldn't trust me if I were you!

## License
[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
