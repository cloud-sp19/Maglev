import hashlib

class MaglevHash:
    def __init__(self, backends, lookup_size):
        '''
        backends: 1 x N array that contains names of backends
        lookup_size: int containing the desired size of hash table
        '''
        # Number of backends
        self.N = len(backends)
        # Number of entries in the hash. Must be prime.
        self.M = lookup_size

        # Names of backends
        self.name = backends

        # Permutation array which tells you what priority each backend
        # wants a hash.
        self.permutation = []
        self.generate_permutations()

        # Next stores the next index to the permutation array that a backend
        # can consider. Each backend start with their 1st choice at index 0.
        # If the backend is taken, or if it takes one, increment that
        # backend's counter.
        self.next = [0] * self.N
        self.lookup = [-1] * self.M
        self.populate_hash(printing=False)

    def hash1(self, x):
        '''
        1st hash function. Replace this later.
        x: item to hash
        returns: int
        '''
        return int(hashlib.md5(x.encode()).hexdigest(), 16)

    def hash2(self, x):
        '''
        2nd hash function. Replace this later.
        x: item to hash
        returns: int
        '''
        return int(hashlib.sha256(x.encode()).hexdigest(), 16)

    def permute_backend(self, backend_id):
        '''
        Generate permutations for a single backend.
        backend_id: backend name passed to the hash functions
        returns: 1 x M permutation array
        '''
        permutation = [-1] * self.M

        # Generate offset and skip using backend name.
        offset = int(self.hash1(backend_id)) % self.M
        skip = (self.hash2(backend_id) % (self.M-1)) + 1

        # Generate the permutation for a backend.
        for j in range(self.M):
            permutation[j] = (offset + j * skip) % self.M
        return permutation;

    def generate_permutations(self):
        '''
        Generate permutations for all backends.
        '''
        self.permutations = [None] * self.N

        # Create a permutation for each backend.
        for i in range(self.N):
            self.permutations[i] = self.permute_backend(self.name[i])
        return

    def populate_hash(self, printing=False):
        '''
        Populate the lookup table, letting each backend choose their
        desired hashes.
        '''
        num_taken = 0

        # Loop through the backends and let each choose 1 at a time
        # until the lookup table is all filled up.
        while True:
            for i in range(self.N):

                # Look for the first free spot.
                c = self.permutations[i][self.next[i]]
                while self.lookup[c] >= 0:
                    self.next[i] += 1
                    c = self.permutations[i][self.next[i]]

                # Found a free spot, take it.
                self.lookup[c] = i
                self.next[i] += 1
                num_taken += 1
                if printing:
                    print('backend {} chose {}'.format(self.name[i], c))

                # All filled up!
                if num_taken == self.M:
                    return
        return


    def print_permutations(self):
        '''
        Prints the permutation array.
        '''
        for i in range(self.N):
            print(self.name[i], end=': ')
            print(self.permutations[i])
        return

    def print_lookup(self):
        '''
        Prints the lookup table.
        '''
        print('lookup table', end=': ')
        print(self.lookup)

if __name__ == "__main__":
    backends = ['b1', 'b2', 'b3', 'b4']
    prime = 13
    maglev = MaglevHash(backends, prime)
    maglev.print_permutations()
    maglev.print_lookup()
