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
        int simpleHash(int a, int x, int b, int prime) const;
        int hash1(int x) const;
        int hash2(int x) const;
        void permuteBackend(int backend_id);
        void permuteBackends(bool debug=false);
        void populateHash(bool debug=false);
        void printPermutations() const;
        void printHash() const;
        /* Performs maglev lookup. */
        void maglevHash();
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
    /* Lookup is a _num_entry length array that reserves equal number
     * of table entries for backends. */
    _lookup = std::vector<int>(_num_entries, -1);

    initializeMaglev();
    return;
}

int MaglevBalancer::simpleHash(int a, int x, int b, int prime) const {
    return (a * x + b) % prime;
}

int MaglevBalancer::hash1(int x) const {
    // TODO use an actual hash function.
    return simpleHash(5, abs(x), 9, 211);
}

int MaglevBalancer::hash2(int x) const {
    // TODO use an actual hash function.
    return simpleHash(12, abs(x), 2, 379);
}

void MaglevBalancer::permuteBackend(int backend_id) {
    _permutations[backend_id] = std::vector<int>(_num_entries, -1);

    int offset = hash1(backend_id) % _num_entries;
    int skip = (hash2(backend_id) % (_num_entries - 1)) + 1;

    for (int j = 0; j < _num_entries; j++) {
        _permutations[backend_id][j] = simpleHash(skip, j, offset, _num_entries);
    }
    return;
}

void MaglevBalancer::permuteBackends(bool debug) {
    for (int i = 0; i < _num_endpoints; i++) {
        permuteBackend(i);
    }

    if (debug) printPermutations();
    return;
}


void MaglevBalancer::populateHash(bool debug) {
    /* The number of lookup table entries taken so far. */
    int num_taken = 0;
    /* Keep track of the next lookup index that the endpoint wants. */
    std::vector<int> next(_num_endpoints, 0);

    while (true) {
        for (int i = 0; i < _num_endpoints; i++) {
            /* The next lookup index backend 'i' wants. */
            int want = _permutations[i][next[i]];

            /* Lookup index is taken. */
            while (_lookup[want] >= 0) {
                want = _permutations[i][++next[i]];
            }

            /* Found a free index. Lookup table hashes to endpoint. */
            _lookup[want] = i;
            next[i]++;
            num_taken++;
            if (debug) std::cout << i << " chose " << want << std::endl;

            /* Lookup table is full. */
            if (num_taken == _num_entries) {
                if (debug) printHash();
                return;
            }
        }
    }
    return;
}

/*===================================================================*/
void MaglevBalancer::printPermutations() const {
    for (int i = 0; i < _num_endpoints; i++) {
        std::cout << "backend " << i << ": [";
        for (int j = 0; j < _num_entries-1; j++) {
            std::cout << _permutations[i][j] << ", ";
        }
        std::cout << _permutations[i][_num_entries-1] << "]" << std::endl;
    }
    return;
}

void MaglevBalancer::printHash() const {
    std::cout << "Lookup table: [";
    for (int i = 0; i < _num_entries-1; i++) {
        std::cout << _lookup[i] << ", ";
    }
    std::cout << _lookup[_num_entries-1] << "]" << std::endl;
    return;
}

/*===================================================================*/

void MaglevBalancer::initializeMaglev() {
    permuteBackends(true);
    populateHash(true);
    return;
}

void MaglevBalancer::maglevHash() {
    //TODO create a connection tracking table
    //TODO if hash is in the connection tracking table, send it to that one
    //TODO if hash is not in connection tracking table, use maglev hashing
    // and then add it to the connection tracking table
    cMessage *job = new cMessage("job");
    send(job, "out", _lookup[rand() % _num_entries]);
    scheduleAt(simTime() + 1, _send_msg_event);
    return;
}

void MaglevBalancer::handleMessage(cMessage *msg) {
    maglevHash();
    return;
}
