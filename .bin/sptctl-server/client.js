#!/usr/bin/node

// the command line interface for sptctl

const WebSocket = require('ws');

const $1 = process.argv[2];

const getInfo = (key) =>
{
  ws = new WebSocket("ws://127.0.0.1:8420");

  ws.onopen = () =>
  {
    ws.send(JSON.stringify({
      type: 'command',
      data: 'info',
    }));
  };

  ws.onmessage = (message) =>
  {
    message = JSON.parse(message.data);

    if (key)
    {
      const keys = key.split(',');

      keys.forEach((k) => console.log(message[k]));
    }
    else
    {
      console.log(message);
    }

     ws.close();
  };
};

const sendCommand = (key) =>
{
  ws = new WebSocket("ws://127.0.0.1:8420");

  ws.onopen = () =>
  {
    ws.send(JSON.stringify({
      type: 'command',
      data: key,
    }));

    ws.close();
  };
};

if (
  $1 === 'play-pause' ||
  $1 === 'next' ||
  $1 === 'previous' ||
  $1 === 'like' ||
  $1 === 'repeat' ||
  $1 === 'shuffle'
)
  sendCommand($1);
else
  getInfo($1);