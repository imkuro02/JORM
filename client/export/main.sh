#!/bin/sh
echo -ne '\033c\033]0;Client\a'
base_path="$(dirname "$(realpath "$0")")"
"$base_path/main.x86_64" "$@"
