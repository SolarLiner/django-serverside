const { PlayerBox, Application, parse_data } = require("./common");
const { html } = require("htm/preact");
const render = require("preact-render-to-string");

const {object_list} = parse_data();

process.stdout.write(render(html`
  <${Application}>
    <h1>Players</h1>
    ${object_list.map(p => html`<${PlayerBox} player=${p}/>`)}
  <//>
`));
