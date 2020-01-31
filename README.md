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

**Darkness** is a simple dockerized **Flask API** used to control **NeoPixels** strips connected to **Raspberry Pi**.

> 📚 For more information go to [Darkness](https://darkness.bednarski.dev/) official site!

## 🍬 Features
The most noticeable feature currently implemented in Darkness:
- **Run as a Docker container**, simple to get started.
- **Python API**, lightweight Flask powered API.
- **Animation System,** flexible way to show notifications.
- **Command Line client**, by using Darkness CLI you can integrate anything.

## 🔥 Setup

**Darkness** is run as a Docker container, you can try it out with commands below.

This runs a container with minimal setup required:

```bash
docker run --name darkness --cap-add SYS_RAWIO --device /dev/mem --device /dev/vcio -p 5000:8000 rangerdigital/darkness
```

>🔨 You can specify LED count `-e LED_COUNT=16`, (Default: 16) and GPIO port `-e LED_GPIO=18`, Default: 18).

Or in case It doesn't work:

```bash
docker run --name darkness --privileged -p 5000:8000 rangerdigital/darkness
```

>🔪 The privileged flag is seriously **insecure**, I wouldn't trust me if I were you!

## 🎉 Usage

You can use **Darkness CLI** client control Darkness running on your Raspberry Pi by installing it with the command below:
```bash
curl https://darkness.bednarski.dev/install.sh | sudo bash
```
<p align="center">
	<img src="docs\.vuepress\public\terminal.gif" alt="Darkness CLI Terminal" width=750/>
</p>

Currently supports **only Linux** distributions, or If you want to have full control use **Darkness API** to its fullest:

The easiest way to start is to run **GET** requests against `/state` endpoint,
with **POST** or **PUT** you can update these values to control still ambient light.
```json
{
"hue":  360,
"saturation":  1,
"status":  true,
"value":  1
}
```
If you want to see the rainbow animation just **POST** or **PUT** to `/animations/rainbow`.
```json
{
"msg":  "Rainbow animation completed!"
}
```
You can specify duration of the animation with **URL parameters**,
 for example: `/animations/rainbow?duration=10` with play rainbow animation for 10 seconds.

>💡 For full API documentation go to [Darkness](https://darkness.bednarski.dev/) official site!

## 🚧 Contributing

**You are more than welcome to help me build the Darkness!**

Just fork this project from the `master` branch and submit a Pull Request (PR) to the `dev` branch.
If you are modifying the Darkness server you should also run `pytest` functional tests inside `/darkness/tests` directory.

## 📃 License
This project is licensed under [GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/) .
