#!/bin/bash
rm -rf demo
mkdir demo
PYTHONPATH=src codeanim tests/e2e.md $@
