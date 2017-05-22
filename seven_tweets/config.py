import os


auth_token = os.getenv("ST_AUTH", "st_auth")
db_host = os.getenv("ST_DB", "st_db")
db_user = os.getenv("ST_USER", "st_user")
db_pass = os.getenv("ST_PASS", "st_pass")
db_port = 5432
docker_network = "st_network"
docker_repository = "ushtipak/7tweets"
app_name = docker_repository.split("/")[1]
app_port = 2500
app_server = "professor-chaos"
postgres_version = "9.6.2"
postgres_storage = "/opt/postgres-data"

DB_CONFIG = dict(user=db_user,
                 host=db_host,
                 port=db_port,
                 password=db_pass)
DOCKER_DB_CONFIG = [db_host,
                    docker_network,
                    db_user,
                    db_pass,
                    postgres_storage,
                    db_port,
                    db_port,
                    postgres_version]
DOCKER_APP_CONFIG = [app_name,
                     docker_network,
                     app_port,
                     app_port,
                     auth_token,
                     docker_repository]
