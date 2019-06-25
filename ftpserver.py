#!/usr/bin/env python2
# coding: utf-8

import os,socket,threading,time,errno,stat
import traceback

allow_delete = False
local_ip = socket.gethostbyname(socket.gethostname())
local_port = 8888
currdir=os.path.abspath('.')

class FTPserverThread(threading.Thread):
    def __init__(self,(conn,addr)):
        self.conn=conn
        self.addr=addr
        self.basewd=currdir
        self.cwd=self.basewd
        self.rest=False
        self.pasv_mode=False
        threading.Thread.__init__(self)

    def run(self):
        self.conn.send('220 Welcome!\r\n')
        while True:
            cmd=self.conn.recv(256)
            if not cmd: break
            else:
                print 'Recieved:', cmd.strip()
                try:
                    func = getattr(self, cmd[:4].strip().upper())
                    ret = func(cmd)
                    if isinstance(ret, str):
                        print '> ', ret.strip()
                        self.conn.send(ret)
                except Exception,e:
                    print 'ERROR:',e
                    traceback.print_exc()
                    self.conn.send('500 Sorry.\r\n')

    def SYST(self,cmd):
        return '215 UNIX Type: L8\r\n'
    def OPTS(self,cmd):
        if cmd[5:-2].upper()=='UTF8 ON':
            return '200 OK.\r\n'
        else:
            return '451 Sorry.\r\n'
    def USER(self,cmd):
        return '331 OK.\r\n'
    def PASS(self,cmd):
        return '230 OK.\r\n'
        #self.conn.send('530 Incorrect.\r\n')
    def QUIT(self,cmd):
        return '221 Goodbye.\r\n'
    def NOOP(self,cmd):
        return '200 OK.\r\n'
    def TYPE(self,cmd):
        self.mode=cmd[5]
        return '200 Binary mode.\r\n'

    def CDUP(self,cmd):
        if not os.path.samefile(self.cwd,self.basewd):
            #learn from stackoverflow
            self.cwd=os.path.abspath(os.path.join(self.cwd,'..'))
        return '200 OK.\r\n'
    def PWD(self,cmd):
        cwd=os.path.relpath(self.cwd,self.basewd)
        if cwd=='.':
            cwd='/'
        else:
            cwd='/'+cwd
        return ('257 \"%s\"\r\n' % cwd)
    def CWD(self,cmd):
        chwd=cmd[4:-2]
        if chwd=='/':
            newcwd=self.basewd
        elif chwd[0]=='/':
            newcwd=os.path.join(self.basewd,chwd[1:])
        else:
            newcwd=os.path.join(self.cwd,chwd)
        try:
            mode = os.stat(newcwd).st_mode
            if not stat.S_ISDIR(mode):
                return '550 Not a directory.\r\n'
        except OSError as e:
            if e.errno == errno.ENOENT:
                return '550 No such directory.\r\n'
            else:
                raise
        self.cwd = newcwd
        return '250 OK.\r\n'

    def PORT(self,cmd):
        if self.pasv_mode:
            self.servsock.close()
            self.pasv_mode = False
        l=cmd[5:].split(',')
        self.dataAddr='.'.join(l[:4])
        self.dataPort=(int(l[4])<<8)+int(l[5])
        return '200 Get port.\r\n'

    def PASV(self,cmd): # from http://goo.gl/3if2U
        self.pasv_mode = True
        self.servsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.servsock.bind((local_ip,0))
        self.servsock.listen(1)
        ip, port = self.servsock.getsockname()
        print 'open', ip, port
        return ('227 Entering Passive Mode (%s,%u,%u).\r\n' %
                (','.join(ip.split('.')), port>>8&0xFF, port&0xFF))

    def start_datasock(self):
        if self.pasv_mode:
            self.datasock, addr = self.servsock.accept()
            print 'connect:', addr
        else:
            self.datasock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.datasock.connect((self.dataAddr,self.dataPort))

    def stop_datasock(self):
        self.datasock.close()
        if self.pasv_mode:
            self.servsock.close()


    def LIST(self, cmd):
        if len(cmd) > 7:
            path = cmd[5:-2]
            if path[0] != '/':
                path = os.path.join(self.cwd, path)
        else:
            path = self.cwd
        try:
            mode = os.stat(path).st_mode
            if not stat.S_ISDIR(mode):
                return '550 Not a directory.\r\n'
        except OSError as e:
            if e.errno == errno.ENOENT:
                return '550 No such directory.\r\n'
            else:
                raise
        self.conn.send('150 Here comes the directory listing.\r\n')
        print 'list:', path
        self.start_datasock()
        for t in os.listdir(path):
            k=self.toListItem(os.path.join(path,t))
            self.datasock.send(k+'\r\n')
        self.stop_datasock()
        return '226 Directory send OK.\r\n'

    def toListItem(self,fn):
        st=os.stat(fn)
        fullmode='rwxrwxrwx'
        mode=''
        for i in range(9):
            mode+=((st.st_mode>>(8-i))&1) and fullmode[i] or '-'
        d=(os.path.isdir(fn)) and 'd' or '-'
        ftime=time.strftime(' %b %d %H:%M ', time.gmtime(st.st_mtime))
        return d+mode+' 1 user group '+str(st.st_size)+ftime+os.path.basename(fn)

    def MKD(self,cmd):
        dn=os.path.join(self.cwd,cmd[4:-2])
        os.mkdir(dn)
        return '257 Directory created.\r\n'

    def RMD(self,cmd):
        dn=os.path.join(self.cwd,cmd[4:-2])
        if allow_delete:
            os.rmdir(dn)
            return '250 Directory deleted.\r\n'
        else:
            return '450 Not allowed.\r\n'

    def DELE(self,cmd):
        fn=os.path.join(self.cwd,cmd[5:-2])
        if allow_delete:
            os.remove(fn)
            return '250 File deleted.\r\n'
        else:
            return '450 Not allowed.\r\n'

    def RNFR(self,cmd):
        self.rnfn=os.path.join(self.cwd,cmd[5:-2])
        return '350 Ready.\r\n'

    def RNTO(self,cmd):
        fn=os.path.join(self.cwd,cmd[5:-2])
        os.rename(self.rnfn,fn)
        return '250 File renamed.\r\n'

    def REST(self,cmd):
        self.pos=int(cmd[5:-2])
        self.rest=True
        return '250 File position reseted.\r\n'

    def RETR(self,cmd):
        fn=os.path.join(self.cwd,cmd[5:-2])
        #fn=os.path.join(self.cwd,cmd[5:-2]).lstrip('/')
        print 'Downlowding:',fn
        if self.mode=='I':
            fi=open(fn,'rb')
        else:
            fi=open(fn,'r')
        self.conn.send('150 Opening data connection.\r\n')
        if self.rest:
            fi.seek(self.pos)
            self.rest=False
        data= fi.read(1024)
        self.start_datasock()
        while data:
            self.datasock.send(data)
            data=fi.read(1024)
        fi.close()
        self.stop_datasock()
        return '226 Transfer complete.\r\n'

    def STOR(self,cmd):
        fn=os.path.join(self.cwd,cmd[5:-2])
        print 'Uploading:',fn
        if self.mode=='I':
            fo=open(fn,'wb')
        else:
            fo=open(fn,'w')
        self.conn.send('150 Opening data connection.\r\n')
        self.start_datasock()
        while True:
            data=self.datasock.recv(1024)
            if not data: break
            fo.write(data)
        fo.close()
        self.stop_datasock()
        return '226 Transfer complete.\r\n'

class FTPserver(threading.Thread):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((local_ip,local_port))
        threading.Thread.__init__(self)

    def run(self):
        self.sock.listen(5)
        while True:
            th=FTPserverThread(self.sock.accept())
            th.daemon=True
            th.start()

    def stop(self):
        self.sock.close()

if __name__=='__main__':
    ftp=FTPserver()
    ftp.daemon=True
    ftp.start()
    print 'On', local_ip, ':', local_port
    raw_input('Enter to end...\n')
    ftp.stop()
