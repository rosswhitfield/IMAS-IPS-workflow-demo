This assumes you have cloned the repos already, since they will just be copied in

```
git clone ssh://git@git.iter.org/imas/access-layer.git
git clone ssh://git@git.iter.org/imas/data-dictionary.git
```

To build docker image

```
docker build . --tag imas
```

To run IPS-IMAS demo in container

```
docker run imas
```
