#!/bin/bash
rm -rf demo
mkdir demo
PYTHONPATH=. codeanim tests/e2e.md $@
