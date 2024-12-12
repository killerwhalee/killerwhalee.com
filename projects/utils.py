def list_projects(random=False):
    """
    List projects in project directory

    """

    from pathlib import Path
    from random import shuffle
    import os

    # Get path of project directory
    project_dir = Path(__file__).resolve().parent

    # Create list of project in directory
    projects = [
        project
        for project in os.listdir(project_dir)
        if os.path.isdir(project_dir / project) and project != "__pycache__"
    ]
    projects.sort()

    # Shuffle order if flag is on
    if random:
        shuffle(projects)

    return projects
