import os
import click
import logging
import subprocess

@click.group()
def cli():
    pass

@cli.command()
@click.option("--name", required=True, help="Docker network name")
def setup_network(name):
  
  try:

    network_delete_if_exists_then_create(network=name)
    
  except Exception  as e:
    click.secho(e, fg='red')


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
