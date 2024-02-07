from ._anvil_designer import signin_signupTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

class signin_signup(signin_signupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def button_login_click(self, **event_args):
    # Tente autenticar o usuário
    if anvil.users.login_with_form():
      # Se o login for bem-sucedido, redirecione para Form2
      anvil.open_form('Form1')


