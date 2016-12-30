#-*- coding: utf-8 -*-

import os
import subprocess
import re

def kill_ports(ports):
    for port in ports:
        print('kill %s start' % port)
        popen = subprocess.Popen('lsof -i:%s' % port, shell = True, stdout=subprocess.PIPE)
        (data, err) = popen.communicate()
        print('data:\n%s  \nerr:\n%s' % (data, err))

        pattern = re.compile(r'\b\d+\b', re.S)
        pids = re.findall(pattern, data)

        print('pids:%s' % str(pids))

        for pid in pids:
            if pid != '' and pid != None:
                try:
                    print('pid:%s' % pid)
                    popen = subprocess.Popen('kill -9 %s' % pid, shell = True, stdout = subprocess.PIPE)
                    (data, err) = popen.communicate()
                    print('data:\n%s  \nerr:\n%s' % (data, err))
                except Exception, e:
                    print('kill_ports exception:%s' % e)

        print('kill %s finish' % port)


if __name__ == '__main__':
    ports = ['8000']
    kill_ports(ports)

# COMMAND  PID USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
# Python  2669  lgq    5u  IPv4 0x409ad167683e57e5      0t0  TCP *:irdmi (LISTEN)
