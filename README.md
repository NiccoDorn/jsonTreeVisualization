# jsonTreeVisualization
> This is a simple project that aims at visualizing arbitrary json structures as a collapsable tree in HTML/CSS/JS.
For a first quick impression, have a look at the generated github pages link. 
<div align="center">
    🌐 <a href="https://niccodorn.github.io/jsonTreeVisualization/">Live Demo at: https://niccodorn.github.io/jsonTreeVisualization/</a> &nbsp;&nbsp;
</div>
<p></p>

Idea: If you're working with a big project and want to view generated structure of files with a specific substring in a specific project or any other generated json structure, you can do that by either going through the json or having a nice collapsable tree of that structure where you can select what structure you leave collapsed and which one you want to view. As an example, I include a cursed but valid `nasty.json` file as well as the Barometric files structure in `baro_hierarchy.json` hierarchy (notice: no matching for altitude!) from the root project ardupilot, which can be found here: https://github.com/ArduPilot/ardupilot . I might later upload how I generated this .json. But in itself, it is not the main focus of this repo. If you still wanna see it, contact me or open an issue (if that works).

## Setup Requirements File for the Python Setup Scripts
- Well... install the packages yourself if you desparately want to use old Python versions.

## Webserver Start & Stop
- start: start terminal in root directory, `cd` into `webserver` and execute `python startWebVizHTTPS.py` in Terminal
- shutdown: simply press **[Ctrl+C]** in the terminal where you started the python script from
- if you're on Windows it should start the server without difficulties but with a Browser Warning because the used TLS certificate is self-signed and not from a trusted CA.
- on Linux you might need to paste the presented URL (in terminal) manually into a browser of your choice.
- some browsers, network and waf settings that you may have setup some time before, might conflict with a self-signed server start-up but should be unlikely though
- we do not talk about some partially-eaten fruits here! *yuck*

## HTTP/HTTPS Webserver
- `startWebVizHTTP(S).py` scripts to fire up a simple webserver on localhost
  - the HTTPS variant makes use of self-signed certs (Santa Corp), of which at least the CN needs to be provided.
  - see `cert.pem` and `key.pem`
  - see also a discussion with ChatGPT, why HTTPS Localhost may be relevant depending on the environment `security_convo_localhost_https.md`
    
## HTML Skeleton:
- `index.html`,
  - invokes the `jsonViz.js` script, which then fetches some json (can be a different one)
  - invokes a d3.v7.min.js as the `d3_v7.min.js` file, which I copied to local env (see copyright notice) to stay strictly in localhost communication mode
  - invokes a `styles.css` which can be expanded depending on what DOM elements are used in the static `index.html`

## Getting Data:
- see `tree_script/jsonTree.sh`, you probably first need to set the right permissions for this script with: `chmod +x jsonTree.sh`, then just execute it with `./jsonTree.sh .` as an example
- see `tree_script/jsonTree.ps1`, a powershell script that generates a nested structure which is easily parsed and visualized later, this one you execute with `.\jsonTree.ps1 .` as an example
- both scripts require of you to provide a valid path from which to generate the json. Quick use: just type `.` to get a jsonTree of the directory you're currently executing the script from, provide `..` to get a json of the path above your current directory location
- see `example_project.json`, notice that it's compressed format

## Visualization:
- `jsonViz.js`:
  - gets the json file as input, here you can define, which .json file to visualize
  - recursively builds a tree from provided json structure, probably not exhaustive but this is as far as I'll do it
  - renders a(n) expandable/collapsable tree with html/css and .js generated css rules
- in (firefox) browser you can press **[Ctrl+P]** to attempt Print to PDF Browser Function, where you can save the current expanded-collapsed tree to a .pdf file, make use of different formats to be able to fully visualize bigger trees

## Security Considerations
- if you're somehow including this into a bigger project of yours:
- consider either re-creating new `cert.pem` and `key.pem` from time to time
- if you want this as a micro-service running on some "real server" (docker container - within a kube pod) (not localhost):
  - obviously use CA certs, especially when you're doing more advanced mapping / visualization scenarios
  - adjust to your vetted communication processes in your system(s)
  - filesystem hiararchies, project config hierarchies etc. may contain sensible information and should not be leaked
- have a read into `security_convo_localhost_https.md`, it might tell you something you do not already know
