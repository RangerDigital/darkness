#!/usr/bin/env python3
import click
import requests
import spectra


@click.group()
def main():
    pass


@main.command()
@click.argument("colour")
@click.option('--server', default="http://127.0.0.1:5000", help="Address of Darkness container.")
def set(server, colour):
    x = spectra.html(colour).to("hsv").values
    result = requests.post(
        server + "/state", json={"hue": x[0], "saturation": x[1], "value": x[2]})
    print("Code:", result.status_code)


@main.command()
@click.argument("red")
@click.argument("green")
@click.argument("blue")
@click.option('--server', default="http://127.0.0.1:5000", help="Address of Darkness container.")
def rgb(server, red, green, blue):
    x = spectra.rgb(int(red) / 255, int(green) / 255, int(blue) / 255).to("hsv").values
    print(x)
    result = requests.post(
        server + "/state", json={"hue": x[0], "saturation": x[1], "value": x[2]})
    print("Code:", result.status_code)


@main.command()
@click.argument("hue")
@click.argument("saturation")
@click.argument("value")
@click.option('--server', default="http://127.0.0.1:5000", help="Address of Darkness container.")
def hsv(server, hue, saturation, value):
    x = spectra.hsv(int(hue), int(saturation), int(value)).to("hsv").values
    print(x)
    result = requests.post(
        server + "/state", json={"hue": x[0], "saturation": x[1], "value": x[2]})
    print("Code:", result.status_code)


@main.command()
@click.option('--server', default="http://127.0.0.1:5000", help="Address of Darkness container.")
def get(server):
    result = requests.get(server + "/state")
    state = result.json()

    if state["status"]:
        click.echo("Status: " + click.style("ON", fg="green"))
    else:
        click.echo("Status: " + click.style("OFF", fg="red"))

    print("Hue: {} | Saturation: {} | Value: {}".format(
        round(state["hue"], 0), round(state["saturation"], 2), round(state["value"], 2)))


@main.command()
@click.option('--server', default="http://127.0.0.1:5000", help="Address of Darkness container.")
def toggle(server):
    state = requests.get(server + "/state")
    status = state.json()["status"]

    result = requests.post(
        server + "/state", json={"status": not status})
    print("Code:", result.status_code)


if __name__ == '__main__':
    main()
