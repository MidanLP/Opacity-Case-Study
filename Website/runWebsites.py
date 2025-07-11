import subprocess
import os


#Backup script for hosting with Python (not recommended, delayed and weird timings, not reality like)
#Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

#Relative paths to scripts
script1 = os.path.join(current_dir, "Case-Study", "Parachute", "para_server.py")
script2 = os.path.join(current_dir, "Case-Study", "Healthcare", "health_server.py")

#Run both scripts in parallel
process1 = subprocess.Popen(["python", script1], shell=True)
process2 = subprocess.Popen(["python", script2], shell=True)

process1.wait()
process2.wait()

print("Both scripts have finished executing.")
