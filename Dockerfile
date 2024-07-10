FROM python:3.8-slim

# Install PostgreSQL command-line tools
RUN apt-get update && apt-get install -y postgresql-client

# Update and install ChromaDB
RUN pip3 install chromadb

# Pull the official Chroma image
RUN docker pull chromadb/chromadb:latest

# Run ChromaDB
CMD ["chromadb", "--db-path", "/data"]