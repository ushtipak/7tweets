from fabric.api import local, run, settings, env

env.user = "root"

repository = "ushtipak/7tweets"
name = repository.split("/")[1]
port = 2500
network = "radionica"

actions = dict(build="docker build -t {}:TAG .".format(repository),
               push="docker push {}".format(repository),
               create_network="docker network create {}".format(network),
               start="docker run -d --name {} --net {} -p {}:{} {}:TAG".
                     format(name, network, port, port, repository),
               stop="docker stop {}; docker rm {}".format(name, name),
               status="docker ps | grep \"{}:TAG\" || echo stopped".
                      format(repository))


def build(tag="latest"):
    local(actions["build"].replace("TAG", tag))


def push(tag="latest"):
    local(actions["push"].replace("TAG", tag))


def create_network():
    with settings(warn_only=True):
        local(actions["create_network"])


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


def deploy(tag="latest"):
    build(tag)
    push(tag)
    with settings(warn_only=True):
        run(actions["stop"])
        run(actions["create_network"])
    run(actions["start"].replace("TAG", tag))
