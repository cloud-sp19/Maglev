#include <stdlib.h>
#include <omnetpp.h>

using namespace omnetpp;

class MaglevBalancer : public cSimpleModule {
    protected:
        /* Number of endpoints that the load balancer is connected to. */
        int _num_endpoints;
        /* Number of entries for the Maglev lookup table. */
        int _num_entries;

        /* Event that is run to send a message. */
        cMessage* _send_msg_event;

        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;

        /* Initializes Maglev hash table. */
        void initializeMaglev(int num_endpoints, int table_size);
        /* Performs maglev lookup. */
        void maglevHash();

        // TODO Move this somewhere else, some other object.
        /* Initialization for ECMP. Sets seed to represent randomly
         * hashed packets. */
        void initializeECMP();
        /* Runs ECMP. */
        void ECMP();
};

Define_Module(MaglevBalancer);

/*===================================================================*/
void MaglevBalancer::initialize() {

    /* Kickoff message. */
    _send_msg_event = new cMessage("_send_msg_event");
    scheduleAt(simTime(), _send_msg_event);

    /* Get parameters from network.ned. */
    _num_endpoints = getParentModule()->par("num_endpoints");
    _num_entries = par("num_entries");
    initializeMaglev(_num_endpoints, _num_entries);
}

void MaglevBalancer::handleMessage(cMessage *msg) {
    maglevHash();
}

/*===================================================================*/

void MaglevBalancer::initializeMaglev(int num_endpoints, int table_size) {
}

void MaglevBalancer::maglevHash() {
}

/*===================================================================*/

void MaglevBalancer::initializeECMP() {
    /* Set seed to represent randomly hashed packets. */
    int seed = 1;
    srand(seed);
}

void MaglevBalancer::ECMP() {
    cMessage *job = new cMessage("job");
    
    send(job, "out", rand() % _num_endpoints);

    scheduleAt(simTime() + 1, _send_msg_event);

}
