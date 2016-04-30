# Project NS-3

This directory stores the code and report for the projce NS-3.

To run the program, firstly put the `MyWifi.cc` file in the `ns-allinone-3.24.1/ns-3.24.1/scratch` directory and the `wn.sh` script in the `ns-allinone-3.24.1/ns-3.24.1 directory`. 

Then run the `wn.sh` script. Follow the instruction and enter the parameter to spicify a scenario.

#####e.g.

- Default Run (true/false)? - choose to run the default setting or not.
- Number of stations -  set the number of stations/nodes
- Number of simulation times - set the number of simulation times you want in order to generate the average result of the scenario
- DataRate - choose the data rate from 1Mbps, 2Mbps, 5.5Mbps and 11Mbps
- Control Algorithm - choose the rate control algorithm from Constant Rate control algorithm, Idea Rate control algorithm, AARF Rate contorl algorithm, AARF-CD Rate control algorithm, and AMRR Rate control algorithm
- Distance - set the distance between stations and AP, ranged 1 to 1000
