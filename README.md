# Mantium Web Interface

The web interface for the [automation](https://github.com/hivesolutions/automium) build system.  
Should be able to control a set of automium projects displaying the results of build runs.
The automium system uses the atm file specification that defines a zip file containing
both the specification (build.json) file and the scripts to be run.

## Installation

* `easy_install mantium`

## Configuration

### Viriatum

In order to configure automium together with viraitum you must add a new location to
the **viriatum.ini** configuration file.

```
[location:automium]
path = /automium
handler = wsgi
script_path = /usr/local/lib/python2.7/dist-packages/mantium-$VERSION-py2.7.egg/automium_web.wsgi
```

## Inspiration

* File storage website with minimalistic approach [ge.tt](http://ge.tt)
