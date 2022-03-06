# exec-setup-env
CLI execution setup environment for docker resources: network, container It reduces complexity by wrapping complexity docker syntax.

### Usage
```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  setup-network
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

### Contact

Contact me if you want to contribute.
