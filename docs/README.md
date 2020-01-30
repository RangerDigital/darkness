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
  details: It all begins at the command line.
footer: GPL-3.0 Licensed | Copyright © 2020
---

## 🚀 Use Cases
**Typical use cases I needed for myself:**
- **Alert notifications from Grafana,**
  I wanted to have visual feedback about my infrastructure.
- **Automation visual feedback,**
  I wanted to have notifications about the state of my Ansible playbooks.
- **Ambient lighting,**
  because routers with RGB lighting are 🔥.

## 🍬 Features
**The most noticeable feature implemented in Darkness:**
- **Run as a Docker container**, simple to get started.
- **Python API**, lightweight Flask powered API.
- **Animation System,** flexible way to show notifications.
- **Command Line client**, by using darkness.py you can integrate anything.

<img style="display: block; margin-left: auto; margin-right: auto;" class="center" src="terminal.gif" width=750/>

**To install darkness.py CLI client simply run this command below:**
```bash
curl https://darkness.bednarski.dev/install.sh | sudo bash
```

## 🔥 Quick Start
### Prerequisites
**Things you will need to get started:**
- Raspberry Pi
- Docker Engine installed on Raspberry.
- NeoPixels (Ws281x) LEDs connected to (Defaults uses GPIO 18) your Raspberry.

### Setup
**To run the Darkness, create Docker container with this command:**
```bash
docker run --name darkness --cap-add SYS_RAWIO --device /dev/mem --device /dev/vcio -p 5000:8000 rangerdigital/darkness
```
This will run an API server on port **5000** on your Raspberry.

### Usage
**There are multiple ways to interact with the Darkness.**

::: warning Warning!
Darkness is currently in the development stage so the whole documentation is incomplete.
:::

But for now, the easiest way to try it out is to run **GET** requests against **/state** endpoint, with **POST** or **PUT** you can update these values to control still ambient light.
```json
{
"hue":  360,
"saturation":  1,
"status":  true,
"value":  1
}
```
You can also control Darkness with **darkness.py** command-line client! You can find a prototype in darkness-cli directory on GitHub.
