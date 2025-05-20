# jsonTreeVisualization
This is a simple project that aims at visualizing arbitrary json structures as a collapsable tree in HTML/CSS/JS.
Idea: If you're working with a big project and want to view generated structure of files with a specific substring in a specific project or any
other generated json structure, you can do that by either going through the json or having a nice collapsable tree of that structure
where you can select what structure you leave collapsed and which one you want to view. As an example, I include a cursed but valid .json
as well as the Barometric files in baro_hierarchy.json hierarchy (notice: no matching for altitude!) 
from the root project ardupilot, which can be found here: https://github.com/ArduPilot/ardupilot .
I might later upload how I generated this .json. But in itself, it is not the main focus of this repo.
If you still wanna see it, contact me or open an issue (if that works).

## Requirements File for the Python Setup Scripts
- Well... install the packages yourself if you desparately want to use old Python versions

## HTTP/HTTPS Webserver
- `startWebVizHTTP(S).py` scripts to fire up a simple webserver on localhost
  - the HTTPS variant makes use of self-signed certs (Santa Corp), of which at least the CN needs to be provided.
  - see `cert.pem` and `key.pem`
  - see also a discussion with ChatGPT, why HTTPS Localhost may be relevant depending on the environment `security_convo_localhost_https.md`
  - 
## HTML Skeleton:
- `index.html`,
  - invokes the jsonViz.js script, which then fetches some json (can be a different one)
  - invokes a d3.v7.min.js as the `d3_v7.min.js` file, which I copied to local env (see copyright notice) to stay strictly in localhost communication mode
  - invokes a `styles.css` which can be expanded depending on what DOM elements are used in the static `index.html`

## Visualization:
- `jsonViz.js`:
  - fetches the json file, here you can define, which .json file you to visualize, at the moment it is "nasty.json"
  - recursively builds a tree from provided json structure, probably not exhaustive but this is as far as I'll do it
  - renders a tree with html/css and .js generated css rules

