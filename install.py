#!/usr/bin/python 
import os
import os.path
import fileinput

#######################################################################
def play_book ( pb, inv ):
  "run playbook"
  book = "ansible-playbook " + pb +  " -i " +  inv
  os.system(book)
  return;

def python ( py ):
  "run py script"
  ps = "/usr/bin/python ./" + py
  os.system(ps)
  return;

def docker_run ( dexec ):
  "run docker"
  ds = "/usr/bin/docker run " + dexec
  os.system(ds)
  return;

def copy ( ori, dest ):
   " coping file "
   pw = "cp " + ori + " " + dest
   os.system(pw)
   return;

##########################################################################
# todo = transform DEF
filein="/etc/ansible/ansible.cfg"
fileout="/etc/ansible/ansible.cfg"

f = open(filein,'r')
filedata = f.read()
f.close()

newdata = filedata.replace("#host_key_checking = False","host_key_checking = False")

f = open(fileout,'w')
f.write(newdata)
f.close()
##########################################################################
docker_run("-e LICENSE=accept  -v \"$(pwd)\":/data ibmcom/icp-inception:2.1.0-ee cp -r cluster /data")

copy("/root/.ssh/id_rsa", "/root/cluster/ssh_key")
copy("/root/servers/hosts", "/root/cluster/hosts")
play_book("/root/servers/hosts.yml", "/root/inventory")
play_book("/root/servers/config_prereq.yml", "/root/inventory")

docker_run("-e LICENSE=accept --net=host  -t -v \"$(pwd)/cluster\":/installer/cluster ibmcom/icp-inception:2.1.0-ee install")

