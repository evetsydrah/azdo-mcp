from mcp.server.fastmcp import FastMCP
import httpx
import os
import json
import base64
from dotenv import load_dotenv
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from typing import List, Dict, Any, Optional, Union

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP(
    name="Azure DevOps MCP Server",
    port=8080,
    on_duplicate_tools="error" # Set duplicate handling
    )

AZURE_DEVOPS_PAT = os.getenv("AZURE_DEVOPS_PAT")
AZURE_DEVOPS_ORG_URL = os.getenv("AZURE_DEVOPS_ORG_URL")

@mcp.tool()
def get_azure_devops_projects(organization_url: str = "") -> str:
    """Get all projects from Azure DevOps organization.
    
    This function retrieves all projects from the specified Azure DevOps organization.
    
    Args:
        organization_url: The URL of your Azure DevOps organization (optional, uses env var if not provided)
        
    Returns:
        A JSON string containing the list of projects with their details
    """
    try:
        # Use parameter or fall back to environment variable
        org_url = organization_url or AZURE_DEVOPS_ORG_URL   
      
        
        # Create a connection to the org
        credentials = BasicAuthentication('', AZURE_DEVOPS_PAT)
        connection = Connection(base_url=org_url, creds=credentials)
        
        # Get a client (the "core" client provides access to projects, teams, etc)
        core_client = connection.clients.get_core_client()
        
        # Get all projects
        projects = core_client.get_projects()
        
        # Convert to JSON serializable format
        project_list = []
        for project in projects:
            project_list.append({
                "id": project.id,
                "name": project.name,
                "description": project.description if hasattr(project, 'description') else "",
                "url": project.url if hasattr(project, 'url') else "",
                "state": project.state if hasattr(project, 'state') else ""
            })
        
        result = {
            "count": len(project_list),
            "projects": project_list
        }
        
        
        return json.dumps(result)
        
    except Exception as e:        
        return json.dumps({"error": f"Error retrieving projects: {str(e)}"})
    
@mcp.tool()
def get_repositories(project_name: str, organization_url: str = "") -> str:
    """Get all repositories in a specific project.
    
    Args:
        project_name: The name of the Azure DevOps project
        organization_url: The URL of your Azure DevOps organization (optional, uses env var if not provided)
        
    Returns:
        A JSON string containing the list of repositories in the project
    """
    if not project_name:
        #logger.error("Project name parameter is required")
        return json.dumps({"error": "Project name parameter is required"})
    
    try:
        # Use parameter or fall back to environment variable
        org_url = organization_url or AZURE_DEVOPS_ORG_URL
        
        #logger.info(f"Retrieving repositories for project: {project_name}")
        
        # Create a connection to the org
        credentials = BasicAuthentication('', AZURE_DEVOPS_PAT)
        connection = Connection(base_url=org_url, creds=credentials)
        
        # Get a Git client
        git_client = connection.clients.get_git_client()
        
        # Get repositories
        repositories = git_client.get_repositories(project=project_name)
        
        # Convert to JSON serializable format
        repo_list = []
        for repo in repositories:
            repo_list.append({
                "id": repo.id,
                "name": repo.name,
                "url": repo.remote_url if hasattr(repo, 'remote_url') else "",
                "default_branch": repo.default_branch if hasattr(repo, 'default_branch') else "",
                "is_disabled": repo.is_disabled if hasattr(repo, 'is_disabled') else False
            })
        
        result = {
            "project_name": project_name,
            "count": len(repo_list),
            "repositories": repo_list
        }
        
        #logger.info(f"Successfully retrieved {len(repo_list)} repositories for project {project_name}")
        return json.dumps(result)
        
    except Exception as e:
        #logger.error(f"Error retrieving repositories: {str(e)}")
        return json.dumps({"error": f"Error retrieving repositories: {str(e)}"})


@mcp.tool()
def get_repository_items(project_name: str, repository_id: str, path: str = "", recursive: bool = False, organization_url: str = "") -> str:
    """Get items (files and folders) from a Git repository.
    
    Args:
        project_name: The name of the Azure DevOps project
        repository_id: The ID of the repository
        path: Path to the item (optional, defaults to root)
        recursive: Whether to get items recursively (default: False)
        organization_url: The URL of your Azure DevOps organization (optional, uses env var if not provided)
        
    Returns:
        A JSON string containing the list of items in the repository path
    """
    if not project_name:
        #logger.error("Project name parameter is required")
        return json.dumps({"error": "Project name parameter is required"})
        
    if not repository_id:
        #logger.error("Repository ID parameter is required")
        return json.dumps({"error": "Repository ID parameter is required"})
    
    try:
        # Use parameter or fall back to environment variable
        org_url = organization_url or AZURE_DEVOPS_ORG_URL
        
        #logger.info(f"Retrieving items from repository {repository_id} in project {project_name}, path: {path}")
        
        # Create a connection to the org
        credentials = BasicAuthentication('', AZURE_DEVOPS_PAT)
        connection = Connection(base_url=org_url, creds=credentials)
        
        # Get a Git client
        git_client = connection.clients.get_git_client()
        
        # Get items
        recursion_level = "Full" if recursive else "None"
        items = git_client.get_items(
            repository_id=repository_id, 
            project=project_name,
            scope_path=path,
            recursion_level=recursion_level
        )
        
        # Convert to JSON serializable format
        item_list = []
        for item in items:
            item_list.append({
                "path": item.path,
                "is_folder": item.is_folder if hasattr(item, 'is_folder') else False,
                "size": item.size if hasattr(item, 'size') else 0,
                "url": item.url if hasattr(item, 'url') else ""
            })
        
        result = {
            "project_name": project_name,
            "repository_id": repository_id,
            "path": path,
            "recursive": recursive,
            "count": len(item_list),
            "items": item_list
        }
        
        #logger.info(f"Successfully retrieved {len(item_list)} items from repository")
        return json.dumps(result)
        
    except Exception as e:
        #logger.error(f"Error retrieving repository items: {str(e)}")
        return json.dumps({"error": f"Error retrieving repository items: {str(e)}"})

@mcp.tool()
def get_file_content(project_name: str, repository_id: str, file_path: str, organization_url: str = "") -> str:
    """Get content of a file from a Git repository.
    
    Args:
        project_name: The name of the Azure DevOps project
        repository_id: The ID of the repository
        file_path: Path to the file
        organization_url: The URL of your Azure DevOps organization (optional, uses env var if not provided)
        
    Returns:
        A JSON string containing the file content and metadata
    """
    if not project_name:
        #logger.error("Project name parameter is required")
        return json.dumps({"error": "Project name parameter is required"})
        
    if not repository_id:
        #logger.error("Repository ID parameter is required")
        return json.dumps({"error": "Repository ID parameter is required"})
        
    if not file_path:
        #logger.error("File path parameter is required")
        return json.dumps({"error": "File path parameter is required"})
    
    try:
        # Use parameter or fall back to environment variable
        org_url = organization_url or AZURE_DEVOPS_ORG_URL
        
        #logger.info(f"Retrieving file content: {file_path} from repository {repository_id}")
        
        # Create a connection to the org
        credentials = BasicAuthentication('', AZURE_DEVOPS_PAT)
        connection = Connection(base_url=org_url, creds=credentials)
        
        # Get a Git client
        git_client = connection.clients.get_git_client()
        
        # Get the item
        item = git_client.get_item(
            repository_id=repository_id,
            project=project_name,
            path=file_path,
            include_content=True
        )
        
        # Return error if it's a folder
        if getattr(item, 'is_folder', False):
            return json.dumps({"error": f"Path {file_path} is a folder, not a file"})
        
        # Handle content
        content = None
        is_binary = False
        
        if hasattr(item, 'content') and item.content:
            # If content is base64-encoded
            if hasattr(item, '_links') and getattr(item, 'encoding', '') == 'base64':
                try:
                    content = base64.b64decode(item.content).decode('utf-8')
                except UnicodeDecodeError:
                    is_binary = True
                    content = None
            else:
                content = item.content
        
        result = {
            "project_name": project_name,
            "repository_id": repository_id,
            "file_path": file_path,
            "content": content,
            "is_binary": is_binary,
            "size": getattr(item, 'size', 0),
            "url": getattr(item, 'url', "")
        }
        
        #logger.info(f"Successfully retrieved file content for {file_path}")
        return json.dumps(result)
        
    except Exception as e:
        #logger.error(f"Error retrieving file content: {str(e)}")
        return json.dumps({"error": f"Error retrieving file content: {str(e)}"})

@mcp.tool()
def get_wiki_pages(project_name: str, wiki_id_or_name: str, path: str = "", organization_url: str = "") -> str:
    """Get Azure DevOps wiki pages.
    
    Args:
        project_name: The name of the Azure DevOps project
        wiki_id_or_name: The ID or name of the wiki
        path: Path to the wiki page (optional, defaults to root)
        organization_url: The URL of your Azure DevOps organization (optional, uses env var if not provided)
        
    Returns:
        A JSON string containing the wiki page information and content
    """
    if not project_name:
        #logger.error("Project name parameter is required")
        return json.dumps({"error": "Project name parameter is required"})
        
    if not wiki_id_or_name:
        #logger.error("Wiki ID or name parameter is required")
        return json.dumps({"error": "Wiki ID or name parameter is required"})
    
    try:
        # Use parameter or fall back to environment variable
        org_url = organization_url or AZURE_DEVOPS_ORG_URL
        
        #logger.info(f"Retrieving wiki page: {path} from wiki {wiki_id_or_name} in project {project_name}")
        
        # Create a connection to the org
        credentials = BasicAuthentication('', AZURE_DEVOPS_PAT)
        connection = Connection(base_url=org_url, creds=credentials)
        
        # Get a wiki client
        wiki_client = connection.clients.get_wiki_client()
        
        # Get the wiki page
        wiki_page = wiki_client.get_page(
            project=project_name, 
            wiki_identifier=wiki_id_or_name, 
            path=path,
            recursion_level="OneLevel", 
            include_content=True
        )
        
        result = {
            "project_name": project_name,
            "wiki_id_or_name": wiki_id_or_name,
            "path": getattr(wiki_page, 'path', path),
            "content": getattr(wiki_page, 'content', ""),
            "id": getattr(wiki_page, 'id', ""),
            "url": getattr(wiki_page, 'url', "")
        }
        
        #logger.info(f"Successfully retrieved wiki page: {path}")
        return json.dumps(result)
        
    except Exception as e:
        #logger.error(f"Error retrieving wiki page: {str(e)}")
        return json.dumps({"error": f"Error retrieving wiki page: {str(e)}"})



if __name__ == "__main__":
    # mcp.run(transport="streamable-http")
    mcp.run(transport="sse")
