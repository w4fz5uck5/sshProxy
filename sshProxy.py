import os, base64, argparse,sys

class xpl():
	def __init__(self, remote_host_name,remote_host_addr,remote_host_port,local_proxy_addr,local_proxy_port):
		self.remote_host_name = remote_host_name
		self.remote_host_port = remote_host_port
		self.remote_host_addr = remote_host_addr
		self.local_proxy_port = local_proxy_port
		self.local_proxy_addr = local_proxy_addr

	def main(self): #create a file containing the configuration in $HOME/.ssh/config
		payload = """host {0}
 HostName {1}
 ProxyCommand proxytunnel -v -p {2}:{3} -d {1}:{4}
 Port {4}
 ServerAliveInterval 999999\n""".format(self.remote_host_name, self.remote_host_addr, self.local_proxy_addr, self.local_proxy_port, self.remote_host_port)
		encoded =  base64.b64encode(payload)
		os.system("echo {0} | base64 -d  >> $HOME/.ssh/config".format(encoded)) 
		print "[+] Configuration successfully added"
		print "\n[+] Now you can do something like: ssh root@{0}".format(self.remote_host_name)
		
parser = argparse.ArgumentParser(description='SSH Proxy connector')
parser.add_argument('-lhost', help='Local proxy ip')
parser.add_argument('-lport', default=8080, help='Local proxy port, Default(8080).')
parser.add_argument('-rname', default="server_dummy", help='Target name, i.e: ssh root@server_dummy (Default: server_dummy)')    
parser.add_argument('-rhost', help='Target ip to connect through proxy')
parser.add_argument('-rport', default=22, help='Target port',)
args = parser.parse_args()
if len(sys.argv) == 1:
    sys.exit(0)
c = xpl(args.rname, args.rhost, args.rport, args.lhost, args.lport)
c.main()
