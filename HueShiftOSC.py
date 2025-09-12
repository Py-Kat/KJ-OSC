from pythonosc import udp_client
from colorama import Style, Fore
from random import uniform
from time import sleep
import keyboard
from threading import Event

client = udp_client.SimpleUDPClient(
    "127.0.0.1",
    9000
)

parameter = None
delay = 0
breaking = None

stop = Event()
keyboard.add_hotkey(
    "shift+q",
    lambda: stop.set(),
    suppress=True
)

while True:

    if breaking:
        break

    parameter = input(
        "\n\n| Enter the name of your avatar's hue shift parameter."
        +Fore.RED+
        "\n\n| Parameter name MUST be exact!"
        +Fore.YELLOW+
        "\n| Exact parameter name can be found following this path:"
        "\n| AppData > LocalLow > VRChat > VRChat > OSC > usr_(id) > Avatars"
        +Fore.RED+
        "\n| NOTE: THE 'OSC' FOLDER WILL NOT EXIST IF OSC IS DISABLED IN-GAME!"
        +Style.RESET_ALL+
        "\n\n| > "
    )

    if parameter.strip() == "":
        print(
            Fore.RED+
            "\n\n| You can't enter nothing!"
            +Style.RESET_ALL
        )
        sleep(2)
        continue
    break

while True:

    if breaking:
        break

    try:
        delay = float(input(
            "\n\n| Enter the delay of which the hue will shift."
            +Fore.YELLOW+
            "\n\n| Or input '0' for random delays!"
            +Style.RESET_ALL+
            "\n\n| > "
        ))

        if delay < 0:
            print(
                Fore.RED+
                "\n\n| You can't use a negative delay!"
                +Style.RESET_ALL
            )
            sleep(2)
            continue

        input(
            Fore.RED+
            "\n\n| Use SHIFT+Q to quit the script at any point!"
            +Style.RESET_ALL+
            "\n\n| PRESS ENTER TO BEGIN! > "
        )

        if delay == 0:
            try:
                while not stop.is_set():
                    while True:
                        if stop.is_set():
                            breaking = True
                            break

                        delay = uniform(0.1, 1.5)
                        number = uniform(0, 1)
                        client.send_message(
                            f"/avatar/parameters/{parameter}",
                            number
                        )
                        print(
                            f"\n\n| Value Sent: {number:.2f}"
                            +Fore.YELLOW+
                            f"\n| Delay: {delay:.2f} Seconds"
                            +Style.RESET_ALL
                        )
                        sleep(delay)

            finally:
                keyboard.remove_all_hotkeys()

        else:
            try:
                while not stop.is_set():
                    while True:
                        if stop.is_set():
                            breaking = True
                            break

                        number = uniform(0, 1)
                        client.send_message(
                            f"/avatar/parameters/{parameter}",
                            number
                        )
                        print(
                            f"\n\n| Value Sent: {number:.2f}"
                        )
                        sleep(delay)

            finally:
                keyboard.remove_all_hotkeys()

    except ValueError:
        print(
            Fore.RED+
            "\n\n| That's not a number!"
            +Style.RESET_ALL
        )
        sleep(2)
        continue