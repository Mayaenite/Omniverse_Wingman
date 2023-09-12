
import os
import importlib
import wingapi
if not os.path.dirname(__file__) in os.sys.path:
	os.sys.path.append(os.path.dirname(__file__))
	
import wing_to_omni_connections
import DML_Utils
import os
import wingapi
importlib.reload(DML_Utils)
#--------------------------------------------------------------------------------
def send_code_to_omniverse():
	"""Sends The Currently Active Document Text"""
	code = DML_Utils.get_Active_Document_Text()
	wing_to_omni_connections.connect_To_Omniverse(code)
	
#--------------------------------------------------------------------------------
def send_selected_to_omniverse():
	"""Sends The Currently Hilighted Code"""
	code = DML_Utils.get_Selection_Text()
	wing_to_omni_connections.connect_To_Omniverse(code)

send_code_to_omniverse.contexts = [wingapi.kContextNewMenu("Omniverse"),wingapi.kContextEditor()]
send_selected_to_omniverse.contexts = [wingapi.kContextNewMenu("Omniverse"),wingapi.kContextEditor()]
