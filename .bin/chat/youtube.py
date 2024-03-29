#!/usr/bin/python

import os
import json
import time

import google_auth_oauthlib.flow
import googleapiclient.discovery
from munch import munchify

from . import Message
from .twitch import Chat as Interface

# keep in mind it might break
# this script is still new and error prone
# and can need manually restarts

api_version = "v3"

# how to get client_secret.json
# https://stackoverflow.com/a/55416898/10336604
client_secret_file = "client_secret.json"

# run the script directly to generate it
# requires a functional client_secret.json
credentials_file = "yt_credentials.json"


class Chat(Interface):
    def __init__(self, channel):
        super().__init__(channel)

        with open(credentials_file, "r") as file:
            self.__client__ = googleapiclient.discovery.build(
                "youtube",
                api_version,
                credentials=google_auth_oauthlib.flow.google.oauth2.credentials.Credentials(
                    token=json.load(file)["token"]
                ),
            )

    def __start__(self):
        # search for live streams in channel
        response = munchify(
            self.__client__.search()
            .list(
                part="snippet",
                channelId=self.__channel__,
                eventType="live",
                maxResults=25,
                order="viewCount",
                type="video",
            )
            .execute()
        )

        if len(response["items"]) < 1:
            raise Exception("No live events for this channel")

        videoId = response["items"][0].id.videoId

        # get live chat id from the video id
        response = munchify(
            self.__client__.videos()
            .list(
                part="liveStreamingDetails",
                id=videoId,
            )
            .execute()
        )

        liveChatId = response["items"][0].liveStreamingDetails.activeLiveChatId

        nextPageToken = None

        while True:
            request = self.__client__.liveChatMessages().list(
                part="id,snippet,authorDetails",
                pageToken=nextPageToken,
                liveChatId=liveChatId,
            )

            response = munchify(request.execute())

            # skip first pull
            if nextPageToken is not None:
                for event in response["items"]:
                    if (
                        event.snippet.type == "superChatEvent"
                        and "userComment" in event.snippet.superChatDetails
                    ):
                        message = Message(
                            # 100 bits is $1.00
                            # 1000000 micros is $1.00
                            # 1000000 / 10000 === 100 === $1.00
                            bits=event.snippet.superChatDetails.amountMicros / 10000,
                            author=event.authorDetails.displayName,
                            text=event.snippet.superChatDetails.userComment,
                        )

                    elif event.snippet.type == "textMessageEvent":
                        message = Message(
                            bits=0,
                            author=event.authorDetails.displayName,
                            text=event.snippet.textMessageDetails.messageText,
                        )

                    if message:
                        for listener in self.__listeners__:
                            listener(message)

                    # sleep the interval / the amount of messages
                    # to avoid sending the entire list of message
                    # as a batch
                    time.sleep(
                        (response.pollingIntervalMillis / 1000) / len(response["items"])
                    )

            # sleep the entire interval at once
            if (nextPageToken is None) or (len(response["items"]) == 0):
                time.sleep(response.pollingIntervalMillis / 1000)

            nextPageToken = response.nextPageToken


if __name__ == "__main__":
    # disable https verification when running locally
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    scopes = [
        "https://www.googleapis.com/auth/youtube",
        "https://www.googleapis.com/auth/youtube.force-ssl",
    ]

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secret_file, scopes=scopes
    )

    credentials = flow.run_local_server()

    # write credentials to yt_credentials.json
    with open(credentials_file, "w") as file:
        file.write(credentials.to_json())
