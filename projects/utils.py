from pathlib import Path
import os


class Project:
    def __init__(self, path):
        # Basic name/desc for project
        self.name = os.path.basename(path)
        self.description = ""

        # Does project use websocket?
        self.routes = os.path.exists(path / "routes.py")

    def __eq__(self, value):
        if isinstance(value, Project):
            return self.name == value.name

        elif isinstance(value, str):
            return self.name == value

        else:
            raise NotImplemented

    def __lt__(self, value):
        if isinstance(value, Project):
            return self.name < value.name

        elif isinstance(value, str):
            return self.name < value

        else:
            raise NotImplemented


def list_projects(random=False):
    """
    List projects in project directory

    """

    from random import shuffle

    # Get path of project directory
    project_dir = Path(__file__).resolve().parent

    # Create list of project in directory
    projects = [
        Project(project_dir / project)
        for project in os.listdir(project_dir)
        if os.path.isdir(project_dir / project) and project != "__pycache__"
    ]
    projects.sort()

    # Shuffle order if flag is on
    if random:
        shuffle(projects)

    return projects
