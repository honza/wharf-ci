wharf-ci
========

Jenkins-like, docker-based, DVCS-backed build system

How it works
------------

* wharf-ci is a Django app that lets you create projects that will be built
* GitHub's web hooks will kick off builds
* Each build happens in a new docker container
* Add a Dockerfile for your project
* Add a build command for your project
* Show build history
* Keep failed builds around for inspection
* Trigger hooks on successful builds

License
-------

BSD, short and sweet
