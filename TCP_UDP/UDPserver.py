import socket
if __name__ == '__main__':

    ip="127.0.0.1"
    port=5000
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((ip,port))

    print("Start server")
    while True:
        data,addr = server.recvfrom(1024)
        data=data.decode('utf-8')

        if data=="Exit":
            print("client disconnected...")
            server.close()
            break 

        print(f'client :'+data)

        data = data.upper()
        data = data.encode('utf-8')
        server.sendto(data,addr)    
    
        

        