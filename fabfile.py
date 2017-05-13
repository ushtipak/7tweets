from fabric.api import local, run, settings, env
import config

env.user = "root"


actions = dict(build="docker build -t {}:TAG ."
                     .format(config.docker_repository),
               push="docker push {}"
                    .format(config.docker_repository),
               create_network="docker network create {}".
                              format(config.docker_network),
               pull="docker pull {}"
                    .format(config.docker_repository),
               start="docker run -d --name {} --net {} -p {}:{} {}:TAG".
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
    local(actions["build"].replace("TAG", tag))


def push(tag="latest"):
    local(actions["push"].replace("TAG", tag))


def create_network():
    with settings(warn_only=True):
        local(actions["create_network"])


def pull(tag="latest"):
    local(actions["pull"].replace("TAG", tag))


def start(tag="latest"):
    local(actions["start"].replace("TAG", tag))


def stop():
    with settings(warn_only=True):
        local(actions["stop"])


def status(tag="latest"):
    local(actions["status"].replace("TAG", tag))


def restart():
    stop()
    start()


def initialize_db():
    local(actions["initialize_db"])


def destroy_db():
    with settings(warn_only=True):
        local(actions["destroy_db"])


def reinitialize_db():
    destroy_db()
    initialize_db()


def remote_initialize_db():
    run(actions["initialize_db"])


def remote_destroy_db():
    with settings(warn_only=True):
        run(actions["destroy_db"])


def remote_reinitialize_db():
    remote_destroy_db()
    remote_initialize_db()


def deploy(tag="latest"):
    build(tag)
    push(tag)
    with settings(warn_only=True):
        run(actions["stop"])
        run(actions["create_network"])
    run(actions["pull"].replace("TAG", tag))
    run(actions["start"].replace("TAG", tag))
