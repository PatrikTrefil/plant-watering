#!/bin/bash

set -euo pipefail

# HACK: use config.json
status_file="$(jq -r ".status_file" < config.json)"
log_repo_path="$(jq -r ".log_repo" < config.json)"

eval status_file="$status_file"

echo "Status file $status_file"
cat "$status_file"
echo ""

new_file_name="$(date "+%Y_%m_%d__%H_%M").txt"

cp -v "$status_file" "${log_repo_path}/$new_file_name"

cd "$log_repo_path"
git add "$new_file_name"
git ci -m "automatic update"
git push
