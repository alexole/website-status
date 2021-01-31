"""Various helper tasks."""

import os
from invoke import task


@task
def clean(ctx):
    """Cleanup build artifacts and *.pyc files."""

    with ctx.cd(os.path.dirname(__file__)):
        ctx.run('python setup.py clean')
        ctx.run('find . -name "*.pyc" -delete')
        ctx.run('find . -name "__pycache__" -delete')


@task(pre=[clean])
def install(ctx):
    """Install the project with pip."""

    with ctx.cd(os.path.dirname(__file__)):
        ctx.run('pip install -e .')


@task
def pin_deps(ctx):
    """"Pin the dependencies."""

    with ctx.cd(os.path.dirname(__file__)):
        ctx.run('pip-compile --generate-hashes requirements.in')


@task
def pin_dev_deps(ctx):
    """"Pin the dev dependencies."""

    with ctx.cd(os.path.dirname(__file__)):
        ctx.run('pip-compile --generate-hashes requirements-dev.in')


@task
def deps(ctx):
    """Install the development requirements."""

    with ctx.cd(os.path.dirname(__file__)):
        ctx.run('pip install -r requirements-dev.txt')


@task
def check(ctx):
    """Run some code quality checks."""

    with ctx.cd(os.path.dirname(__file__)):
        ctx.run('flake8 --max-complexity 15 --max-line-length 120 src tests')
        ctx.run('mypy --ignore-missing-imports src tests')


@task(help={'no-coverage': 'Ignore the code coverage', 'html-report': 'Generate HTML coverage report as well',
            'no-colors': 'Remove color escape codes fro the output'})
def test(ctx, no_coverage=False, html_report=False, no_colors=False):
    """Run the tests."""

    with ctx.cd(os.path.dirname(__file__)):
        if no_coverage:
            ctx.run('env $(cat env_file | xargs) pytest --doctest-modules src tests', pty=not no_colors)
        else:
            ctx.run('env $(cat env_file | xargs) coverage run --source=src -m pytest --quiet '
                    '--doctest-modules src tests', pty=not no_colors)
            ctx.run('coverage report -m', pty=not no_colors)
            if html_report:
                ctx.run('coverage html', pty=not no_colors)
