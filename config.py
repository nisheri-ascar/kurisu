import os
import dotenv
from styling import *


dotenv.load_dotenv()

COMMAND_PREFIX = ".katagari"
PRIV_TOKEN = str(os.getenv("TOKEN"))
HOSTED_LINK = str(os.getenv("HOSTED_LINK"))
MC_IP_ADDR = str(os.getenv("MC_IP_ADDR"))
HTTP_PORT = 8080 # FIXME: use envvar
DRY_RUN = bool(os.getenv("DRY_RUN"))
DRY_RUN = False
PRODUCTION_MODE=str(os.getenv("PRODUCTION_MODE"))
GUILD_ID = [1529471469464191057, 1532949516171608236]

try:
    file_commit = open("/version", 'r')
    commit = file_commit.read()
except FileNotFoundError as err:
    print("can't find commit.")
    commit = "???"

subtext_notes = [f"{st}dev commit: `{commit}`"]

if PRODUCTION_MODE != True:
    subtext_notes.append(f"{st} `PRODUCTION_MODE` is not set. This instance of kurisu is running locally.")
if DRY_RUN == True:
    subtext_notes.append(f"{st} `DRY_RUN` is set to True. Waiting time will be skipped and script will not be executed.")

if DRY_RUN == True or DRY_RUN == 1:
    BASE_TIME_WAIT = 0
else:
    BASE_TIME_WAIT=30
httpd = None



