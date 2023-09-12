
import wingapi


_ignore_scripts = True


#--------------------------------------------------------------------------------
def get_Active_Editor():
	""""""
	return wingapi.gApplication.GetActiveEditor()

#--------------------------------------------------------------------------------
def get_Active_Document():
	""""""
	return wingapi.gApplication.GetActiveDocument()

#--------------------------------------------------------------------------------
def get_Active_Document_Text():
	""""""
	doc = get_Active_Document()
	return doc.GetText() if doc != None else ""

#--------------------------------------------------------------------------------
def get_Selection():
	""""""
	editor = get_Active_Editor()
	return editor.GetSelection() if editor != None else None

#--------------------------------------------------------------------------------
def get_Selection_Text():
	""""""
	txt = ""
	
	editor = get_Active_Editor()
	
	if editor != None:
		start,end = editor.GetSelection()
		txt = editor.GetDocument().GetCharRange(start, end)
	return txt

#--------------------------------------------------------------------------------
def get_Get_Selection_Or_Document_Text():
	""""""
	txt = get_Selection_Text()
	if txt == "":
		txt = get_Active_Document_Text()
	return txt
	