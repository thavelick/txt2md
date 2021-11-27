#!/bin/bash
set -e
diff examples/lorem/expected_unwrap.txt <(./unwrap.py examples/lorem/input.txt)
diff examples/lorem/expected_out.txt <(./txt2md.py examples/lorem/input.txt)
diff examples/rfc/expected_out.txt <(./txt2md.py examples/rfc/input.txt)
diff examples/page_headers/expected_out.txt <(./txt2md.py examples/page_headers/input.txt)
which pylint > /dev/null && pylint -s n *.py
which mypy > /dev/null && mypy --strict *.py
