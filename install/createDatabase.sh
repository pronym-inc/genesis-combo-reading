#!/usr/bin/env bash
echo "Creating database..."
createuser -s genesis_combo_reading || :
createdb -O genesis_combo_reading genesis_combo_reading || :