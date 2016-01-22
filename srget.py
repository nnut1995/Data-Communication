#!/usr/bin/env python
import os
import re
import socket as sk


def mkDownloadRequest(serv, objName):
    return ("GET {o} HTTP/1.1\r\n" + "Host: {s}\r\n\r\n").format(o=objName, s=serv)

def mkDownloadResumeRequest(serv, objName,start,stop):
    return ("GET {o} HTTP/1.1\r\n" + "Host: {s}\r\n"+"Range: bytes={h}-{z}"+"\r\n\r\n").format(o=objName, s=serv, h=start, z= stop)

def get_only_content_length(url):
	if url[:7] == 'http://':
		url = url[7:]
	cut = url.find('/')
	servName = url[:cut]
	objname = url[cut:]
	num = ['0','1','2','3','4','5','6','7','8','9']
	port = 80
	sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
	sock.connect((servName, port))
	request = mkDownloadRequest(servName, objname)
	sock.send(request)
	Header = ''
	while True:  #get header
	    data = sock.recv(1)
	    Header += data
	    if "\r\n\r\n" in Header:
	    	sock.close()
	        break
	length = Header.find("Content-Length")
	content_length = ''
	
	for x in range(100):  # get content length
		if Header[length+x] in num:
			content_length += Header[length+x]
		elif Header[length+x] == "\n":
			break
	return [content_length,len(Header)]

#get_only_content_length('images.clipartpanda.com/lion-clipart-4Tb5XEETg.png')
def Full_Download(filename,url):
	if url[:7] == 'http://':
		url = url[7:]
	cut = url.find('/')
	servName = url[:cut]
	objname = url[cut:]
	num = ['0','1','2','3','4','5','6','7','8','9']
	port = 80
	sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
	sock.connect((servName, port))
	request = mkDownloadRequest(servName, objname)
	sock.send(request)
	Header = ""
	c = 0

	while True:  #get header
	    data = sock.recv(1)
	    Header += data
	    c += len(data)
	    if "\r\n\r\n" in Header:
	        break
	print Header

	length = Header.find("Content-Length")
	content_length = ''
	
	for x in range(100):  # get content length
		if Header[length+x] in num:
			content_length += Header[length+x]
		elif Header[length+x] == "\n":
			break
	print content_length

	if length == "-1": # download without content length
		Collector = ''
		while True:
		    data = sock.recv(1024)
		    file = open(filename,'wb')#.write(data)   # Trying to create a new file or open one
		    file.write(data)
		    file.close()
		    if len(data) == 0:
		        sock.close()
		        break
		file.close()	
	else: #download with content length
		dataSoFar = 0
		Data = ''
		print content_length
		file = open(filename,'wb')
		while dataSoFar < int(content_length):
			data2 = sock.recv(1024000)
			dataSoFar += len(data2)
			print dataSoFar, "*"
			file.write(data2)
		file.close
		print "End"
		sock.close()

#find_content_length('mildnoii.png','images.clipartpanda.com/lion-clipart-4Tb5XEETg.png')	

def resume(argv):
	filename = ""
	url = ""
	try: 
		opts,args = getopt.getopt(argv,"o:","ofile=")
	except getopt.GetoptError:
		sys.exit(2)
	url = argv[-1]
	for opt,arg in opts:
		if opt == '-o':
			filename = arg

	print get_only_content_length(url)
	if os.path.isfile(filename):
		file_onlocal = os.path.getsize(filename)
		file_onlocal = int(file_onlocal)
		content_length = int(get_only_content_length(url)[0])
		add_data = content_length - file_onlocal
		print add_data, 'add_data'
		print content_length, 'content_length'
		print file_onlocal, 'file_onlocal'
		if file_onlocal == content_length:
			print "file is already download"
		else:
			file_onlocal = int(file_onlocal)# + get_only_content_length(url)[1]
			print file_onlocal
			if url[:7] == 'http://':
				url = url[7:]
			cut = url.find('/')
			servName = url[:cut]
			objname = url[cut:]
			Header = ''
			port = 80
			sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
			sock.connect((servName, port))
			dataSoFar = 0
			request2 = mkDownloadResumeRequest(servName,objname,file_onlocal,content_length)
			sock.send(request2)	
			file = open(filename,'a+')
			while True:  #get header
			    data = sock.recv(1)
			    Header += data
			    if "\r\n\r\n" in Header:
			        break
			while dataSoFar < add_data:
			    data2 = sock.recv(1024)
			    file.write(data2)
			    #print "data2",data2
			    dataSoFar += len(data2)
			    print dataSoFar, "*"
			    if len(data2) == 0:
			    	break
			sock.close()
			file.close()	
		print dataSoFar-add_data
		print len(Header), 'Header'
	else:
		Full_Download(filename,url)

if __name__ == '__main__':
	if len(sys.argv) >=4:
		resume(sys.argv[1:])


resume('LionNoii.png','images.clipartpanda.com/lion-clipart-4Tb5XEETg.png')