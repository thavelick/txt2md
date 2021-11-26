#!/bin/bash
set -e
diff examples/lorem/expected_unwrap.txt <(./unwrap.py examples/lorem/input.txt)
diff examples/lorem/expected_out.txt <(./txt2md.py examples/lorem/input.txt)
diff examples/rfc/expected_out.txt <(./txt2md.py examples/rfc/input.txt)
