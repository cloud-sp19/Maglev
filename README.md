# Omnet installation

### Installing omnetpp
```
curl -o omnetpp-5.4.1-src-linux.tgz https://ipfs.omnetpp.org/release/5.4.1/omnetpp-5.4.1-src-linux.tgz
tar -xf omnetpp-5.4.1-src-linux.tgz
cd omnetpp-5.4.1
. setenv
./configure
make
```
Config may tell you to install some dependencies. If you get an issue with OSG, just follow its instruction to disable it in the configuration file. To start running omnetpp, run `omnetpp` from the omnetpp root directory.

### Installing inet
Download inet from https://inet.omnetpp.org/Download.html, place it anywhere, it does not necessarily need to be in the omnet/samples folder.
```
cd inet4
make makefiles
make
. setenv
```
From omnetpp, choose a project. Go into project>properties, and click on project references. Check off inet. Open inet and run an example to make sure that it's working.

Now, you can run your program by clicking the green play button.


## Run Maglev/Fattree
Add Maglev to your omnet projects
Make sure to add inet as a reference
Set environment by running in the iNET root folder:
$. setenv 

## Other references
https://stackoverflow.com/questions/38392495/how-to-extend-a-simple-module-from-inet
