import subprocess
import sys

def main():
	
	pid1 = subprocess.Popen([sys.executable, "groundstation.py"])
	pid2 = subprocess.Popen([sys.executable, "comm_module.py"])
	pid3 = subprocess.Popen([sys.executable, "tele_module.py"])
	print(pid1)
	print(pid2)
	print(pid3)
	

if __name__ == '__main__':
	main()
