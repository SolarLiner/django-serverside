const {Application, parse_data} = require("./common");
const {html} = require("htm/preact");
const render = require("preact-render-to-string");


const {object} = parse_data();
process.stdout.write(render(html`
  <${Application}>
    <h1>Player: ${object.name}</h1>
    <a href="/">Back</a>
    <h2>Games</h2>
    <table style="border-radius: 1px">
      <thead>
        <tr>
          <th>Game</th>
          <th>Score</th>
        </tr>
      </thead>
    <tbody>
      ${object.scores.map(({game, score}) => html`<tr><td>${game.name}</td><td>${score}</td></tr>`)}
    </tbody>
    </table>
    <h2>Data</h2>
    <pre><code>${JSON.stringify(object.scores, null, 4)}</code></pre>
  <//>
`));
