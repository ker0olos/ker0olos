import re
import socket
import threading

# keep in mind it might break
# this script is still new and error prone
# and can need manually restarts

# it was made to match shughes-uk/python-youtubechat APIs
# to allow seamless transitions for multi-streams


class TwitchMessage:
    def __init__(self, username, message):
        self.username: str = username
        self.content: str = message


class TwitchChat:
    def __init__(self, token, channel):
        self.__listeners__ = []

        self.__token__ = token
        self.__channel__ = channel

        self.__sock__ = socket.socket()

        self.__stop__ = threading.Event()
        self.__thread__ = threading.Thread(target=self.__start__)

        self.is_closed = False

    def __start__(self):
        self.__sock__.connect(("irc.chat.twitch.tv", 6667))

        self.__sock__.send(f"PASS {self.__token__}\n".encode("utf-8"))
        self.__sock__.send(f"NICK *\n".encode("utf-8"))
        self.__sock__.send(f"JOIN #{self.__channel__}\n".encode("utf-8"))

        try:
            while not self.__stop__.is_set():
                for resp in self.__sock__.recv(1024 * 4).decode("utf-8").split("\r\n"):

                    if self.__stop__.is_set():
                        break

                    if resp.startswith("PING"):
                        self.__sock__.send("PONG\n".encode("utf-8"))

                    matches = re.findall(
                        f"@(.*).tmi.twitch.tv PRIVMSG #{self.__channel__} :(.*)", resp
                    )

                    for (username, message) in matches:
                        for listener in self.__listeners__:
                            listener(TwitchMessage(username, message))

        except Exception as e:
            raise e

        finally:
            self.is_closed = True

    def start(self):
        self.__thread__.start()

    def stop(self):
        self.__sock__.close()
        self.__stop__.set()

    def subscribe_chat_message(self, listener):
        self.__listeners__.append(listener)
