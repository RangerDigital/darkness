---
sidebar: auto
---
# Guide

## 📑 Introduction
I wanted to build **Darkness** for controlling **NeoPixels** ring under my **Raspberry Pi 3B+** router. Because It sits on my desk I could use It as a **visual notification system**.

**Darkness** consists of **Docker** container running **Python API** server and optional **command-line client** that you can use to easily integrate with your other automation systems.

::: tip 💡 Tip!
The whole thing was built to be as easy as possible to deploy and use so don't expect all the bells and whistles... yet!
:::

<br>

## 🔥 Installation
Installation of Darkness is a **simple process**, provided you have all the necessary **prerequisites**.

### Prerequisites
For the **hardware** side of things:

- Raspberry Pi 2/3/3B/3B+
- NeoPixels (WS281X LEDs) strip or ring connected to your Raspberry's GPIO 18 pin.

::: tip 💡 Tip!
Darkness uses a Python port of [rpi_ws281x](https://github.com/jgarff/rpi_ws281x) library! Check it out for more advanced stuff.
:::

And finally for the **software** requirements:
- `docker` engine running on your Raspberry. If you need help with that check out [Docker Docs](https://docs.docker.com/get-started/)!
- `curl` for installing CLI client or interacting with API.

<br>

### Darkness Controller
**Darkness** is run as a **Docker** container, you can deploy it out with commands below.

This runs a container with **minimal permissions** required:

```bash
docker run --name darkness --cap-add SYS_RAWIO --device /dev/mem --device /dev/vcio -p 5000:8000 rangerdigital/darkness
```

Or in case It doesn't work:

```bash
docker run --name darkness --privileged -p 5000:8000 rangerdigital/darkness
```

::: danger 🛡 Danger!
The privileged flag is seriously **insecure**, I wouldn't trust me if I were you!
:::

You can use `-e` flag to **configure** Darkness. Available environment variables:

 - `LED_COUNT` *(Default: 16)* - **Number of LEDs** connected to Raspberry.
 - `LED_PIN` *(Default: 18)* - **GPIO Pin** that you connected LEDs to Raspberry.

<br>

### Darkness CLI
If you are running **Linux** *(Tested on Ubuntu, Debian, Manjaro)* you can use dedicated **Darkness CLI** client. Install by simply running this command below:

```bash
curl https://darkness.bednarski.dev/install.sh | sudo bash
```

::: danger 🛡 Danger!
This will run install.sh with root privileges.
:::

If you don't trust piping directly into the bash then save and check this script yourself or install manually with darkness.py from the project's repository.

<br>

## 🎉 Usage
If you are using **Darkness CLI** client you should specify **URL** to your controller with:

- Using `--server http://127.0.0.1:5000` command option.
- Using `DARKNESS_URL` environment variable that will save this setting.

*(This **defaults** to `localhost`)*

You can change LEDs color with **HTML Color** name, **HEX** code, **HSV** or **RGB** values.

- For example, this command **sets LEDs color** to purple:

```bash
darkness set purple
```

- If you want to **disable LEDs** *(Also disables showing animations!)* use:

```bash
darkness toggle
```

- To **see all available commands** use:

```bash
darkness --help

Usage: darkness [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  animation  Runs specified animation.
  get        Gets current state of leds.
  hsv        Sets leds color using HSV values.
  rgb        Sets leds color using RGB values.
  set        Sets leds color using HEX and color names.
  toggle     Toggles leds On and Off.
```

<br>

If you prefer to use **API** there are currently two endpoints you can interact with:

- `/state` - Sets the current state of LEDs, you can toggle them and set color with HSV values.

```bash
curl -X PUT -d '{"hue": 360}' http://127.0.0.1:5000/state
```

Use **GET** method to check the state, If you want to update the state use **POST** or **PUT** method with **JSON** payload shown below.

```bash
{
"hue":  360,
"saturation":  1,
"status":  true,
"value":  1
}
```

- `/animations/{Name of Animation}` - You can **POST** or **PUT** to this endpoint to initiate one of two currently available animations. For example:

```bash
curl -X POST http://127.0.0.1:5000/animations/blink?count=5&hue=360
```
This will blink five times with red hue.

<br>

**Currently available animation:**
- `rainbow` - Shows 🌈 animation!

  *Parameters:*
  - `?duration=10` - Number of seconds animation will run.

- `blink` - Blinks LEDs with the selected color.

  *Parameters:*
  - `?count=0` - Number of times It will blink
  - `?hue=360` - Hue of LEDs blinking.

<br>

## 🚧 Contributing

**You are more than welcome to help me build the Darkness!**

Just fork this project from the `master` branch and submit a Pull Request (PR) to the `dev` branch.

If you are modifying the Darkness server you should also run `pytest` functional tests inside `/darkness/tests` directory.

<br>

## 📃 License
This project is licensed under [GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/) .
