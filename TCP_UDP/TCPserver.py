import socket
def main():
    ip="127.0.0.1"
    port=1234
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    print("waiting client: ")
    client,address=server.accept()
    print("connect fron : "+str(address))
    while True :
        data = client.recv(1024).decode('utf-8') 
        if not data :
            break 
        print("Message From client :"+data)
        data= str(data.upper())
        client.send(data.encode('utf-8'))
    client.close()
if __name__ == '__main__': 
    main()
                      
