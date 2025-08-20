#!/bin/bash
while true; do
  inotifywait -r -e close_write,moved_to,create ~/godai-genesis/uploads && ~/godai-genesis/sync_site.sh
done
