FROM python:3.8-slim

# Install PostgreSQL command-line tools
RUN apt-get update && apt-get install -y postgresql-client


FROM chromadb

WORKDIR /chroma/chroma

COPY ../../../Chromadb/chroma-retail /chroma/chroma


