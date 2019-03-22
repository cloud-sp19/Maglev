#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class MaglevBalancer : public cSimpleModule {
    protected:
        /* Number of endpoints that the load balancer is connected to. */
        int _num_endpoints;
        /* Number of entries for the Maglev lookup table. */
        int _num_entries;

        /* Permutation array, the values that each backend wants. */
        std::vector<std::vector<int>> _permutations;
        /* Lookup table. */
        std::vector<int> _lookup;

        /* Event that is run to send a message. */
        cMessage* _send_msg_event;

        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;

        /* Initializes Maglev hash table. */
        void initializeMaglev();
        int hash1(int x) const;
        int hash2(int x) const;
        void permuteBackend(int backend_id);
        void permuteBackends(bool debug=false);
        void populateHash(bool debug=false);
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

    /* Permutations array is an array that holds each endpoints'
     * desired table indices. */
    _permutations = std::vector<std::vector<int>>(_num_endpoints);

    initializeMaglev();
}

int MaglevBalancer::hash1(int x) const {
    // TODO assert that x is not negative.
    // TODO use an actual hash function.
    int simple_a = 5;
    int simple_b = 9;
    int simple_prime = 211;
    return (simple_a * x + simple_b) % simple_prime;
}

int MaglevBalancer::hash2(int x) const {
    // TODO assert that x is not negative.
    // TODO use an actual hash function.
    int simple_a = 12;
    int simple_b = 2;
    int simple_prime = 379;
    return (simple_a * x + simple_b) % simple_prime;
}

void MaglevBalancer::permuteBackend(int backend_id) {
    _permutations[backend_id] = std::vector<int>(_num_entries, -1);

    int offset = hash1(backend_id) % _num_entries;
    int skip = (hash2(backend_id) % (_num_entries - 1)) + 1;

    for (int j = 0; j < _num_entries; j++) {
        _permutations[backend_id][j] = (skip * j + offset) % _num_entries;
    }
}

void MaglevBalancer::permuteBackends(bool debug) {
    for (int i = 0; i < _num_endpoints; i++) {
        permuteBackend(i);
    }

    if (debug) {
        for (int i = 0; i < _num_endpoints; i++) {
            std::cout << "backend " << i << ": [";
            for (int j = 0; j < _num_entries-1; j++) {
                std::cout << _permutations[i][j] << ", ";
            }
            std::cout << _permutations[i][_num_endpoints-1] << "]" << std::endl;
        }
    }
}

void MaglevBalancer::populateHash(bool debug) {

}

void MaglevBalancer::handleMessage(cMessage *msg) {
    maglevHash();
}

/*===================================================================*/

void MaglevBalancer::initializeMaglev() {
    permuteBackends(true);
    populateHash();
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
