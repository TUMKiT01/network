import socket
def main() :
    ip = "127.0.0.1"
    port=1234
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((ip,port))
    data = input("ป้อนข้อความ  : ")
    while data!='q':
        server.send(data.encode('utf-8'))
        data = server.recv(1024).decode('utf-8')
        print("Data from server : "+data)
        data= input("ป้อนข้อความ :")
    server.close()
if __name__ == '__main__': 
    main()