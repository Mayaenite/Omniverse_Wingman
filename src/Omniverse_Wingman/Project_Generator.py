from pathlib import Path
import shutil
import inspect
import re
import os
#-------------------------------------------------------------------------------
def create_init_file(folder:Path):
	""""""
	init_file = folder.joinpath("__init__.py")
	if not init_file.exists():
		init_file.open("w").close()
#-------------------------------------------------------------------------------	
def clone_files(dest:Path,source:Path):

	for source_file in list(source.glob("*.py"))+list(source.glob("*.pyi")):
		dest_file:Path = dest.joinpath(source_file.name)

		if not dest_file.exists():
			shutil.copyfile( str(source_file), str(dest_file) )
#-------------------------------------------------------------------------------
def create_Child_Folder(parent:Path,child:str) -> Path:
	""""""
	child_folder:Path = parent.joinpath(child)

	if not child_folder.exists():
		child_folder.mkdir()

	return child_folder
#-------------------------------------------------------------------------------
def clone_folder_structure(clone_location:Path,scan_location:Path):
	""""""
	if not scan_location.name == "__pycache__":

		clone_folder = create_Child_Folder(clone_location, scan_location.name)

		clone_files(clone_folder, scan_location)

		create_init_file(clone_folder)

		for scan_sub_folder in scan_location.iterdir():
			scan_sub_folder:Path

			if scan_sub_folder.is_dir():
				clone_folder_structure(clone_folder, scan_sub_folder)
#-------------------------------------------------------------------------------
def find_Wing_Project_Folder_Location(ext_project_dir:Path):
	#-------------------------------------------------------------------------------
	def recursive_config_scaner(folder:Path) -> Path:
		
		if folder.name == "config":
			return folder.parent
		else:
			for child_folder in [item for item in list(folder.iterdir()) if item.is_dir()]:
				if not child_folder.name in ["app",".vscode","tools"]:
					return recursive_config_scaner(child_folder)
	#-------------------------------------------------------------------------------
	def recursive_project_name_scaner(folder:Path) -> str:
		
		child_folders = [ child for child in list(folder.iterdir()) if child.is_dir() ]
		
		for child_folder in child_folders:
			if not child_folder.name in ["app",".vscode","tools"]:
				if child_folder.name.count(".") >= 2:
					result = child_folder.name
					return result
				else:
					return recursive_project_name_scaner(child_folder)
	
	wing_project_folder = recursive_config_scaner(ext_project_dir)
	wing_project_name   = recursive_project_name_scaner(ext_project_dir)
	
	return wing_project_folder,wing_project_name.replace(".","_")
#-------------------------------------------------------------------------------
def mod_Template_Project_To_Include_Root_Project_Dir(folder_name:str):
	""""""
	project_file:Path = Path(__file__).parent.joinpath("Template/Omniverse_Project.template")
	
	if project_file.exists():
		
		project_text = project_file.read_text()
		
		result = project_text.replace("REPLACE_ME",folder_name)
		
		return result
	else:
		raise OSError("The Omniverse_Project.template could not be found")
#-------------------------------------------------------------------------------
def Build_Wing_Project_File(ext_project_dir:Path):
	""""""
	
	project_folder,project_name = find_Wing_Project_Folder_Location(ext_project_dir)
	
	new_project_data = mod_Template_Project_To_Include_Root_Project_Dir(project_folder.stem.split(".")[0])
	
	wing_project_file:Path = project_folder.joinpath(project_name+".wpr")
	
	wing_project_file.write_text(new_project_data)
########################################################################
class Custom_Cleanup_Jobs:
	""""""
	#----------------------------------------------------------------------
	def __init__(self,data):
		"""Constructor"""
		self.data = data
	#----------------------------------------------------------------------
	def clean_Carb_Input_File_Enums(self):
		""""""

		file_to_edit = Path(self.data._output_Dir.joinpath("carb\input.pyi"))

		if file_to_edit.exists():
			text         = file_to_edit.read_text()

			expression   = "# value = <"
			subst        = "= None #<"
			result = re.sub(expression, subst, text, 0, re.MULTILINE)

			expression = (
				r"    def __eq__\(self, other: object\) -> bool: ...\n"
				r"    def __getstate__\(self\) -> int: ...\n"
				r"    def __hash__\(self\) -> int: ...\n"
				r"    def __index__\(self\) -> int: ...\n"
				r"    def __init__\(self, value: int\) -> None: ...\n"
				r"    def __int__\(self\) -> int: ...\n"
				r"    def __ne__\(self, other: object\) -> bool: ...\n"
				r"    def __repr__\(self\) -> str: ...\n"
				r"    def __setstate__\(self, state: int\) -> None: ...\n"
				r"    @property\n"
				r"    def name\(self\) -> str:\n"
				r"        \"\"\"\n"
				r"        :type: str\n"
				r"        \"\"\"\n"
				r"    @property\n"
				r"    def value\(self\) -> int:\n"
				r"        \"\"\"\n"
				r"        :type: int\n"
				r"        \"\"\"\n")
			subst        = ""
			result = re.sub(expression, subst, result, 0, re.MULTILINE)

			expression   = r"__members__: dict.+"
			subst        = ""
			result = re.sub(expression, subst, result, 0, re.MULTILINE)

			file_to_edit.write_text(result)
########################################################################
class Omni_Exts_To_Packs_Generator:
	""""""
	#----------------------------------------------------------------------
	def __init__(self,Omni_Ext_dir:str, output_folder:str=None):
		"""Constructor"""
		self._omni_ext_dir      = Path(Omni_Ext_dir)

		self._output_Dir:Path = Path(output_folder) if not output_folder == None else self._omni_ext_dir.joinpath("_auto_compleate_code")

		if not self._output_Dir.exists():
			self._output_Dir.mkdir()

		self._app_dir : Path      = self._omni_ext_dir.joinpath("app")

		self._list_of_scan_dirs   = [self._app_dir.joinpath("extscache"), self._app_dir.joinpath("kit\kernel")]

		self._carb_dir : Path     = self._app_dir.joinpath("kit\kernel\py\carb")

		self._run_Generator()
		self._run_Custom_Cleanups()
	##----------------------------------------------------------------------
	def _run_Custom_Cleanups(self):
		""""""
		cleanups = Custom_Cleanup_Jobs(self)
		for name, method in inspect.getmembers(cleanups):
			if inspect.ismethod(method) and name.startswith("clean_"):
				method()

	#----------------------------------------------------------------------
	def _run_Generator(self):
		""""""
		for scan_folder in self._list_of_scan_dirs:

			for omni_folder in scan_folder.glob("**/omni/"):

				clone_folder_structure(self._output_Dir, omni_folder)

		clone_folder_structure(self._output_Dir, self._carb_dir)

def main():
	ext_project_dir = Path(os.sys.argv[1])
	Omni_Exts_To_Packs_Generator(ext_project_dir)
	Build_Wing_Project_File(ext_project_dir)	

if __name__ == "__main__":
	main()
	