network MaglevTopo {
    parameters:
        int k;

    submodules:
        core[(k>>1)*(k>>1)] : CoreSwitch;
        pod[k] : Pod {
            k = k;
        }
        server[(k*k*k)>>2] : Server;

    connections allowunconnected:
        for i = 0..(k>>1)*(k>>1)-1, for j = 0..k-1 {
            core[i].port++ <--> pod[j].port++;
        }
        for i = 0..k-1, for j = 0..(k>>1)*(k>>1)-1 {
          pod[i].port++ <--> server[i*(k>>1)*(k>>1) + j].port;
        }
}
