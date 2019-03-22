#include <iostream>
#include <omnetpp.h>

using namespace omnetpp;

class MaglevEndpoint : public cSimpleModule {
    virtual void handleMessage(cMessage *msg) override;
};

Define_Module(MaglevEndpoint);

void MaglevEndpoint::handleMessage(cMessage *msg) {
    /* Act as a sink. */
    delete msg;
}
