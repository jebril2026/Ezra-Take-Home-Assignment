import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CONFIG_JSON = Path(__file__).parent / "config.json"

def get_env():
	return os.getenv("ENV", "staging")

def load_config():
	with open(CONFIG_JSON) as f:
		return json.load(f)

def get_url(key):
	env_override = os.getenv(key)
	if env_override:
		return env_override
	env = get_env()
	config = load_config()
	try:
		return config["environments"][env][key]
	except KeyError:
		raise RuntimeError(f"Missing config for env '{env}', key '{key}'")

MEMBER_URL = get_url("MEMBER_URL")
INTERNAL_HUB_URL = get_url("INTERNAL_HUB_URL")
INTERNAL_HUB_EMAIL = os.getenv("INTERNAL_HUB_EMAIL", "michael.krakovsky+test_interview@functionhealth.com")
INTERNAL_HUB_PASSWORD = os.getenv("INTERNAL_HUB_PASSWORD", "12121212Aa")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
