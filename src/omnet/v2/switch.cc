#include <iostream>
#include <omnetpp.h>

using namespace omnetpp;

class AggSwitch: public cSimpleModule {
};

class EdgeSwitch: public cSimpleModule {
};

class CoreSwitch: public cSimpleModule {
};


Define_Module(AggSwitch);
Define_Module(EdgeSwitch);
Define_Module(CoreSwitch);
