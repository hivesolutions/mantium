# Automium Web Interface

The web interface for the [automation](https://github.com/hivesolutions/automium) build system.  
Should be able to control a set of automium projects displaying the results of build runs.
The automium system uses the atm file specification that defines a zip file containing
both a 

## Installation

* `easy_install automium_web`

## Configuration

### Viriatum

In order to configure automium together with viraitum you must add a new location to
the ''viritaum.ini'' configuration file.

```[location:automium]
path = /automium
handler = wsgi
script_path = /usr/local/lib/python2.7/dist-packages/automium_web-0.1.0-py2.7.egg/automium_web.wsgi
```

## Inspiration

* File storage website with minimalistic approach [ge.tt](http://ge.tt)