# Imports          #
from pythonosc import udp_client
from wonderwords import RandomWord
import requests
from bs4 import BeautifulSoup
from time import sleep


# Client          #
client = udp_client.SimpleUDPClient(
    "127.0.0.1",
    9000
)


# Send Random Dictionary.com Stuff          #
loops = 0
while True:
    try:
        loops += 1

        r = RandomWord()
        search_term = r.word()

        response = requests.get(
            f"https://www.dictionary.com/browse/{search_term}",
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )
        message = soup.find(
            "li",
            class_="TOpzjFHcRBqzUMLLKa9s"
        )


        print(
            f"\n\nLoop Number: {loops}"
            f"\n\n{search_term}"
            f"\n{response.url}"
        )
        client.send_message(
            "/chatbox/input",
            [
                f"{search_term}: {message.text[0:144:1]}",
                True
            ]
        )
        sleep(10)
    except ValueError:
        print(
            "\n\nNone! Skipping..."
        )
        continue