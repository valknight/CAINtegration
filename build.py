import os
import shutil
import click
import PyInstaller.__main__

files = ['config.example.json', 'miniweb.exe']
directories = ['web']

if __name__ == '__main__':
    click.echo(click.style('Cleaning up existing builds...'))
    shutil.rmtree('dist')
    click.echo(click.style('Running pyinstaller...'))
    PyInstaller.__main__.run([
        'main.py',
        '--onefile'
    ])
    click.echo(click.style('Removing build folder'))
    shutil.rmtree('build')
    click.echo(click.style('Copying requirements'))
    for folder in directories:
        shutil.copytree(folder, 'dist/{}'.format(folder))
    for f in files:
        shutil.copyfile(f, 'dist/{}'.format(f))