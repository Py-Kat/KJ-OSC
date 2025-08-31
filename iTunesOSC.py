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

last_status = None

while True:
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

        if state == 1:
            status = (
                f"♫ | {track.Name}"
                f"\n👤 | {track.Artist}"
                f"\n《 {format_time(position)} "
                f"/ {format_time(duration)} 》"
            )

        elif state == 0 and position > 0:
            status = "| Paused."

        else:
            status = "| Nothing Playing."

    else:
        status = "| Nothing Playing."


    if status != last_status:
        client.send_message(
            "/chatbox/input",
            [
                status,
                True, False
            ]
        )
        print(
            f"\n\n| Sent To OSC:   {status}"
        )
        last_status = status

    sleep(2)