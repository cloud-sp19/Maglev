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

package Maglev.simulations;

import Maglev.Server;
import Maglev.Endpoint;
import Maglev.User;
import Maglev.Router;
import Maglev.CoreSwitch;
import Maglev.Pod;
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
        int num_endpoints;
    submodules:
        configurator : Ipv4NetworkConfigurator {
    		config = default(xml("<config><interface hosts='**' address='10.x.x.x' netmask='255.x.x.x'/></config>"));   
    	}
        server[(k^3)>>2] : StandardHost {
          @display("p=400,400,r,50");
        }
        core[(k>>1)^2] : CoreSwitch {
          @display("p=300,200,r,100");
        }
        pod[k] : Pod {
            k=k;
            @display("p=400,300,r,100");
        };
        endpoint[num_endpoints] : Endpoint {
          @display("p=600,600,r,100");   
        }
        user : User {
          @display("p=100,100"); 
        }
        router : Router {
            hasTcp=true;
            @display("p=200,100");   
        }
        
    connections allowunconnected:
        for i=0..(k>>1)^2-1 {
            router.ethg++ <--> Eth100G <--> core[i].ethg++;
        }
        for i=0..k-1, for j=0..(k>>1)^2-1 {
            pod[i].uplink++ <--> Eth100G <--> core[j].ethg++;
        	pod[i].downlink++ <--> Eth100G <--> server[i*(k>>1)^2 + j].ethg++;
        }
        for i=0..num_endpoints-1, for j=0..((k^3)>>2)-1 {
            server[j].ethg++ <--> Eth100G <--> endpoint[i].ethg++;
            endpoint[i].ethg++ <--> Eth100G <--> router.ethg++;
        }
        router.ethg++ <--> Eth100G <--> user.ethg++;
}
