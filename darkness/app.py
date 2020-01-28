#!/usr/bin/env python3
import time
from flask import Flask, jsonify, request
from leds import StripController

app = Flask(__name__)
strip = StripController()


@app.route("/state", methods=["GET"])
def get_state():
    hue, saturation, value = strip.hsv

    response = {"hue": hue, "saturation": saturation,
                "value": value, "status": strip.status}
    return jsonify(response)


@app.route("/state", methods=["PUT", "POST"])
def update_state():
    payload = request.json or {}

    # Get current state dictionary. Updates changed values.
    state = {"hue": strip.hsv[0], "saturation": strip.hsv[1],
             "value": strip.hsv[2], "status": strip.status}
    state.update(payload)

    # Validate payload, No Pydantic because of old Python :C
    # TODO: Find a better way to validate inputs, maybe upgrade Python?
    if not isinstance(state["hue"], int) or state["hue"] > 360 or state["hue"] < 0:
        return jsonify({"error": "Hue must be a value between 0 and 360!"}), 400

    if not (isinstance(state["saturation"], int) or isinstance(state["saturation"], float)) or state["saturation"] > 1 or state["saturation"] < 0:
        return jsonify({"error": "Saturation must be a value between 0 and 1!"}), 400

    if not (isinstance(state["value"], int) or isinstance(state["value"], float)) or state["value"] > 1 or state["value"] < 0:
        return jsonify({"error": "Value must be a value between 0 and 1!"}), 400

    if type(state["status"]) != type(True):
        return jsonify({"error": "Status must be a boolean value!"}), 400

    # Update strip with new state.
    strip.status = state["status"]
    strip.set_color([state["hue"], state["saturation"], state["value"]])

    return jsonify(state)

# TODO: Refactor all validation and structure for animations!

# Rainbow animation.
@app.route("/animations/rainbow", methods=["PUT", "POST"])
def show_rainbow():
    duration = float(request.args.get("duration") or 1)

    if strip.event_running:
        return jsonify({"error": "Animation is currently running!"}), 400

    if duration == 0 or duration > 60:
        return jsonify({"error": "You don't want to do that!"}), 400

    if duration <= 0 or duration > 60:
        return jsonify({"error": "Duration must be a value between 0 and 60!"}), 400

    strip.event_running = True

    state_hsv = strip.hsv
    state_status = strip.status

    for hue in range(0, 360):
        time.sleep(duration / 360)
        strip.set_color([hue, 1, 1], save_state=False)

    # Restore state before animation.
    strip.status = state_status
    strip.set_color(state_hsv)

    strip.event_running = False

    return jsonify({"msg": "Rainbow animation completed!"})


# Rainbow animation.
@app.route("/animations/blink", methods=["PUT", "POST"])
def show_blink():
    count = int(request.args.get("count") or 1)
    hue = int(request.args.get("hue") or 360)

    if strip.event_running:
        return jsonify({"error": "Animation is currently running!"}), 400

    if hue > 360 or hue < 0:
        return jsonify({"error": "Hue must be a value between 0 and 360!"}), 400

    if count == 0 or count > 60:
        return jsonify({"error": "Count must be a value between 0 and 60!"}), 400

    strip.event_running = True

    state_hsv = strip.hsv
    state_status = strip.status

    for i in range(count):

        for value in range(10, 0, -1):
            time.sleep(0.01)
            strip.set_color([hue, 1, 1 / value], save_state=False)

        time.sleep(0.3)

        for value in range(1, 10):
            time.sleep(0.01)
            strip.set_color([hue, 1, 1 / value], save_state=False)

        strip.set_color([0, 0, 0], save_state=False)
        time.sleep(0.3)

    # Restore state before animation.
    strip.status = state_status
    strip.set_color(state_hsv)

    strip.event_running = False

    return jsonify({"msg": "Blink animation completed!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
