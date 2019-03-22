network MaglevTopo {
    parameters:
        int num_endpoints;

    submodules:
        loadbalancer : MaglevBalancer;
        endpoints[num_endpoints] : MaglevEndpoint;

    connections:
        for i = 0..num_endpoints-1 {
            loadbalancer.out++ --> endpoints[i].in;
        }
}
