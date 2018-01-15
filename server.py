import socket, select

pairs = []
players = []

if "__main__" == __name__:
    socket.setdefaulttimeout(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 1664))
    s.listen(2)
    while 1:
        try:
            (cs, addr) = s.accept()
            players.append(cs)
        except socket.timeout:
            pass
        read, write, err = select.select(players, players, players, 1)
        for player in read:
            data = player.recv(4096)
            i = players.index(player)
            if(i%2 == 0):
                try:
                    players[i+1].send(data)
                except IndexError:
                    pass
            else:
                players[i-1].send(data)
