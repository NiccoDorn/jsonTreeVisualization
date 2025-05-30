// main - jetzt mit input über klassische Event Listener
document.getElementById("loadBtn").addEventListener("click", () => {
  const input = document.getElementById("jsonInput").value;
  let parsedJson;
  try {
    parsedJson = JSON.parse(input);
  } catch (err) {
    alert("Invalid JSON:\n" + err.message);
    return;
  }

  d3.select("svg").selectAll("*").remove();
  initializeVisualization(parsedJson);
  document.getElementById('inputContainer').style.display = 'none';
  document.getElementById('resetBtn').style.display = 'inline-block';
  document.querySelectorAll('.exportBtn').forEach(btn => btn.style.display = 'inline-block');
});

document.getElementById("resetBtn").addEventListener("click", () => {
  d3.select("svg").selectAll("*").remove();
  document.getElementById('inputContainer').style.display = 'block';
  document.getElementById('resetBtn').style.display = 'none';
  document.querySelectorAll('.exportBtn').forEach(btn => btn.style.display = 'none');
  document.getElementById("jsonInput").value = ""; // sicherstellen, dass nix zwischengespeichert wird
  window.scrollTo(0, 0); // zurück nach oben
});

document.getElementById("printBtnPDF").addEventListener("click", () => {
  window.print(); // geht's vielleicht ganz lazy über css media query? JAAA!
});

document.getElementById("printBtnSVG").addEventListener("click", () => {
  return; // TODO: Implement me.
});

document.getElementById("printBtnPNG").addEventListener("click", () => {
  return; // TODO: Implement me.
});


// darstellung 
function initializeVisualization(rawJson) {

  function buildTree(name, node) {
    const newNode = { name };

    if (node === null) {
      return newNode;
    }
    
    if (typeof node === 'number' || typeof node === 'boolean' || typeof node === 'string') {
      return { name: String(node) };
    }

    const children = [];

    if (Array.isArray(node)) {
      for (const item of node) {
        if (item === null) {
          children.push({ name: "null" });
        } else if (typeof item === 'number' || typeof item === 'boolean' || typeof item === 'string') {
          children.push({ name: item });
        } else if (typeof item === 'object') {
          children.push(buildTree(item.name || "map", item.children || item));
        }
      }
    } else if (typeof node === 'object') {
      for (const key in node) {
        if (key === "path") continue;

        const value = node[key];

        if (value === null) {
          children.push({ name: `${key}: null` });
        } else if (typeof value === 'number' || typeof value === 'boolean' || typeof value === 'string') {
          children.push({ name: `${key}: ${value}` });
        } else {
          children.push(buildTree(key, value));
        }
      }
    }

    if (children.length > 0) {
      newNode.children = children;
    }

    return newNode;
  }


  let rootName = "root";
  let rootData = rawJson;

  if (!Array.isArray(rawJson) && typeof rawJson === 'object') {
    const keys = Object.keys(rawJson);
    if (keys.length === 1) {
      rootName = keys[0];
      rootData = rawJson[rootName];
    }
  }
  
  const data = buildTree(rootName, rootData);
  const root = d3.hierarchy(data, d => d.children);
  root.x0 = 50;
  root.y0 = 0;

  root.children.forEach(collapse);

  function collapse(d) {
    if (d.children) {
      d._children = d.children;
      d._children.forEach(collapse);
      d.children = null;
    }
  }

  const svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height"),
        g = svg.append("g").attr("transform", "translate(150,0)");

  const tree = d3.tree().size([height, width]);
  const duration = 400;

  let i = 0;

  update(root);

  function update(source) {
    const treeData = tree(root);
    const nodes = treeData.descendants();
    const links = treeData.links();

    nodes.forEach(d => d.y = d.depth * 200);

    const node = g.selectAll("g.node")
      .data(nodes, d => d.id || (d.id = ++i));

    const nodeEnter = node.enter().append("g")
      .attr("class", "node")
      .attr("transform", _d => `translate(${source.y0},${source.x0})`)
      .on("click", (_event, d) => {
        if (d.children) {
          d._children = d.children;
          d.children = null;
        } else {
          d.children = d._children;
          d._children = null;
        }
        update(d);
      });

    nodeEnter.append("circle")
      .attr("r", 5)
      .style("fill", d => d._children ? "#6baed6" : "#fff");

    nodeEnter.append("text")
      .attr("dy", 3)
      .attr("x", d => d.children || d._children ? -10 : 10)
      .style("text-anchor", d => d.children || d._children ? "end" : "start")
      .text(d => d.data.name);

    const nodeUpdate = nodeEnter.merge(node);

    nodeUpdate.transition()
      .duration(duration)
      .attr("transform", d => `translate(${d.y},${d.x})`);

    nodeUpdate.select("circle")
      .attr("r", 5)
      .style("fill", d => d._children ? "#6baed6" : "#fff");

    const nodeExit = node.exit().transition()
      .duration(duration)
      .attr("transform", _d => `translate(${source.y},${source.x})`)
      .remove();

    nodeExit.select("circle").attr("r", 1e-6);
    nodeExit.select("text").style("fill-opacity", 1e-6);

    const link = g.selectAll("path.link")
      .data(links, d => d.target.id);

    const linkEnter = link.enter().insert("path", "g")
      .attr("class", "link")
      .attr("d", _d => {
        const o = { x: source.x0, y: source.y0 };
        return diagonal(o, o);
      });

    const linkUpdate = linkEnter.merge(link);

    linkUpdate.transition()
      .duration(duration)
      .attr("d", d => diagonal(d.source, d.target));

    link.exit().transition()
      .duration(duration)
      .attr("d", _d => {
        const o = { x: source.x, y: source.y };
        return diagonal(o, o);
      })
      .remove();

    nodes.forEach(d => {
      d.x0 = d.x;
      d.y0 = d.y;
    });
  }

  function diagonal(s, d) {
    return `M ${s.y} ${s.x}
            C ${(s.y + d.y) / 2} ${s.x},
              ${(s.y + d.y) / 2} ${d.x},
              ${d.y} ${d.x}`;
  }
}