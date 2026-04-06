import typer
from rich.console import Console
from rich.table import Table
import requests
import time
import os

app = typer.Typer(help="BishopTech Swarm CLI")
console = Console()

API_URL = os.getenv("SWARM_API_URL", "http://localhost:8000/api")

@app.command()
def templates():
    """List all agent templates."""
    try:
        response = requests.get(f"{API_URL}/templates")
        response.raise_for_status()
        data = response.json()
        
        table = Table(title="Agent Templates")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("API", style="green")
        
        for t in data:
            table.add_row(str(t["id"]), t["name"], t["default_api"])
            
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error fetching templates: {e}[/red]")

@app.command()
def swarms():
    """List all swarms."""
    try:
        response = requests.get(f"{API_URL}/swarms")
        response.raise_for_status()
        data = response.json()
        
        table = Table(title="Swarms")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Description", style="green")
        
        for s in data:
            table.add_row(str(s["id"]), s["name"], s["description"])
            
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error fetching swarms: {e}[/red]")

@app.command()
def run(swarm_id: int, prompt: str):
    """Run a swarm with a given prompt."""
    try:
        response = requests.post(f"{API_URL}/swarms/{swarm_id}/run", json={"input_prompt": prompt, "swarm_id": swarm_id})
        response.raise_for_status()
        run_data = response.json()
        run_id = run_data["id"]
        console.print(f"[green]Swarm started! Run ID: {run_id}[/green]")
        console.print("Waiting for completion...")
        
        # Poll for completion
        while True:
            time.sleep(2)
            res = requests.get(f"{API_URL}/runs/{run_id}")
            res.raise_for_status()
            current_run = res.json()
            status = current_run["status"]
            
            if status == "completed":
                console.print(f"\n[bold green]Run Completed![/bold green]\n")
                console.print(f"[bold cyan]Final Output:[/bold cyan]\n{current_run['final_output']}")
                break
            elif status == "failed":
                console.print(f"\n[bold red]Run Failed![/bold red]\n")
                console.print(current_run.get('final_output', 'Unknown error'))
                break
                
    except Exception as e:
        console.print(f"[red]Error running swarm: {e}[/red]")

@app.command()
def logs(run_id: int):
    """View logs for a specific run."""
    try:
        res = requests.get(f"{API_URL}/runs/{run_id}")
        res.raise_for_status()
        current_run = res.json()
        
        console.print(f"[bold cyan]Run {run_id} Status: {current_run['status']}[/bold cyan]")
        
        for log in current_run.get("logs", []):
            console.print(f"\n[bold magenta]--- Agent: {log['agent_name']} ---[/bold magenta]")
            console.print(log['output'])
            
    except Exception as e:
        console.print(f"[red]Error fetching logs: {e}[/red]")

if __name__ == "__main__":
    app()
