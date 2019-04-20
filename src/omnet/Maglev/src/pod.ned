//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

package maglev;

import inet.node.ethernet.Eth10G;
import inet.node.ethernet.Eth100G;
import ned.IdealChannel;

module Pod
{
    parameters:
        int k;
    gates:
        inout uplink[(k>>1)^2];
        inout downlink[(k>>1)^2];
    submodules:
        agg[k>>1] : AggSwitch;
        edge[k>>1] : EdgeSwitch;
    connections allowunconnected:
        for i=0..(k>>1)-1, for j=0..(k>>1)-1 {
        	agg[i].ethg++ <--> Eth10G <--> edge[j].ethg++;
        	agg[i].ethg++ <--> IdealChannel <--> uplink++;
        	edge[i].ethg++ <--> IdealChannel <--> downlink++;
        }
}
