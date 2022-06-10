#!/bin/bash

find . -name '*.py' -not -path "./env/*" -exec autopep8 --select E11,E127 -a --in-place '{}' \;