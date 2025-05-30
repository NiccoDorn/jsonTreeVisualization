# TODO List for future visualization and functionality
> Since the visualization is only dependent on a valid .json (.json validity in this particular project is very broad), one can easily re-use this "overview management" for different purposes. A very far but cool scenario: You have a hierarchy of servers in a network, one node errors / endpoint fails: Click that node and get transferred to a different window with most recent changes and from there immediately locate all important ressources / communication points to be able to very quickly troubleshoot and identify potential problems. Like this, this tool could server as a central monitoring overview tool.

## Making this a github hosted website
- [x] Let the webserver script run as github pages subdomain
- [x] Provide Github Pages demo functionality

## Visualization and additional functionality
- [x] Allow for user input json via input field
- [x] Implement reset and print functionalities
- [x] Adjust CSS for better looks
- [ ] Implement Print to SVG and Print to PNG functionalities
- [ ] Add coloring to different types and file extensions as leafs/endpoints (small task)
- [ ] add buttons for "expand all" and "collapse all" for easy use + search functionality, which marks the searched and found node
- [ ] Testing and give circle inner info like "tested"/"vetted"/"reviewed"
- [x] include Linux/Windows .json generation script for directory json generation or implement your custom json generator for whatever
- [ ] For massive amounts of same-level item, predefine minimal vertical distance between branches
- [x] Test with an exhaustive set of different but valid .json structures

## Extension / VSCode integrated [Optional]
- [ ] include in development pipeline for quick overview as quick launch extensions or similar
- [ ] VSCode right-click functionality for selected directory for a quick overview using a .json generator script for that selected directory

## Merging  with bigger analysis tool [Optional]
- [ ] For (sub-)domain checking and validation (Automated Ownership Detection): "Scanned" & "Result"
- [ ] Some scores about attack vectors that have been performed - inspired by structure of CVE/CWE/MITRE database
- [ ] Azure Cloud Mapping and traversal overview information (Tenants/Subscriptions/Ressources like Workspaces or Azure Keyvaults)
    - [ ] Azure/Azure Cloud already provides its own tree visualization of some system's or cluster's network hierarchy
    - [ ] However, it can not be easily annotated with custom status like "security tested" or similar (afaik)
- [ ] Kubernetes Cluster Mapping within Managed Azure Cloud Environment / Azure AD and on premise systems

## Transformations into other structures: From tree to graph [Optional]
- [ ] endpoint checking for multiple occurences/usages in e.g. imports and process pipeline
- [ ] basically PDG of some software stack like ArduPilot: use existing research to leverage analysis (Web Security/ Systems Security)
- [ ] Flow of function calls of the same function throughout different files for visualization