import re
import socket
import threading

# keep in mind it might break
# this script is still new and error prone
# and can need manually restarts


class Message:
    def __init__(self, username, message):
        self.text: str = message
        self.author: str = username


class Chat:
    def __init__(self, token, channel):
        self.__listeners__ = []

        self.__token__ = token
        self.__channel__ = channel

        self.__sock__ = socket.socket()

        self.__stopped__ = False
        self.__thread__ = threading.Thread(target=self.__start__)

    def __start__(self):
        self.__sock__.connect(("irc.chat.twitch.tv", 6667))

        self.__sock__.send(f"PASS {self.__token__}\n".encode("utf-8"))
        self.__sock__.send(f"NICK *\n".encode("utf-8"))
        self.__sock__.send(f"JOIN #{self.__channel__}\n".encode("utf-8"))

        try:
            while not self.__stopped__:
                for resp in self.__sock__.recv(1024 * 4).decode("utf-8").split("\r\n"):

                    if self.__stopped__:
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

    def start(self):
        self.__stopped__ = False
        self.__thread__.start()

    def join(self):
        if self.__thread__.is_alive():
            self.__thread__.join()

    def stop(self):
        self.__stopped__ = True
        self.__sock__.close()
        self.join()

    def listen(self, listener):
        self.__listeners__.append(listener)
