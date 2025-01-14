#!/bin/bash
rm -rf demo
mkdir demo
PYTHONPATH=src codeanim run tests/e2e.md $@
