#!/bin/bash
# Double-click this file in Finder to preview FedWatch locally.
#
# Why this exists: browsers refuse to let a page opened as a file:// URL read
# other local files, so double-clicking index.html shows an empty table. This
# starts a tiny local web server in this folder and opens the page properly.
#
# Close this Terminal window (or press Ctrl-C) when you're done.

cd "$(dirname "$0")" || exit 1

PORT=8765
while lsof -i :$PORT >/dev/null 2>&1; do
    PORT=$((PORT + 1))
done

echo ""
echo "  FedWatch preview"
echo "  ----------------"
echo "  Serving $(pwd)"
echo "  http://localhost:$PORT"
echo ""
echo "  Leave this window open while you're looking at the page."
echo "  Press Ctrl-C (or just close this window) to stop."
echo ""

# Give the server a moment to bind before opening the browser
( sleep 1; open "http://localhost:$PORT" ) &

python3 -m http.server "$PORT" --bind 127.0.0.1
