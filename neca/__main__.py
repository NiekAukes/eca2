import os
import pathlib
import shutil
import typer
from PyInquirer import prompt
from rich import print as rprint


# ============================================================================================================================
#                                                Command line interface
# ============================================================================================================================

cli = typer.Typer()

sep = "\\" if os.name == "nt" else "/"
path = pathlib.Path(__file__).parent.absolute()
templates = [path.name for path in (path / "templates").iterdir() if path.is_dir()]

@cli.command()
def create(project_name: str = "", template: str = ""):
    """
    creates a new project using the eca package
    """

    # if the project name is not specified, ask the user what project name to use
    if project_name == "":
        questions = [
            {
                'type': 'input',
                'name': 'project_name',
                'message': 'what is the name of the project?',
                'default': 'my_project'
            }
        ]
        
        answers = prompt(questions)
        project_name = answers['project_name']
    
    # check if the project name folder either does not exist or is empty
    project_path = pathlib.Path(project_name)
    if project_path.exists() and any(project_path.iterdir()):
        rprint(f"[red]project '{project_name}' already exists or already contains files[/red]")
        return

    # check if the template exists
    if template != "" and template not in templates:
        # use rich print
        rprint(f"[red]template '{template}' does not exist[/red]")
        template = ""
    
    # if the template is not specified, ask the user what template to use
    # use the PyInquirer package
    if template == "":
        questions = [
            {
                'type': 'list',

                'name': 'template',
                'message': 'what template do you want to use?',
                'choices': templates
            }
        ]
        
        answers = prompt(questions)
        template = answers['template']

    # copy the template to the project folder
    template_path = path / "templates" / template

    shutil.copytree(template_path, project_path)

    rprint(f"[green]project '{project_name}' created[/green]")

@cli.command()
def ship():
    print("All hands on deck!")


if __name__ == '__main__':
    cli(["create"])