FROM python:3.8-slim

# Install PostgreSQL command-line tools
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install chromadb


# Expose the port for Chroma
EXPOSE 8080

# Define the command to run Chroma
CMD ["chromadb"]