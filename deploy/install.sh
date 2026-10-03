#!/usr/bin/env bash
# The installer moved to install.sh at the top of the repository. This file is kept so the old
# instructions (`sudo bash deploy/install.sh`, `... url`) still work.
exec bash "$(dirname "${BASH_SOURCE[0]}")/../install.sh" "$@"
