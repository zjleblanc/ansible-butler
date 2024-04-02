import requests
from requests.auth import HTTPBasicAuth
import os
import sys

CONFIG_HOST_KEY = "controller_host"
CONFIG_USERNAME_KEY = "controller_username"
CONFIG_PASSWORD_KEY = "controller_password"
CONFIG_TOKEN_KEY = "controller_token"

ENV_HOST_KEY = "CONTROLLER_HOST"
ENV_USERNAME_KEY = "CONTROLLER_USERNAME"
ENV_PASSWORD_KEY = "CONTROLLER_PASSWORD"
ENV_TOKEN_KEY = "CONTROLLER_OAUTH_TOKEN"
ENV_TOKEN_KEY_ALT = "CONTROLLER_TOKEN"

class ControllerAuth():
  def __init__(self, host=None, username=None, password=None, token=None, verify_ssl=True):
    self.host = host
    self.username = username
    self.password = password
    self.token = token
    self.verify_ssl = verify_ssl

  def default_headers(self) -> dict:
    return {
      "Authorization": "Bearer " + self.token,
      "Content-Type": "application/json"
    }

def get_controller_token(auth: ControllerAuth) -> str:
  resp = requests.post(f"https://{auth.host}/api/v2/tokens/", auth=HTTPBasicAuth(auth.username, auth.password), verify=auth.verify_ssl)
  if resp.status_code not in [200, 201]:
    print(f"[auth] Failed to generate auth token for host {auth.host} and user {auth.username}\n{resp.content}")
    sys.exit(1)
  return resp.json()['token']

def get_controller_auth(config: dict) -> ControllerAuth:
  auth = ControllerAuth(verify_ssl=config.get('verify_ssl', True))
  auth.host = config.get(CONFIG_HOST_KEY)
  auth.token = config.get(CONFIG_TOKEN_KEY)
  # Token in config
  if auth.host and auth.token:
    return auth
  # Username and password in config 
  auth.username = config.get(CONFIG_USERNAME_KEY)
  auth.password = config.get(CONFIG_PASSWORD_KEY)
  if auth.host and auth.username and auth.password:
    auth.token = get_controller_token(auth)
    return auth
  
  auth.host = os.environ.get(ENV_HOST_KEY)
  auth.token = os.environ.get(ENV_TOKEN_KEY, os.environ.get(ENV_TOKEN_KEY_ALT))
  # Token in environment
  if auth.host and auth.token:
    return auth
  # Username and password in environment 
  auth.username = os.environ.get(ENV_USERNAME_KEY)
  auth.password = os.environ.get(ENV_PASSWORD_KEY)
  if auth.host and auth.username and auth.password:
    auth.token = get_controller_token(auth)
    return auth
  
  # Exhausted auth sources
  print("[auth] Did not find authentication details in config or environment, please review the README for usage instructions")
  sys.exit(1)