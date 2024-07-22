#!/bin/sh

# Run the migrations
flask db upgrade

# Execute the provided command
exec "$@"