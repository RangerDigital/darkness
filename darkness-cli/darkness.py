#!/usr/bin/env python3
try:
    import click
    import requests
    import spectra
except ImportError:
    print("Import Error!")
    print("Make sure you have installed all the requirements.")
    exit()


@click.group()
def main():
    pass


@main.command(help="Sets leds color using HEX and color names.")
@click.argument("colour", metavar="<Colour Name>")
@click.option("--server", default="http://127.0.0.1:5000", envvar="DARKNESS_SERVER", help="Address of running Darkness container.")
def set(server, colour):
    try:
        hsv = spectra.html(colour).to("hsv").values
    except:
        click.secho("Conversion Error!", blink=True, fg="red")
        click.echo("This color couldn't be converted to HSV.")
        return

    result = requests.post(
        server + "/state", json={"hue": hsv[0], "saturation": hsv[1], "value": hsv[2]})

    if result.status_code == 200:
        click.secho("Success!", fg="green")
        click.echo("Changed color to {}. Status Code: {}".format(
            colour, result.status_code))
    else:
        click.secho("Requests Error!", blink=True, fg="red")
        click.echo("Status Code: {}".format(result.status_code))


@main.command(help="Sets leds color using RGB values.")
@click.argument("rgb", metavar="<RGB 0-255>", nargs=3)
@click.option("--server", default="http://127.0.0.1:5000", envvar="DARKNESS_SERVER", help="Address of running Darkness container.")
def rgb(server, rgb):
    hsv = spectra.rgb(int(rgb[0]) / 255, int(rgb[1]) / 255,
                      int(rgb[2]) / 255).to("hsv").values

    result = requests.post(
        server + "/state", json={"hue": hsv[0], "saturation": hsv[1], "value": hsv[2]})

    if result.status_code == 200:
        click.secho("Success!", fg="green")
        click.echo("Changed color to RGB: {}. Status Code: {}".format(
            rgb, result.status_code))
    else:
        click.secho("Requests Error!", blink=True, fg="red")
        click.echo("Status Code: {}".format(result.status_code))


@main.command(help="Sets leds color using HSV values.")
@click.argument("hsv", metavar="<HSV 0-360 or 0-1>", nargs=3)
@click.option("--server", default="http://127.0.0.1:5000", envvar="DARKNESS_SERVER", help="Address of running Darkness container.")
def hsv(server, hsv):
    hsv = spectra.hsv(int(hsv[0]), int(hsv[1]), int(hsv[2])).to("hsv").values

    result = requests.post(
        server + "/state", json={"hue": hsv[0], "saturation": hsv[1], "value": hsv[2]})

    if result.status_code == 200:
        click.secho("Success!", fg="green")
        click.echo("Changed color to HSV: {}. Status Code: {}".format(
            hsv, result.status_code))
    else:
        click.secho("Requests Error!", blink=True, fg="red")
        click.echo("Status Code: {}".format(result.status_code))


@main.command(help="Gets current state of leds.")
@click.option("--server", default="http://127.0.0.1:5000", envvar="DARKNESS_SERVER", help="Address of running Darkness container.")
def get(server):
    result = requests.get(server + "/state")

    if result.status_code != 200:
        click.secho("Requests Error!", blink=True, fg="red")
        click.echo("Status Code: {}".format(result.status_code))
        return

    state = result.json()

    if state["status"]:
        click.echo("Status: " + click.style("ON", fg="green"))
    else:
        click.echo("Status: " + click.style("OFF", fg="red"))

    click.echo("Hue: {} | Saturation: {} | Value: {}".format(
        round(state["hue"], 0), round(state["saturation"], 2), round(state["value"], 2)))


@main.command(help="Toggles leds On and Off.")
@click.option("--server", default="http://127.0.0.1:5000", envvar="DARKNESS_SERVER", help="Address of running Darkness container.")
def toggle(server):
    result = requests.get(server + "/state")

    if result.status_code != 200:
        click.secho("Requests Error!", blink=True, fg="red")
        click.echo("Status Code: {}".format(result.status_code))
        return

    status = result.json()["status"]

    result = requests.post(server + "/state", json={"status": not status})

    if result.status_code == 200:
        click.secho("Success!", fg="green")
        click.echo("Changed status to: {}. Status Code: {}".format(
            not status, result.status_code))
    else:
        click.secho("Requests Error!", blink=True, fg="red")
        click.echo("Status Code: {}".format(result.status_code))


@main.command(help="Runs specified animation.")
@click.argument("name", metavar="<Animation Name>")
@click.option("--server", default="http://127.0.0.1:5000", envvar="DARKNESS_SERVER", help="Address of running Darkness container.")
@click.option("--hue", default=0, help="Hue value used by some animation.")
@click.option("--count", default=1, help="Repeat count used by some animation.")
@click.option("--duration", default=1, help="Duration time used by some animation.")
def animation(server, name, hue, count, duration):
    result = requests.post(server + "/animations/" + name,
                           params={"duration": duration, "hue": hue, "count": count})

    if result.status_code == 200:
        click.secho("Success!", fg="green")
        click.echo("Animation with name {} just run. Status Code: {}".format(
            name, result.status_code))
    else:
        click.secho("Requests Error!", blink=True, fg="red")
        click.echo("Status Code: {}".format(result.status_code))


if __name__ == '__main__':
    main()
