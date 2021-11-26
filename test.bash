#!/bin/bash
set -e
diff examples/lorem/expected_unwrap.txt <(./unwrap.py examples/lorem/input.txt)
diff expamles/lorem/input.txt <(./txt2md examples/lorem/input.txt)
