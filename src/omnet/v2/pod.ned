import ned.DatarateChannel;
import ned.IdealChannel;

module Pod {
    parameters:
        int k;
    gates:
        inout port[k];
    submodules:
        agg[k>>1] : AggSwitch;
        edge[k>>1] : EdgeSwitch;
    connections allowunconnected:
        for i = 0..(k>>1)-1, for j = 0..(k>>1)-1 {
            agg[i].port++ <--> edge[j].port++;
        }
        for i = 0..(k>>1)-1 {
            agg[i].port++ <--> port++;
        }
}
