from pythonosc import udp_client
import win32com.client
from time import sleep

def format_time(seconds: float) -> str:
    """Format seconds as M:SS"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

itunes = win32com.client.Dispatch(
    "Itunes.Application"
)

client = udp_client.SimpleUDPClient(
    "127.0.0.1",
    9000
)

last_status = ""

while True:
    state = itunes.PlayerState
    position = itunes.PlayerPosition

    if state == 1:
        track = itunes.CurrentTrack
        duration = track.Duration
        status = (f"| {track.Name} - {track.Artist}"
                  f"\n《 {format_time(position)} "
                  f"/ {format_time(duration)} 》")

    elif state == 0:
        if position > 0:
            track = itunes.CurrentTrack
            status = "Paused."
        else:
            status = "Nothing Playing."

    else:
        status = "Nothing Playing."

    if status != last_status:
        client.send_message(
            "/chatbox/input",
            [
                status,
                True, False
            ]
        )
        print(
            f"\n\nSent To OSC:   {status}"
        )
        last_status = status
    sleep(2)

# todo FIX CRASH WHEN NOTHING IS IN THE PLAYER!