import os
import click
import time
import subprocess
import utils

@click.group()
def cli():
    pass

@cli.command()
@click.option('--profile', required=True, help="Configured AWS profile name to authenticate to ECR")
@click.option('--registry-id', required=False, default='219919340901', help="ECR AWS registry Id. By default uses AWS US 219919340901")
@click.option('--region', required=False, default='us-east-1', help="ECR AWS region name. By default uses region us-east-1")
def authenticate_aws_ecr(profile, registry_id, region):

  try:

    utils.authenticate_with_profile(profile, registry_id, region)

  except Exception as e:

    click.secho(e, fg='red')


@cli.command()
@click.option('--image-name', required=True, help="Docker image name")
@click.option('--image-tag', required=True, help="Docker image tag")
@click.option('--registry-id', required=False, default='219919340901', help="ECR AWS registry Id")
@click.option('--region', required=False, default='us-east-1', help="ECR AWS region name")
def pull_image(image_name, image_tag, registry_id, region):

  try:

    utils.pull_image_from_registry(image_name, image_tag, registry_id, region)
    utils.tag_local_remote_image(image_name, image_tag, registry_id, region)
  except Exception  as e:
    click.secho(e, fg='red')

@cli.command()
@click.option("--name", required=True, help="Docker network name")
def setup_network(name):
  try:
    network_delete_if_exists_then_create(network=name)    
  except Exception  as e:
    click.secho(e, fg='red')

@cli.command()
@click.option('--name', required=True, help = "Docker database container name")
@click.option('--base-image', required=True, help="Docker database image")
@click.option('--network', required=True, help="Network to attach container database")
def setup_database(name, base_image, network):

  try:

    _create_local_database_image(name, base_image, network)

    _wait_thread(10)

    _run_local_database_migrations(name, network)

  except Exception as e:

    click.secho(e, fg='red')


def _wait_thread(timeout):

  for i in range(timeout):
    os.system("print \".\"")
    time.sleep(1)

def _create_local_database_image(name, base_image, network):

  try:

    click.secho("clean up existing containers to avoid crash duplicated...")

    cmd = f"docker rm -f {name}"
    subprocess.run(cmd, shell=True)

    click.secho(f"creating local database base on {base_image} with  name {name}. Attached to network {network} on port 5432...")

    cmd = f"docker run -d --name {name} --network {network}  -p 5432:5432 -e POSTGRES_USER=kong -e POSTGRES_DB=kong -e POSTGRES_PASSWORD=kong {base_image}"
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode('utf-8')

    click.secho(out)

  except subprocess.CalledProcessError as e:

    raise Exception(e.output)

def _run_local_database_migrations(name, network):


  try:
    sandbox = f"{name}-sandbox"
    cmd = f"docker run --rm --network={network} -e KONG_DATABASE=postgres -e KONG_PG_HOST={name} -e KONG_PG_PASSWORD=kong -e KONG_PASSWORD=kong {name} kong migrations bootstrap"
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode('utf-8')

    click.secho(out)

  except subprocess.CalledProcessError as e:

    raise Exception(e.output)

def network_delete_if_exists_then_create(network=None):
  
  _delete_network(network)
  _create_network(network)


def _delete_network(network=None):

  try: 

    click.secho('filter available networks....')

    cmd = f"docker network ls -f 'name={network}$' | awk '(NR>1)' | cut -d ' ' -f 1"
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT,shell=True).decode('utf-8')

    if out:
      click.secho('an existing network with same name exists... removing it')
      cmd = f"docker network rm {out}"  
      subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode('utf-8')
      
  except subprocess.CalledProcessError as e:
    raise Exception(e.output)

  return True
  
def _create_network(network=None):

  click.secho(f"creating docker network...")

  cmd = f"docker network create {network}"
  
  try:

    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT,  shell=True).decode('utf-8')

  except subprocess.CalledProcessError as e:
    raise Exception(e.output)
  
  click.secho(f"created docker network with name {network}")

  return out

cli()
