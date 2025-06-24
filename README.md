# Azure DevOps MCP Server

A Model Context Protocol (MCP) server that provides seamless integration with Azure DevOps services through FastAPI. This server exposes Azure DevOps operations as MCP tools, enabling AI assistants and other MCP clients to interact with Azure DevOps projects, repositories, wikis, and file contents.

## Features

- **Project Management**: List and retrieve information about Azure DevOps projects
- **Repository Operations**: Browse repositories, list files and folders, and retrieve file contents
- **Wiki Integration**: Access and retrieve Azure DevOps wiki pages and content
- **FastMCP Framework**: Built on the FastMCP framework for high-performance MCP tool serving
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
- Azure DevOps Personal Access Token (PAT)
- Access to an Azure DevOps organization

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd azdomcp
```

2. Install dependencies using uv:
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
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

### Using with MCP Clients

This server can be used with any MCP-compatible client. The server exposes the Azure DevOps tools through the MCP protocol, allowing AI assistants to:

- Browse your Azure DevOps projects
- Explore repository structures
- Read file contents
- Access wiki documentation
- Retrieve project metadata

### Example MCP Client Configuration

For VS Code with the MCP extension, add this to your MCP configuration:

```json
{
  "mcpServers": {
    "azure-devops": {
      "command": "python",
      "args": ["path/to/azdomcp/main.py"],
      "env": {
        "AZURE_DEVOPS_PAT": "your_pat_here",
        "AZURE_DEVOPS_ORG_URL": "https://dev.azure.com/your-org"
      }
    }
  }
}
```

## Architecture

- **FastMCP Framework**: High-performance MCP server implementation
- **Azure DevOps SDK**: Official Python SDK for Azure DevOps integration
- **SSE Transport**: Real-time communication using Server-Sent Events
- **Error Handling**: Comprehensive error handling and JSON response formatting
- **Modular Design**: Clean separation of concerns with individual tool functions

## Dependencies

- `fastmcp`: FastMCP framework for MCP server implementation
- `azure-devops`: Official Azure DevOps Python SDK
- `msrest`: Microsoft REST client library
- `httpx`: HTTP client for async operations
- `fastapi`: Modern web framework for APIs
- `python-dotenv`: Environment variable management

## Error Handling

The server includes robust error handling for common scenarios:
- Invalid authentication credentials
- Missing required parameters
- Network connectivity issues
- Resource not found errors
- Binary file detection and handling

All errors are returned as JSON responses with descriptive error messages.

## Development

### Project Structure

```
azdomcp/
├── main.py              # Main MCP server implementation
├── school_list.py       # Additional MCP tools (school-related)
├── pyproject.toml       # Project configuration
├── .env                 # Environment variables (create this)
├── README.md           # This file
└── .vscode/
    └── mcp.json        # MCP client configuration
```

### Running in Development Mode

For development with auto-reload:

```bash
uvicorn main:mcp --reload --port 8080
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue in the repository
- Check Azure DevOps SDK documentation
- Review FastMCP framework documentation

---

**Note**: This server provides read-only access to Azure DevOps resources. Ensure your PAT has the minimum required permissions for security best practices.
