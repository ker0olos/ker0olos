#!/usr/bin/node

const fs = require('fs');

const path = process.argv[2];

const [ timestamp, summary, title ] = process.argv[3].split('\\n');

const content = fs.readFileSync(path, { encoding: 'utf-8' }).split('\n');

console.log(content);

const target = content.findIndex((s, i) =>
{
  if (s === timestamp && content[i + 3] === summary && content[i + 4] === title)
    return true;
});

if (target <= -1)
  return;

content.splice(target, 6);

fs.writeFileSync(path, content.join('\n'));