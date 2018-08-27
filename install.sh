#!/usr/bin/env bash

set -ueo pipefail

if hash sops 2>/dev/null; then
    echo "sops is already installed:"
    sops --version
else
    echo "Please install sops: https://github.com/mozilla/sops or make it available in the PATH"
fi
