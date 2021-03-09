#!/usr/bin/node

// the layer between the Spicetify extension
// and the command line interface

const WebSocket = require('ws');

/**
* @typedef { Object } Info
* @property { 'playing' | 'paused' } state
* @property { string } title
* @property { string } artist
* @property { string } artUrl
* @property { string } trackUrl
* @property { number } position
* @property { number } duration
* @property { 0 | 1 | 2 } repeat
* @property { 0 | 1 } shuffle
*/

/**
* @type { Info }
*/
let info = {};

let spicetify;

const wss = new WebSocket.Server({
  port: 8420
});

wss.on('connection', (ws) =>
{
  ws.on('message', (message) =>
  {
    message = JSON.parse(message);

    // info received from spicetify
    if (message.type === 'info')
    {
      spicetify = ws;

      info = message.data;
    }
    
    if (message.type === 'command' && spicetify)
    {
      // return info to client
      if (message.data === 'info')
      {
        ws.send(JSON.stringify(info));
      }
      // pass a command to spicetify
      else
      {
        spicetify.send(message.data);
      }
    }
  });
});