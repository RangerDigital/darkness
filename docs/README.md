---
home: true
heroImage: https://github.com/RangerDigital/darkness/raw/master/logo.png
actionText: Get Started
actionLink: /guide/
features:
- title: Simplicity First
  details: The simplest setup with maximum flexibility.
- title: Docker Powered
  details: Enjoy the Darkness with simple Docker command.
- title: Command-line Client
  details: It all begins at the command-line.
footer: GPL-3.0 Licensed | Copyright © Jakub Bednarski 2020
---

<p align="center">
  <b>Darkness</b> is a simple dockerized <b>API</b> used to control <b>NeoPixels</b> strips connected to <b>Raspberry Pi</b>.
</p>

<br>

## 🚀 Use Cases
My typical use cases for The Darkness:

- **Alert notifications from Grafana,**
  I wanted to have visual feedback about my infrastructure.
- **Automation visual feedback,**
  I wanted to have notifications about the state of my Ansible playbooks.
- **Ambient lighting,**
  because routers with RGB lighting are 🔥.

<br>

## 🍬 Features
The most noticeable features currently implemented in Darkness:

- **Run as a Docker container,** simple to get started.
- **Python API,** lightweight Flask powered API.
- **Animation System,** flexible way to show notifications.
- **Command-line Client,** by using Darkness CLI you can integrate anything.

<br>

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

<br>


## 🎉 Usage
You can use **Darkness CLI** client control Darkness running on your Raspberry Pi by installing it with the command below:
```bash
curl https://darkness.bednarski.dev/install.sh | sudo bash
```

<p align="center">
  <img src="terminal.gif" alt="Darkness CLI Terminal" width=750/>
</p>

Currently supports **only Linux** distributions, or If you want to have full control use **Darkness API**.

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
for example: `/animations/rainbow?duration=10` will play rainbow animation for 10 seconds.

<br>

## 📃 License
This project is licensed under [GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/) .
