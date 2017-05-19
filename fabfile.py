from fabric.api import local, run, settings, env
import config

env.user = "root"


# actions that are identical remotely and locally are extracted here :)
actions = dict(build="docker build -t {}:TAG ."
                     .format(config.docker_repository),
               push="docker push {}"
                    .format(config.docker_repository),
               create_network="docker network create {}".
                              format(config.docker_network),
               pull="docker pull {}"
                    .format(config.docker_repository),
               start="docker run -d --name {} --net {} -p {}:{} "
                     "-e ST_AUTH={} {}:TAG".
                     format(*config.DOCKER_APP_CONFIG),
               stop="docker stop {}; docker rm {}".
                     format(config.app_name, config.app_name),
               status="docker ps | grep \"{}:TAG\" || echo stopped".
                      format(config.docker_repository),
               initialize_db="docker run -d --name {} --net {} "
                             "--restart unless-stopped -e POSTGRES_USER={} "
                             "-e POSTGRES_PASSWORD={} "
                             "-v {}:/var/lib/postgresql/data "
                             "-p 0.0.0.0:{}:{} postgres:{}".
                             format(*config.DOCKER_DB_CONFIG),
               destroy_db="docker stop {}; docker rm {}".
                          format(config.db_host, config.db_host))


def build(tag="latest"):
    """Build Docker image."""
    local(actions["build"].replace("TAG", tag))


def push(tag="latest"):
    """Push lastly build image to https://hub.docker.com/"""
    local(actions["push"].replace("TAG", tag))


def create_network():
    """Create Docker network that 7tweets and required DB will use."""
    with settings(warn_only=True):
        local(actions["create_network"])


def pull(tag="latest"):
    """Pull latest image from https://hub.docker.com/"""
    local(actions["pull"].replace("TAG", tag))


def start(tag="latest"):
    """Start 7tweets on local workstation."""
    local(actions["start"].replace("TAG", tag))


def remote_start(tag="latest"):
    """Remotely start 7tweets application."""
    run(actions["start"].replace("TAG", tag))


def stop():
    """Stop 7tweets on local workstation."""
    with settings(warn_only=True):
        local(actions["stop"])


def remote_stop():
    """Remotely stop 7tweets application."""
    with settings(warn_only=True):
        run(actions["stop"])


def status(tag="latest"):
    """Check if 7tweets is currently running in a container."""
    local(actions["status"].replace("TAG", tag))


def remote_status(tag="latest"):
    """Remotely check if 7tweets is alive."""
    run(actions["status"].replace("TAG", tag))


def restart():
    """Restart 7tweets on local workstation."""
    stop()
    start()


def remote_restart():
    """Remotely restart 7tweets application."""
    remote_stop()
    remote_start()


def initialize_db():
    """Raise a fresh Postgres DB on local workstation."""
    local(actions["initialize_db"])


def remote_initialize_db():
    """Remotely raise a fresh Postgres contained."""
    run(actions["initialize_db"])


def destroy_db():
    """Stop and remove local Postgres DB instance."""
    with settings(warn_only=True):
        local(actions["destroy_db"])


def remote_destroy_db():
    """Remotely stop and remove Postgres contained."""
    with settings(warn_only=True):
        run(actions["destroy_db"])


def reinitialize_db():
    """Destroy (if needed) and re-create local Postgres DB instance."""
    destroy_db()
    initialize_db()


def remote_reinitialize_db():
    """Remotely (if necessary) destroy and re-create Postgres contained."""
    remote_destroy_db()
    remote_initialize_db()


def test_locally(tag="latest"):
    """Build and push image, prepare and start all requirements locally."""
    build(tag)
    push(tag)
    with settings(warn_only=True):
        local(actions["stop"])
        local(actions["create_network"])
    local(actions["pull"].replace("TAG", tag))
    local(actions["start"].replace("TAG", tag))


def deploy(tag="latest"):
    """Build and push image and remotely prepare and start all requirements."""
    build(tag)
    push(tag)
    with settings(warn_only=True):
        run(actions["stop"])
        run(actions["create_network"])
    run(actions["pull"].replace("TAG", tag))
    run(actions["start"].replace("TAG", tag))
