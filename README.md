# Azure DevOps MCP Server

A Model Context Protocol (MCP) server that provides seamless integration with Azure DevOps services through FastAPI. This server exposes Azure DevOps operations as MCP tools, enabling AI assistants and other MCP clients to interact with Azure DevOps projects, repositories, wikis, and file contents.

## Features

- **Project Management**: List and retrieve information about Azure DevOps projects
- **Repository Operations**: Browse repositories, list files and folders, and retrieve file contents
- **Wiki Integration**: Access and retrieve Azure DevOps wiki pages and content
- **SSE Transport**: Supports Server-Sent Events for real-time communication

## Available MCP Tools

### 1. `get_azure_devops_projects`
Retrieves all projects from an Azure DevOps organization.

**Parameters:**
- `organization_url` (optional): Azure DevOps organization URL

**Returns:** JSON with project details including ID, name, description, URL, and state.

### 2. `get_repositories`
Lists all repositories within a specific Azure DevOps project.

**Parameters:**
- `project_name` (required): Name of the Azure DevOps project
- `organization_url` (optional): Azure DevOps organization URL

**Returns:** JSON with repository information including ID, name, URL, default branch, and status.

### 3. `get_repository_items`
Browses files and folders in a Git repository.

**Parameters:**
- `project_name` (required): Name of the Azure DevOps project
- `repository_id` (required): Repository ID
- `path` (optional): Specific path to browse (defaults to root)
- `recursive` (optional): Whether to recursively list items (default: False)
- `organization_url` (optional): Azure DevOps organization URL

**Returns:** JSON with file/folder listings including paths, types, sizes, and URLs.

### 4. `get_file_content`
Retrieves the content of a specific file from a Git repository.

**Parameters:**
- `project_name` (required): Name of the Azure DevOps project
- `repository_id` (required): Repository ID
- `file_path` (required): Path to the file
- `organization_url` (optional): Azure DevOps organization URL

**Returns:** JSON with file content, metadata, and binary file detection.

### 5. `get_wiki_pages`
Accesses Azure DevOps wiki pages and their content.

**Parameters:**
- `project_name` (required): Name of the Azure DevOps project
- `wiki_id_or_name` (required): Wiki identifier or name
- `path` (optional): Specific wiki page path (defaults to root)
- `organization_url` (optional): Azure DevOps organization URL

**Returns:** JSON with wiki page content, metadata, and URLs.

## Prerequisites

- Python 3.13 or higher
- Azure DevOps Personal Access Token (PAT) with reference to https://github.com/microsoft/azure-devops-python-api
- Access to an Azure DevOps organization

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd azdo-mcp
```

2. Install dependencies using uv:
```bash
pip install uv
uv lock
uv sync
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
AZURE_DEVOPS_PAT=your_personal_access_token_here
AZURE_DEVOPS_ORG_URL=https://dev.azure.com/your-organization
```

### Azure DevOps Setup

1. Generate a Personal Access Token (PAT) in Azure DevOps:
   - Go to Azure DevOps → User Settings → Personal Access Tokens
   - Create a new token with appropriate scopes (Code: Read, Wiki: Read, Project and Team: Read)

2. Note your organization URL (typically `https://dev.azure.com/your-organization`)

## Usage

### Running the Server

Start the MCP server:

```bash
python main.py
```

The server will start on port 8080 using Server-Sent Events (SSE) transport.

## Development

### Project Structure

```
azdo-mcp/
├── main.py              # Main MCP server implementation
├── pyproject.toml       # Project configuration
├── .env                 # Environment variables (create this)
├── README.md            # This file
```


---

**Note**: This server provides read-only access to Azure DevOps resources. Ensure you have review the necessary permissions and scopes for your Personal Access Token (PAT) to access the required resources.

Please also refer to the [Azure DevOps Python API documentation](https://github.com/microsoft/azure-devops-python-api) for more details on available operations and configurations.

