#!/usr/bin/env bash
# Utility to find all occurrences of a string in every .mak and .yaml file
find . \( -name \*.mak -o -name \*.yaml \) -exec grep "${1}" '{}' \; -print
