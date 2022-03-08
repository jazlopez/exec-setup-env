# exec-setup-env
CLI execution setup environment for docker resources: network, container It reduces complexity by wrapping complexity docker syntax.

### Install 

You require to have python3 and PIP to install module dependencies.

```
python -V
# Python 3.9.1

# install dependencies

pip install -r requirements.txt
```

### Usage
```
Options:
  --help  Show this message and exit.

Commands:
  authenticate-aws-ecr
  pull-image
  setup-database
  setup-network
 ```

#### Authenticate 

```
Usage: main.py authenticate-aws-ecr [OPTIONS]

Options:
  --profile TEXT      Configured AWS profile name to authenticate to ECR
                      [required]
  --registry-id TEXT  ECR AWS registry Id. By default uses AWS US 219919340901
  --region TEXT       ECR AWS region name. By default uses region us-east-1
  --help              Show this message and exit.
```

Example

```
python main.py authenticate-aws-ecr --profile awsprodus

```

#### Pull image from registry

```
Usage: main.py pull-image [OPTIONS]

Options:
  --image-name TEXT   Docker image name  [required]
  --image-tag TEXT    Docker image tag  [required]
  --registry-id TEXT  ECR AWS registry Id
  --region TEXT       ECR AWS region name
  --help              Show this message and exit.

```

Example

```
python main.py pull-image --image-name edt-kong-gateway-ee --image-tag 2.1.3.1
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
