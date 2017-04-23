#!/usr/bin/python3

from fabric.api import local, run, settings, env

env.user = "root"

repository = "ushtipak/7tweets"
name = "7tweets"
network = "radionica"
port = 2500

actions = dict(build=f"docker build -t {repository}:TAG .",
               push=f"docker push {repository}",
               create_network=f"docker network create {network}",
               start=f"docker run -d --name {name} --net {network}"
                     f" -p {port}:{port} {repository}:TAG",
               stop=f"docker stop {name}; docker rm {name}",
               status=f"docker ps | grep \"{repository}:TAG\" || echo stopped")


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
