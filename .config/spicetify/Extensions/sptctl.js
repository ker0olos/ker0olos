/// <reference path="../globals.d.ts" />

/**
* @type { WebSocket }
*/
let ws;

function init()
{
  let emitter;
  
  ws = new WebSocket("ws://127.0.0.1:8420");

  ws.onopen = () =>
  {
    emitter = setInterval(emit, 100);
  };

  ws.onmessage = receive;

  ws.onclose = () => clearInterval(emitter);
}

function emit()
{
  const artUrl = () =>
  {
    const url = Spicetify.Player.data.track.metadata.image_xlarge_url || '';

    if (url && url.indexOf('localfile') <= -1)
      return `https://i.scdn.co/image/${url.split(':')[2]}`;

    return '';
  };

  const trackUrl = () =>
  {
    const url = Spicetify.Player.data.track.uri;

    return `https://open.spotify.com/track/${url.split(':')[2]}`;
  };

  ws.send(JSON.stringify({
    type: 'info',
    data: {
      state: Spicetify.Player.isPlaying() ? 'playing' : 'paused',
      title: Spicetify.Player.data.track.metadata.title || 'N/A',
      artist: Spicetify.Player.data.track.metadata.artist_name,
      artUrl: artUrl(),
      trackUrl: trackUrl(),
      position: Spicetify.Player.getProgress(),
      duration: Spicetify.Player.getDuration(),
      liked: Spicetify.Player.getHeart() ? 1 : 0,
      repeat: Spicetify.Player.getRepeat(),
      shuffle: Spicetify.Player.getShuffle() ? 1 : 0
    }
  }));
}

function receive(msg)
{
  msg = msg.data;

  if (msg === 'play-pause')
  {
    Spicetify.Player.togglePlay();
  }
  else if (msg === 'next')
  {
    Spicetify.Player.next();
  }
  else if (msg === 'previous')
  {
    Spicetify.Player.back();
  }
  else if (msg === 'like')
  {
    Spicetify.Player.toggleHeart();
  }
  else if (msg === 'repeat')
  {
    Spicetify.Player.toggleRepeat();
  }
  else if (msg === 'shuffle')
  {
    Spicetify.Player.toggleShuffle();
  }
}

init();