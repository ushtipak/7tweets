docker_repository = "ushtipak/7tweets"
app_name = docker_repository.split("/")[1]
app_port = 2500
app_server = "professor-chaos"
docker_network = "st_network"
postgres_version = "9.6.2"
postgres_storage = "/opt/postgres-data"
db_host = "st_db"
db_port = 5432
db_user = "st_user"
db_name = "tweets"
db_pass = "st_pass"

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
                     docker_repository]
