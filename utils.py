import click
import subprocess


def authenticate_with_profile(profile, registry_id, region):

    try:

        cmd = f"$(aws ecr get-login --registry-ids {registry_id} --no-include-email --region {region} --profile {profile})"

        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode('utf-8')

        click.secho(out)

    except subprocess.CalledProcessError as e:

        raise Exception(e.output)


def pull_image_from_registry(image_name, image_tag, registry_id, region):

    try:

        cmd = f"docker pull {registry_id}.dkr.ecr.{region}.amazonaws.com/{image_name}:{image_tag}"

        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode('utf-8')

        click.secho(out)

    except subprocess.CalledProcessError as e:

        raise Exception(e.output)


def tag_local_remote_image(image_name, image_tag, registry_id, region):

    try:

        cmd = f"docker tag {registry_id}.dkr.ecr.{region}.amazonaws.com/{image_name}:{image_tag} {image_name}"

        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode('utf-8')

        click.secho(out)

    except subprocess.CalledProcessError as e:

        raise Exception(e.output)
