const {readFileSync} = require("fs");
const { html } = require("htm/preact");

function PlayerBox({ player }) {
  const {uid, name} = player;
  return html`
    <div>
      <a href="/player/${uid}">${name}</a>
    </div>
  `;
}

function Application({ children }) {
  return html`
    <div id="app">
      ${children}
    </div>
  `;
}

function parse_data() {
  // const length = parseInt(process.env.NODE_CTX_LEN);
  // console.error(length);
  // const data = process.stdin.read(length);
  // console.error(data);
  // if(typeof data === "string") return JSON.parse(data);
  // if(data===null) return {};
  // return JSON.parse(data.toString());
  return JSON.parse(readFileSync(0).toString());
}

module.exports = { PlayerBox, Application, parse_data };
