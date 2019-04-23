#include <iostream>
#include <omnetpp.h>

using namespace omnetpp;

class Server : public cSimpleModule {
};
class Endpoint : public cSimpleModule {
};
class User : public cSimpleModule {
};
Define_Module(Server);
Define_Module(Endpoint);
Define_Module(User);
