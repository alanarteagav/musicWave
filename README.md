# ![musicWave Logo](resources/musicWave50.png) musicWave
System to create and manipulate a musical database.

## Python Version
musicWave uses Python version 3.5.2 or higher, to see your current Python 3
version, you can run in your terminal:

```
python3 --version
```

alternatively, you can download the latest Python 3 version in the following
link:

[download Python3](https://www.python.org/downloads/)

## Getting dependencies
musicWave uses the following dependencies:

- mutagen
- PyGObject 3.30.1
- pdoc

to install them, you should run the following commands in the terminal:
```
pip3 install mutagen
pip3 install PyGObject
pip3 install pdoc
```

## Running musicWave

To run music wave, you have to use this command (it'll invoke the python
interpreter):

```
python3 -m music_wave.main
```

## Making searches in musicWave

You can make searches in multiple fields using the search bar of the program
main window. These are the valid fiels:

- Title, use:
```
title : your search     or    t : your search
```
- Performer, use:
```
performer : your search    or    p : your search
```
- Album, use:
```
album  your search    or    a : your search
```

- Genre, use:
```
genre : your search    or     g : your search
```
- Year, use:
```
genre : your search   or     y : your search
```

Multiple searches are also allowed, using a syntax like this (note the points
between sentences, which are translated into "AND"):
```
album : my album.  title : some title.  performer : random performer.
```

## Documenting code

To document the code, we will use the pdoc module, first, you have to place
yourself inside the musicWave directory, and then, update the PYTHONPATH,
by running this command:
```
export PYTHONPATH=$(pwd)
```

Next, you have to run this command to generate the documentation inside HTML
files in a directory named "docs" inside the musicWave project folder.
```
pdoc --html --all-submodules --overwrite --html-dir docs music_wave/
```

That command will generate a new "docs" folder, in which are going to be placed
the new HTML files with the code documentation (it'll also include an index.html file).

## Running unit tests

To run the project's unit test, you must run this command once you're in the
musicWave project directory:

```
python3 -m setup.py test
```
