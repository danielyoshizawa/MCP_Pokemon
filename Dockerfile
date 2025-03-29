# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY pyproject.toml ./
COPY src/ ./src/

# Install dependencies
RUN pip install --no-cache-dir -e .

# Expose the port
EXPOSE 8000

# Set entrypoint to run the server
CMD ["python", "src/mcp_pokemon/server.py"]