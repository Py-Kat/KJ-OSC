from pythonosc import udp_client
import win32com.client
import keyboard
from threading import Event
from time import sleep
from colorama import Style, Fore
from random import choice

# Print Rainbow          #
def rainbow_print(text: str) -> None:
    """Prints text in a random color!"""

    # Colors
    (
        blue,
        red,
        green,
        magenta,
        yellow,
        cyan,
        dim,
        bright,
        normal
     ) = (
        Fore.BLUE,
        Fore.RED,
        Fore.GREEN,
        Fore.MAGENTA,
        Fore.YELLOW,
        Fore.CYAN,
        Style.DIM,
        Style.BRIGHT,
        Style.NORMAL
    )

    # Choose Color
    random_color = choice([
        red,
        blue,
        green,
        yellow,
        magenta,
        cyan
    ])

    # Choose Style
    random_style = choice([
        bright,
        dim,
        normal
    ])

    print(random_color + random_style + text)

# Format Time          #
def format_time(seconds: float) -> str:
    """Format seconds as M:SS!"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

# iTunes Info          #
itunes = win32com.client.Dispatch(
    "Itunes.Application"
)

# Client          #
client = udp_client.SimpleUDPClient(
    "127.0.0.1",
    9000
)

stop = Event()

key = input(
    "\n\n| Please choose the KEYBOARD KEY you would like to temporarily bind as the 'quit' key!"
    +Fore.YELLOW+
    "\n\n| To avoid possible errors, please only use a letter key for now! ( Ex. 'q' will be SHIFT+Q )"
    "\n| The first character in this input is what will be used! ( Ex. 'qwerty' will still be SHIFT+Q! )"
    +Style.RESET_ALL+
    "\n\n| > "
)

bound_key = key[:1:]

print(
    Fore.RED+
    f"\n\n| Use SHIFT+{bound_key.upper()} to quit the script while running!"
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

# Main Loop          #
last_status = None
try:
    while not stop.is_set():

        if stop.is_set():
            break

        # Prevent crash if no song is in the player          #
        try:
            state = itunes.PlayerState
            track = itunes.CurrentTrack
        except Exception:
            state = 0
            track = None

        if track is not None:
            try:
                position = itunes.PlayerPosition
            except Exception:
                position = 0
            duration = getattr(
                track,
                "Duration",
                0
            )

            # Music Playing          #
            if state == 1:
                status = (
                    f"♫ | {track.Name}"
                    f"\n👤 | {track.Artist}"
                    f"\n《 {format_time(position)}"
                    f" / {format_time(duration)} 》"
                )

            # Music Paused          #
            elif state == 0 and position > 0:
                status = "| Paused."

        # No Music in the Player          #
            else:
                status = "| Nothing Playing."

        else:
            status = "| Nothing Playing."

        # Send Status to OSC          #
        if status != last_status:
            client.send_message(
                "/chatbox/input",
                [
                    status,
                    True, False
                ]
            )
            rainbow_print(
                f"\n\n| Sent To OSC:"
                f"\n\n{status}"
            )
            last_status = status

        sleep(2) # Status Update Delay          #
finally:
    keyboard.remove_all_hotkeys()