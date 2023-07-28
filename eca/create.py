"""
file for creating a new project using the eca package
it is invoked by command line using the following command:
    eca create <project_name>
    
the user is asked what template to use for the project
possible templates are:
    - basic
    - example
"""
import pathlib
import shutil

# get the template names from the templates folder
templates = [path.name for path in pathlib.Path("templates").iterdir() if path.is_dir()]


def create(project_name, template):
    """
    creates a new project using the eca package
    """
    
    # check if the project name folder either does not exist or is empty
    project_path = pathlib.Path(project_name)
    if project_path.exists() and any(project_path.iterdir()):
        print(f"project '{project_name}' already exists")
        return
    
    # check if the template exists
    if template not in templates:
        print(f"template '{template}' does not exist")
        print("possible templates are:")
        print( *templates, sep="\n - ")
        template = None
    
    # if the template is not specified, ask the user what template to use
    while template is None:
        print("what template do you want to use?")
        print("possible templates are:")
        print( *templates, sep="\n - ")
        template = input("template: ")
        
        if template not in templates:
            print(f"template '{template}' does not exist")
            print("possible templates are:")
            print( *templates, sep="\n - ")
            template = None
    
    # copy the template to the project folder
    template_path = pathlib.Path("templates") / template

    shutil.copytree(template_path, project_path)
    
    
        
    
    