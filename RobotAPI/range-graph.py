# Code to generate tables of distances

from sr.robot import *
import time
import os

PICTURES = 10
BUTTON_GPIO_PIN = 4
STATIC_PATH = "/root/shepherd/shepherd/static/"
CSV_PATH = STATIC_PATH + "csv/"

R = Robot()

R.gpio.pin_mode(BUTTON_GPIO_PIN, INPUT_PULLUP)


def wait_for_button():
    red = False
    while R.gpio.digital_read(BUTTON_GPIO_PIN):
        time.sleep(0.5)
        red = not red
        if red:
            R.motors[0].led.colour = (255, 0, 0)
        else:
            R.motors[0].led.colour = (255, 255, 0)
    R.motors[0].led.colour = (0, 255, 0)


def get_distances(res, dist):
    distances = {"MISS": 0}

    print "Getting distances for " + str(dist) + "cm at " + str(res[0]) + "x" + str(res[1]) + "..."

    R.see(res=res, save=True)
    print "Waiting 10s..."
    time.sleep(10)
    for i in range(PICTURES):
        markers = R.see(res=res, save=False)
        if len(markers) == 0:
            distances["MISS"] += 1
        else:
            marker = markers[0]
            distance = marker.dist
            distance = int(distance * 100)
            if str(distance) in distances:
                distances[str(distance)] += 1
            else:
                distances[str(distance)] = 1

        print str(int(float(i) / float(PICTURES) * 100)) + "% (" + str(i) + "/" + str(PICTURES) + ")"

    return distances


def print_distances_to_console(distances, res, dist):
    print "Results for " + str(dist) + "cm at " + str(res[0]) + "x" + str(res[1]) + ":"
    for k in sorted(distances.iterkeys()):
        print str(k) + ',' + str(distances[k])


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_distances_to_csv(distances, res, dist):
    file_name = "high-" + str(dist) + "cm-" + str(res[0]) + "x" + str(res[1]) + ".csv"
    url = "http://robot.sr/static/csv/" + file_name
    file_path = CSV_PATH + file_name
    ensure_dir(file_path)
    f = open(file_path, "w")

    f.write("Distance,Frequency\r\n")

    for k in sorted(distances.iterkeys()):
        f.write(str(k) + ',' + str(distances[k]) + "\r\n")

    f.close()

    print "Wrote results to " + url


RESOLUTIONS = [
    (640, 480),
    (1296, 736),
    (1296, 976),
    (1920, 1088),
    (1920, 1440)
]

offset = 3

for dist_index in range(6 - offset):
    d = (dist_index + 1 + offset) * 5
    print "Waiting for button press for " + str(d) + "cm..."
    wait_for_button()

    for r in RESOLUTIONS:
        these_distances = get_distances(r, d)
        print_distances_to_console(these_distances, r, d)
        write_distances_to_csv(these_distances, r, d)



