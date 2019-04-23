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

package maglev.simulations;

import maglev.Server;
import maglev.Router;
import maglev.CoreSwitch;
import maglev.Pod;
import inet.node.ethernet.Eth10G;
import inet.node.ethernet.Eth100G;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.inet.StandardHost;
import inet.node.inet.Router;

//
// TODO auto-generates type
//
network Fattree
{
    parameters:
        int k;
    submodules:
        configurator : Ipv4NetworkConfigurator {
    		config = default(xml("<config><interface hosts='**' address='10.x.x.x' netmask='255.x.x.x'/></config>"));   
    	}
        server[(k^3)>>2] : StandardHost;
        core[(k>>1)^2] : CoreSwitch;
        pod[k] : Pod {
            k=k;
        };
        router : Router {
            hasTcp=true;
        }
        
    connections allowunconnected:
        for i=0..(k>>1)^2-1 {
            router.ethg++ <--> Eth100G <--> core[i].ethg++;
        }
        for i=0..k-1, for j=0..(k>>1)^2-1 {
            pod[i].uplink++ <--> Eth100G <--> core[j].ethg++;
        	pod[i].downlink++ <--> Eth100G <--> server[i*(k>>1)^2 + j].ethg++;
        }
        
}
