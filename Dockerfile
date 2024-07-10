FROM python:3.8-slim

# Install PostgreSQL command-line tools
RUN apt-get update && apt-get install -y postgresql-client
