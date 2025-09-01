# Imports          #
from pythonosc import udp_client
import win32com.client
from time import sleep
from colorama import Style, Fore
from random import choice

# Colors Constants
blue = Fore.BLUE
red = Fore.RED
green = Fore.GREEN
magenta = Fore.MAGENTA
yellow = Fore.YELLOW
cyan = Fore.CYAN
dim = Style.DIM
bright = Style.BRIGHT
normal = Style.NORMAL

# Format Time          #
def format_time(seconds: float) -> str:
    """Format seconds as M:SS"""
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

# Main Loop          #
last_status = None
while True:

    # Randomize Console Print Colors          #
    random_color = choice([
        red,
        blue,
        green,
        yellow,
        magenta,
        cyan
    ])
    random_style = choice([
        bright,
        dim,
        normal
    ])

    # Don't crash if no music is in the player          #
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
        print(
            random_color+
            random_style+
            f"\n\n| Sent To OSC:"
            f"\n\n{status}"
        )
        last_status = status

    sleep(2) # Status Update Delay          #