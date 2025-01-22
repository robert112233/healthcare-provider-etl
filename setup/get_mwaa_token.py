import subprocess
from store_env_var import store_env_var

def get_mwaa_token():
    response = subprocess.run(['bash', '-c', './setup/create_web_token.sh'],
                            capture_output=True,
                            text=True,
                            check=True)
    MWAA_TOKEN = response.stdout.strip()

    store_env_var("MWAA_TOKEN", MWAA_TOKEN)