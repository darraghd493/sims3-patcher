# This is heavily annotated to explain what is happening - this is because the code has some weird behaviour
# If you want to see the code without the comments, see main_min.py

import os, re, time, psutil, winreg, win32com.client, sys
from tkinter.messagebox import askquestion
from tkinter import filedialog

if __name__ != "__main__":
	# This is a small check to prevent this file from being run as a module
	# It's not really necessary, but it's here to prevent it from being run by accident
	print("This is running as a module instead of as a script.\nPlease run main.py instead.\nExiting...")
	sys.exit()

def resolve_lnk(path):
	# This resolves the path of a shortcut
	# https://stackoverflow.com/a/571573
	shell = win32com.client.Dispatch("WScript.Shell")
	shortcut = shell.CreateShortCut(path)
	return shortcut.Targetpath

def header(sub = None):
	# This clears the console
	os.system("cls") # Since the script is Windows only, we can use the cls command without worrying about compatibility
	
	# Print the header
	os.system("title Sims 3 Patcher by darraghd493") # Set the title of the console

	if sub == None:
		print("Sims 3 Pather by darraghd493\n")
	else:
		print("Sims 3 Pather by darraghd493: " + sub + "\n")

def kill_task(name):
	# This kills a task by name
	# /f = force, /im = image name (.exe name)
	os.system("taskkill /f /im " + name + ".exe>nul 2>&1") # nul 2>&1 is used to hide the output of the command

def kill_all_executables(path):
	# Get all executable files in the bin folder
	# 
	# This is done by using os.listdir() to get all files in the folder
	# Then we use os.path.join() to join the folder path with the file name
	# This gives us the full path to the file

	for file in os.listdir(path):
		file_path = os.path.join(path, file)

		# We only want to kill the .exe files
		# This is done by using os.path.splitext() to get the file extension
		# Then we check if the file extension is .exe
		if os.path.splitext(file_path)[1] == ".exe":
			kill_task(os.path.splitext(file)[0])

def get_game_folder():
	# This is a small "hack" to the Sims 3 /bin/ folder
	# 
	# It works since the shortcut is always created on the desktop when installing the game
	# of all users, including the public user (C:\Users\Public\Desktop\The Sims 3.lnk)
	# and therefore if that user exists we can quickly find the game's installation path
	if os.path.isfile("C:\\Users\\Public\\Desktop\\The Sims 3.lnk"):
		exe_file = resolve_lnk("C:\\Users\\Public\\Desktop\\The Sims 3.lnk")
		bin_folder = os.path.dirname(exe_file)

		# We need to go back two folders to get the game's installation path
		# This is because the .exe is located in the bin folder which is /The Sims 3/Game/Bin/ on the disk
		# where as we want the game folder which is /The Sims 3/ on the disk
		# 
		# We can cheat our way around this by going back two folders
		# The first back will bring us to /The Sims 3/Game/
		# The second back will bring us to /The Sims 3/
		# 
		# We can use os.path.dirname() to go back one folder
		
		game_dir = os.path.dirname(bin_folder)
		install_dir = os.path.dirname(game_dir)
		return install_dir
	
	# If the above fails, we can check the registry for the game's installation path
	# This is a bit more complicated, but it should work
	#
	# The registry key is located at:
	# HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Sims\The Sims 3
	# and the value is Install Dir
	#
	# We can use the winreg module to get the value
	# https://docs.python.org/3/library/winreg.html
	try:
		winreg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Sims\\The Sims 3")
		install_dir = winreg.QueryValueEx(winreg_key, "Install Dir")[0]
		winreg_key.Close()
		return install_dir
	except:
		# It is possible that the registry key doesn't exist
		# This can happen if the game isn't installed or not installed correctly
		# In this case, we can open a file dialog to let the user select the game's installation folder
		# 
		# We can use the tkinter module to do this
		# https://docs.python.org/3/library/tkinter.html

		filedialog_path = filedialog.askdirectory(title="Select Sims 3 Installation Folder")

		if filedialog_path == "":
			# If the user cancels the file dialog, we can exit the program
			print("No folder selected. Exiting...")
			sys.exit()

		return filedialog_path
	
def get_bin_folder(path):
	# Since the input is just the game's installation path, we need to add the /Game/Bin/ folder to it
	# This is done by os.path.join()
	return os.path.join(path, "Game", "Bin")

def get_document_folder():
	# This folder (/Documents/Electronic Arts/The Sims 3/) is always located in the user's documents folder
	# 
	# We can use the winreg module to get the user's documents folder
	# https://docs.python.org/3/library/winreg.html
	winreg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders")

	# The value is Personal
	# We can use winreg.QueryValueEx() to get the value
	documents_folder = winreg.QueryValueEx(winreg_key, "Personal")[0]
	winreg_key.Close()

	# We can use os.path.join() to join the documents folder with the rest of the path
	return os.path.join(documents_folder, "Electronic Arts", "The Sims 3")

# Create a warning before continuing
if askquestion("Sims 3 Patcher", "Do you want to run the Sims 3 Patcher?", icon="warning") == "no":
	print("Exiting...")

# This is the main script
# It will be run when the file is run as a script

header("Checking files...")

low = 1
low_medium = 2
medium = 3
high = 4
uber = 5

game_folder = get_game_folder()
bin_folder = get_bin_folder(game_folder)
document_folder = get_document_folder()

print("Installation Folder: " + game_folder)
print("Bin Folder: " + bin_folder)
print("Document Folder: " + document_folder)

# Kill all instances of the game running
kill_all_executables(bin_folder)

# Check if the game has been run before
# by checking for the:
# - DeviceConfig.log file
# - Options.ini file
# - GraphicsCards.sgr file
# - GraphicsRules.sgr file
if not (os.path.isfile(os.path.join(document_folder, "DeviceConfig.log")) and os.path.isfile(os.path.join(document_folder, "Options.ini")) and os.path.isfile(os.path.join(bin_folder, "GraphicsCards.sgr")) and os.path.isfile(os.path.join(bin_folder, "GraphicsRules.sgr"))):
	header()
	print("The game has not been run before. Running the game to generate the required files...")

	# Run the game
	os.system(os.path.join(bin_folder, "TS3W.exe"))

	# Wait for the game to close
	# This is done by checking if the game's executable is running
	# If it is, we wait for 1 second and check again
	# If it isn't, we can continue
	while True:
		if os.path.exists(os.path.join(bin_folder, "TS3W.exe")):
			time.sleep(1)
		else:
			break

# We no longer need to read the DeviceConfig.log file for the GraphicsCards.sgr file
# since we just force the rules to accept our GPU
# 
# Unused regex patterns from reading the DeviceConfig.log file:
# - GPU Rating: GPU:\s+(\d+)

if os.path.isfile(os.path.join(document_folder, "DeviceConfig.log")) and os.path.isfile(os.path.join(bin_folder, "GraphicsCards.sgr")):
	# If the DeviceConfig.log file and GraphicsCards.sgr file exists, we can should read them
	header("Patching GraphicsCards.sgr...")

	# Read the DeviceConfig.log file
	log_content = open(os.path.join(document_folder, "DeviceConfig.log"), "r").read()
	cards_content = open(os.path.join(bin_folder, "GraphicsCards.sgr"), "r").read()

	# Fetch all required information
	gpu_name = re.search(r"Name \(database\): (.+?) \[", log_content).group(1)
	gpu_vendor = re.search(r"Vendor:\s*(\w+)", log_content).group(1)
	gpu_chipset = re.search(r", Chipset:\s*(\w+)", log_content).group(1)
	gpu_chipset_vendor = re.search(r"Chipset:         Vendor:\s*(\w+)", log_content).group(1)

	print("GPU Name: " + gpu_name)
	print("GPU Vendor: " + gpu_vendor)
	print("GPU Chipset: " + gpu_chipset + "\n")
	print("GPU Chipset Vendor: " + gpu_chipset_vendor)

	# Add the GPU to the database
	if cards_content.find("card " + gpu_chipset) == -1:
		print("GPU Chipset not found in GraphicsCards.sgr. Continuing...")
		
		vendor_line = ""
		create_vendor = False
		
		# Decide which vendor line to use
		if gpu_chipset_vendor == "1002":
			print("GPU Vendor is AMD.")
			vendor_line = "vendor \"ATI\" 0x1002"
		elif gpu_chipset_vendor == "10b4" or gpu_chipset_vendor == "12d2" or gpu_chipset_vendor == "10de":
			print("GPU Vendor is NVIDIA.")
			vendor_line = "vendor \"NVIDIA\" 0x10b4 0x12d2 0x10de"
		elif gpu_chipset_vendor == "8086":
			print("GPU Vendor is Intel.")
			vendor_line = "vendor \"Intel\" 0x8086"
		elif gpu_chipset_vendor == "102b":
			print("Your GPU Vendor is Matrox which is not supported (but we'll try).")
			create_vendor = True
		elif gpu_chipset_vendor == "5333":
			print("Your GPU Vendor is S3 which is not supported (but we'll try - even though it isn't by default).")
			vendor_line = "vendor \"S3\" 0x5333"
		else:
			print("GPU Vendor is unknown. Creating custom vendor. (your special :0)")
			create_vendor = True
		
		# Perform the action
		if create_vendor:
			cards_content += f"\n\n# Custom Vendor\nvendor \"{gpu_vendor}\" 0x{gpu_chipset_vendor}\n\tcard 0x{gpu_chipset} \"{gpu_name}\"\nend"
		else:
			start_index = cards_content.find(vendor_line) + len(vendor_line)
			insert_content = f"\n\tcard 0x{gpu_chipset} \"{gpu_name}\""
			cards_content = cards_content[:start_index] + insert_content + cards_content[start_index:]
	else:
		print("GPU Chipset found in GraphicsCards.sgr. Stopping GraphicsCards.sgr patches (already patched/working)...")
	
	# Enforce all GPUs to be recognised
	print("Enforcing all GPUs to be recognised")
	cards_content = cards_content.replace(" unsupported", "")
	
	# Update the GraphicsCards.sgr file
	print("Writing changes to GraphicsCards.sgr")
	open(os.path.join(bin_folder, "GraphicsCards.sgr"), "w").write(cards_content)
	
if os.path.isfile(os.path.join(bin_folder, "GraphicsRules.sgr")):
	# If the GraphicsRules.sgr file exists, we can should read it
	header("Patching GraphicsRules.sgr...")

	# Read the GraphicsRules.sgr file
	log_content = open(os.path.join(bin_folder, "GraphicsRules.sgr"), "r").read()

	# Fetch all required information
	gpu_vram = psutil.virtual_memory().total / 1024 / 1024 # Convert to MB

	# Update the VRAM in the GraphicsRules.sgr file
	print("Updating VRAM limit")
	log_content = log_content.replace("seti textureMemory       32", "seti textureMemory       " + str(gpu_vram))

	# Comment out the textureMemorySizeOK (texture size override) line
	# This is done by adding a # to the start of the line	
	print("Removing VRAM limit")
	log_content = log_content.replace("seti textureMemorySizeOK true", "#seti textureMemorySizeOK true")
	
	# Enforce that the GPU is found
	print("Enforcing the GPU to be matched")
	log_content = log_content.replace("seti isCardMatched false", "seti isCardMatched true")

	# Enforce that middle/lower end CPUs are still rated as high
	print("Enforcing the CPU to be rated as high")
	log_content = log_content.replace("seti cpuLevelMedium     2", "seti cpuLevelMedium     3")
	log_content = log_content.replace("seti cpuLevelMedium     1", "seti cpuLevelMedium     3")

	# Update the GraphicsRules.sgr file
	print("Writing changes to GraphicsRules.sgr")
	open(os.path.join(bin_folder, "GraphicsRules.sgr"), "w").write(log_content)

# Create an alert to let the user know that the patching is complete
askquestion("Sims 3 Patcher", "The Sims 3 has been patched!\nDo you want to run the game?", icon="info")
