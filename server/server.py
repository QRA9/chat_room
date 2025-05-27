import socket
import threading
import time

host = '192.168.3.110'
prot = 2024

# 存储所有已连接的客户端,key是客户端的标识符，value是套接字
clients = {}
all_id = []
clients_lock = threading.Lock()  # 锁，用于线程安全地访问clients列表
def tcplink_recv(client_socket, address):
    global clients
    global all_id
    client_id = None
    try:
        #接收客户端的标识符
        client_id = client_socket.recv(1024).decode('utf-8')
        print(f"连接到一个客户端，发送来的标识符为：{client_id}")
        #客户端存入字典
        with clients_lock:
            clients[client_id] = client_socket
            all_id.append(client_id)
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    print(f"客户端{client_id}断开连接")
                    break
                # client_socket.send(data)
                print(f"接收到来自{client_id}的消息:{data}")
                message = client_id + ": " + data + '\n'
                for i in clients.values():
                    i.send(message.encode('utf-8'))
            except Exception as e:
                print(f"客户端{client_id}在中途异常断开连接:{e}")
                break
    except Exception as e:
        print(f"客户端{client_id}在发送标识连接时异常断开连接:{e}")
    #客户端断开连接，在字典中移除
    with clients_lock:
        if client_id and client_id in clients:
            del clients[client_id]
            all_id.remove(client_id)
    client_socket.close()


def tcplink():
    global  clients
    global all_id
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, prot))
    server_socket.listen(10)
    print("等待客户端连接...")
    while True:
        try:
            client_socket, address = server_socket.accept()
            print(f"连接来自{address}")
            #为客户端独立分配线程处理数据
            t = threading.Thread(target=tcplink_recv, args=(client_socket, address))
            t.start()
        except ConnectionResetError:
            print(f"客户端{address}异常断开连接")
            continue
        except KeyboardInterrupt:
            print("服务器关闭")
            break
    server_socket.close()
    print(f"客户端对象{address}关闭")


if __name__ == '__main__':
    t = threading.Thread(target=tcplink)
    t.start()
