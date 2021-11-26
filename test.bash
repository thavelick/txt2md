#!/bin/bash
set -e
diff examples/simple.txt <(./unwrap.py examples/simple_folded_80.txt)
