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


templates = {path.absolute(): path.name for path in (path / "templates").iterdir() if path.is_dir()}

# add tutorials to the list of templates
tutorial_names = {
    "T1": "Tutorial 1: The Event System",
    "T2": "Tutorial 2: Creating your first Block",
}
tutorials = {path.absolute(): tutorial_names[path.name] for path in (path / "tutorials").iterdir() if path.is_dir()}
templates.update(tutorials)




@cli.command()
def create(project_name: str = ""):
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
    
    # if the template is not specified, ask the user what template to use
    # use the PyInquirer package
    questions = [
        {
            'type': 'list',

            'name': 'template',
            'message': 'what template do you want to use?',
            'choices': list(templates.values())
        }
    ]
    
    answers = prompt(questions)
    template = answers['template']
    # convert the tutorial name to the path
    template = list(templates.keys())[list(templates.values()).index(template)]


    shutil.copytree(template, project_path)

    rprint(f"[green]project '{project_name}' created[/green]")

@cli.command()
def ship():
    print("All hands on deck!")


if __name__ == '__main__':
    cli(["create"])