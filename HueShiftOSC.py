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

while True:

    if breaking:
        break

    parameter = input(
        "\n\n| Enter the name of your avatar's hue shift parameter."
        +Fore.YELLOW+
        "\n\n| Exact parameter name can be found following this path:"
        "\n| AppData > LocalLow > VRChat > VRChat > OSC > usr_(id) > Avatars"
        +Fore.RED+
        "\n\n| Parameter name MUST be exact!"
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
            "\n\n| This is in seconds! ( Ex. '1' will be 1 second between loops! )"
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

        key = input(
            "\n\n| Please choose the KEYBOARD KEY you would like to temporarily bind as the 'quit' key!"
            + Fore.YELLOW +
            "\n\n| To avoid possible errors, please only use a letter key for now! ( Ex. 'q' will be SHIFT+Q )"
            "\n| The first character in this input is what will be used! ( Ex. 'qwerty' will still be SHIFT+Q! )"
            + Style.RESET_ALL +
            "\n\n| > "
        )

        bound_key = key[:1:]

        print(
            Fore.RED+
            f"\n\n| Use SHIFT+{bound_key.upper()} to quit the script at any point!"
            +Style.RESET_ALL+
            "\n\n| Press SPACEBAR to begin! ( Ex. 'q' )\n"
        )
        keyboard.wait(
            "space",
            suppress=True
        )

        keyboard.add_hotkey(
            f"shift+{bound_key}",
            lambda: stop.set(),
            suppress=True
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