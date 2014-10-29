# Mantium Web Interface

The web interface for the [automation](https://github.com/hivesolutions/automium) build system.  
Should be able to control a set of automium projects displaying the results of build runs.
The mantium system uses the atm file specification that defines a zip file containing
both the specification (build.json) file and the scripts to be run.

## Installation

    pip install mantium

## Configuration

### Viriatum

In order to configure automium together with viraitum you must add a new location to
the **viriatum.ini** configuration file.

```
[location:mantium]
path = /mantium
handler = wsgi
script_path = /usr/local/lib/python$PY_VERSION/dist-packages/mantium-$VERSION-py$PY_VERSION.egg/mantium.wsgi
```

## Inspiration

* File storage website with minimalistic approach [ge.tt](http://ge.tt)
