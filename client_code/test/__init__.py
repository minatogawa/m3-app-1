from ._anvil_designer import testTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class test(testTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.server.call('set_reload_flag')

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    # Define a flag para recarregar dados em Form1
    anvil.server.call('set_reload_flag')
    # Abre Form1
    open_form('Form1')