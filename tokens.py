import globus_sdk as globus
import json
import os
get_input = getattr(__builtins__, 'raw_input', input)

# Do not change this
CLIENT_ID = '4f0448d6-e7e2-4637-bc64-e8f682d1cc77' # App

# Change this is you want or not.
TOKEN_FILE = os.path.expanduser('~/.wehi-globus-tokens.json')

class WehiGlobusApiHelper:

  def __init__(self):
    if self._tokens_exist():
      self.tokens = self._load()
    else:
      self.tokens = None

  def login(self):
    client = globus.NativeAppAuthClient(CLIENT_ID)
    client.oauth2_start_flow(refresh_tokens=True)

    authorize_url = client.oauth2_get_authorize_url()
    print('Please go to this URL and login: {0}'.format(authorize_url))

    auth_code = get_input('Please enter the code here: ').strip()
    token_response = client.oauth2_exchange_code_for_tokens(auth_code)

    self.tokens = token_response.by_resource_server

    self._save(self.tokens)

  def get_transfer_client(self):
    if self.tokens is None:
      raise Exception('No tokens - please login interactively')

    transfer_tokens = self.tokens['transfer.api.globus.org']

    auth_client = globus.NativeAppAuthClient(client_id=CLIENT_ID)

    authorizer = globus.RefreshTokenAuthorizer(
        transfer_tokens['refresh_token'],
        auth_client,
        access_token=transfer_tokens['access_token'],
        expires_at=transfer_tokens['expires_at_seconds'],
        on_refresh=self._update_tokens)

    tc = globus.TransferClient(authorizer=authorizer)

    return tc

  @staticmethod
  def _update_tokens(token_response):
    """
    Callback function passed into the RefreshTokenAuthorizer.
    Will be invoked any time a new access token is fetched.
    """
    WehiGlobusApiHelper._save(TOKEN_FILE, token_response.by_resource_server)

  @staticmethod
  def _save(tokens):
    """Save a set of tokens for later use."""
    with open(TOKEN_FILE, 'w') as f:
      json.dump(tokens, f)
    os.chmod(TOKEN_FILE, 0o600)


  @staticmethod
  def _tokens_exist():
    return os.path.exists(TOKEN_FILE)

  @staticmethod
  def _load():
    """Load a set of saved tokens."""
    with open(TOKEN_FILE, 'r') as f:
      tokens = json.load(f)
    return tokens