# exec-setup-env
CLI execution setup environment for docker resources: network, container It reduces complexity by wrapping complexity docker syntax.

### Usage
```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  login-registry
  setup-network
 ```

#### Login docker registry

```
Usage: main.py login-registry [OPTIONS]

Options:
  --username TEXT  Docker registry username  [required]
  --password TEXT  Docker registry password (optional)
  --opts TEXT      Specific registry values.
                     --opts "registry-id=1111111,server=https://private.docker.registry.url"
  --help           Show this message and exit.
```


#### Create docker network (remove if exists)

```
python main.py setup-network --name foo

# output
# -------------------------------------------------------------
# filter available networks....
# an existing network with same name exists... removing it
# creating network...
# created docker network with name foo
```
