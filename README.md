# Omnet installation

## Google Cloud
### Create a VM instance
* Open navbar, hover over compute engine, then click VM instances
* Generate ssh key: `ssh-keygen -t rsa -f ~/.ssh/gcp -C <username>`, https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys
* Add ssh public key (`~/.ssh/gcp`) to compute engine metadata, https://console.cloud.google.com/compute/metadata/sshKeys
* Ssh into instance: `ssh -X <username>@<external vm ip>  -i ~/.ssh/gcp.pub`

### Installing omnetpp
```
curl -o omnetpp-5.4.1-src-linux.tgz https://ipfs.omnetpp.org/release/5.4.1/omnetpp-5.4.1-src-linux.tgz
tar -xf omnetpp-5.4.1-src-linux.tgz
cd omnetpp-5.4.1
. setenv
./configure
make
```
Config may tell you to install some dependencies. To start running it, run `omnetpp` from the omnetpp root directory.

### Installing inet
Starting from the omnet root directory, https://github.com/inet-framework/inet/blob/master/INSTALL,
```
cd samples
git clone https://github.com/inet-framework/inet.git
cd inet
make makefiles
make
cd ..
omnetpp
```
From omnetpp, choose a project. Go into project>properties, and click on project references. Make sure that the window name is properties for inet4, or else add a reference to inet.

Now, you can run your program by clicking the green play button.


https://medium.com/google-cloud/graphical-user-interface-gui-for-google-compute-engine-instance-78fccda09e5c
```
ssh -L 5901:localhost:5901  tonydmyang@35.245.202.233 -i ~/.ssh/gcp
```
