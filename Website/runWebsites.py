import subprocess

# Paths to scripts
script1 = r"C:\Users\nadim\Desktop\Bach\Website\Opacity-Case-Study\Parachute\para_server.py"
script2 = r"C:\Users\nadim\Desktop\Bach\Website\Opacity-Case-Study\Healthcare\health_server.py"

# Run both scripts in parallel
process1 = subprocess.Popen(["python", script1], shell=True)
process2 = subprocess.Popen(["python", script2], shell=True)

process1.wait()
process2.wait()

print("Both scripts have finished executing.")
