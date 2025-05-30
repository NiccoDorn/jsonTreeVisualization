#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <rootPath>"
  exit 1
fi

rootPath="$1"
rootName=$(basename "$rootPath")
exclude_regex='(^node_modules$|^\.git$|^venv$|^__pycache__$)' # set your own filter

function build_tree() {
  local dirs=()
  local files=()

  while IFS= read -r entry; do
    name=$(basename "$entry")
    if [[ ! $name =~ $exclude_regex ]]; then
      if [ -d "$entry" ]; then
        dirs+=("$entry")
      else
        files+=("$entry")
      fi
    fi
  done < <(find "$dir" -maxdepth 1 -mindepth 1 | sort)

  local json="{"
  local first=true
  for d in "${dirs[@]}"; do
    [[ $first == false ]] && json+=","
    first=false
    name=$(basename "$d")
    subtree=$(build_tree "$d")
    json+="\"$name\":$subtree"
  done

  for f in "${files[@]}"; do
    [[ $first == false ]] && json+=","
    first=false
    name=$(basename "$f")
    json+="\"$name\":{\"path\":\"$rootName/$(realpath --relative-to="$rootPath" "$f")\"}"
  done

  json+="}"
  echo "$json"
}

tree_json=$(build_tree "$rootPath")
echo "{\"$rootName\":$tree_json}" | jq -c '.' > tree.json
