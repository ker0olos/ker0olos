import os
import re
import signal
import socket
import threading

# keep in mind it might break
# this script is still new and error prone
# and can need manually restarts


class Message:
    def __init__(self, author: str, bits: int, text: str):
        self.text = text
        self.bits = bits
        self.author = author


class Chat:
    def __init__(self, token, channel):
        self.__listeners__ = []

        self.__token__ = token
        self.__channel__ = channel

        self.__client__ = socket.socket()

        self.__thread__ = threading.Thread(target=self.__start__)

    def __start__(self):
        self.__client__.connect(("irc.chat.twitch.tv", 6667))

        self.__client__.send(f"PASS {self.__token__}\n".encode("utf-8"))
        self.__client__.send(f"NICK *\n".encode("utf-8"))

        self.__client__.send(f"CAP REQ :twitch.tv/tags\n".encode("utf-8"))
        self.__client__.send(f"JOIN #{self.__channel__}\n".encode("utf-8"))

        try:
            while True:
                for resp in (
                    self.__client__.recv(1024 * 2).decode("utf-8").split("\r\n")
                ):
                    if resp.startswith("PING"):
                        self.__client__.send("PONG\n".encode("utf-8"))

                    matches = re.findall(
                        f"badges=(.*);*.@(.*).tmi.twitch.tv PRIVMSG #{self.__channel__} :(.*)",
                        resp,
                    )

                    for (badges, username, message) in matches:
                        bits = re.search(r"bits-?.*\/(\d+)", badges)
                        for listener in self.__listeners__:
                            listener(
                                Message(
                                    author=username,
                                    bits=int(bits.group(1)) if bits is not None else 0,
                                    text=message,
                                )
                            )

        except Exception as e:
            raise e

    def start(self):
        self.__thread__.start()

    def stop(self):
        os.kill(os.getpid(), signal.SIGTERM)

    def listen(self, listener):
        self.__listeners__.append(listener)
