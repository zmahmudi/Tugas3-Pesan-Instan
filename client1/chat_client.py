import socket
import threading
import sys
import os
import time

def read_msg(sock_cli):
    while True:
        #terima pesan
        data = sock_cli.recv(65535).decode()
        if len(data)==0:
            break
        if '|' in data:
            sender, filename, filesize = data.split("|")
            print(sender + filename + filesize)

            total = 0
            with open(filename, 'wb') as file:
                while True:
                    if total >= int(filesize):
                        break
                        file.close()
                    print("receiving")
                    data = sock_cli.recv(65535)
                    total = total + len(data)
                    file.write(data)
            print("<" + str(sender) + "> " + filename + " received")
        else:
            print(data)

#buat object socket
sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect ke server
sock_cli.connect(("127.0.0.1",6666))

#kirim username ke server
sock_cli.send(bytes(sys.argv[1], "utf-8"))

#buat thread untuk membaca pesan dan jalankan threadnya
thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
thread_cli.start()

while True:
    #kirim / terima pesan
    print ("Untuk mengirim pesan ke username tertentu, ketik \"username\"")
    print ("Untuk mengirim pesan ke semua, ketik \"bcast\"")
    print ("Untuk menambahkan teman, ketik \"addFriend\"")
    print ("Untuk mengirim pesan ke teman, ketik \"sendFriend\"")
    print ("Untuk mengirim file ke orang lain, ketik \"file\"")
    dest = input()

    if dest == "addFriend" :
        msg = input("Masukkan username yang ingin anda jadikan teman: ")
    
    elif dest == "file" :
        msg = input("Masukkan username tujuan : ")
        filename = input("Masukkan file yang dikirim: ")
        filesize = os.path.getsize(filename)
        sock_cli.send(bytes("{}|{}|{}".format(msg, filename, filesize), "utf-8"))
        time.sleep(0.5)

        with open(filename, "rb") as file:
            while True:
                data = file.read(65535)

                if not data:
                    break

                print("Sending")
                sock_cli.sendall(data)
                print(data)
            print("File telah terkirim\n")

    elif dest == "exit":
        sock_cli.close()
        break
    
    else:
        msg = input("Masukkan pesan anda: ")

    
    sock_cli.send(bytes("{}|{}".format(dest,msg), "utf-8"))