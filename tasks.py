from invoke import task

# This file allows you to define some 'tasks', which you can run using "invoke format" etc

PROJECT_DIR = "wordle"


@task
def develop(c):
    """Install this package in to conda environment in 'development' mode."""
    # c is the Context of invoke
    c.run("conda develop .")


@task
def format(c):
    """Run automatic formatting/linting."""
    # c is the Context of invoke
    c.run(f"black --line-length 120 {PROJECT_DIR} tests")
    c.run(f"autoflake -i -r {PROJECT_DIR} tests")
    c.run(f"isort {PROJECT_DIR} tests")


@task
def check(c):
    """Check for formatting/linting errors."""
    # c is the Context of invoke
    c.run(f"black --line-length 120 --check {PROJECT_DIR} tests")
    c.run(f"flake8 {PROJECT_DIR} tests")
    c.run(f"isort -c {PROJECT_DIR} tests")


@task
def test(c):
    """Run unit tests."""
    # c is the Context of invoke
    c.run("pytest --color=yes")
