#!/bin/bash

export PYTHONPATH=/app:$PYTHONPATH
# Run database migrations
alembic upgrade head

# Start the main application (execute the command passed to the script)
exec "$@"
