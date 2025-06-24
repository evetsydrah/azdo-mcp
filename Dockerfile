
# Use a slim Python 3.13 base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy uv configuration files
COPY pyproject.toml uv.lock ./

# Install dependencies with uv
RUN pip install --no-cache-dir uvicorn fastapi httpx mcp-server python-dotenv azure-devops msrest
RUN uv sync --frozen
# Copy the entire project, including data, website_content, and school_list.py
COPY . .
# COPY ../servers/school_server/school_list.py ./school_list.py
# COPY ../servers/school_server/.env ./.env

# Expose ports 3200 (FastAPI) and 3501 (MCP SSE)
EXPOSE 8080

# Run the MCP SSE server
CMD ["uv", "run", "python", "main.py"]
