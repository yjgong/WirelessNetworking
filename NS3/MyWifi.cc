/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/applications-module.h" 
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"
#include "ns3/ipv4-global-routing-helper.h"   //
#include "ns3/internet-module.h"
#include "ns3/flow-monitor-module.h" 
#include "ns3/random-variable-stream.h"    //
#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace ns3; 
NS_LOG_COMPONENT_DEFINE ("MyWifi");

int 
main (int argc, char *argv[]) 
{
	//int count=1;
	//int mob=0;
	int run=1;
	int nNodes=10;
	int simTimes=3;
	int datarate=3;
	int Distance=100;
	int contr=0;

	std::cout << "Default Run (true:1/false:0)? ";
	std::cin >> run;
	if (!run)
	{
		std::cout << "Number of stations: ";
		std::cin >> nNodes;
		std::cout << "Number of simulation times: ";
		std::cin >> simTimes;
		std::cout << "DataRade (enter 0 for 1Mbps, enter 1 for 2Mbps, enter 2 for 5.5Mbps, enter 3 for 11Mbps):";
		std::cin >> datarate;
		std::cout << "Control Algorithm (enter 0 for ConstantRateWifiManager, enter 1 for IdealWifiManager, enter 2 for AarfWifiManager, enter 3 for AarfcdWifiManager, enter 4 for AmrrWifiManager:";
		std::cin >> contr;
		std::cout << "Distance: ";
		std::cin >> Distance;
	}

  	// Read arguments from command line
  	/*CommandLine cmd;
    cmd.AddValue ("n", "Number of stations", n);
    cmd.AddValue ("d", "Distance", r);
    */

	//int nNodes = 1;
	//while(nNodes <= stations)
	//{
		std::cout << "--------------------------" << "\n";
		std::cout << "Number of nodes: " << nNodes << "\n";

		double total = 0;
		float ratio = 0;
		int pkloss = 0;
		int pksent = 0;
		int pkreceived = 0;
		Time delay = Seconds(0);

		int count = 0;
		while(count<simTimes)   //simulate simtTimes times to get the average values
		{
			double simulationTime = 10.0;
			uint32_t packetSize = 1472;     //max: 
			uint32_t nPacket = 10000; 
			bool verbose = false;

			StringValue phyMode;
			if (datarate==0) phyMode = StringValue("DsssRate1Mbps");
			if (datarate==1) phyMode = StringValue("DsssRate2Mbps");
			if (datarate==2) phyMode = StringValue("DsssRate5_5Mbps");
			if (datarate==3) phyMode = StringValue("DsssRate11Mbps");

			// Create randomness based on time 
			time_t timex;
			time(&timex); 
			RngSeedManager::SetSeed(timex); 
			RngSeedManager::SetRun(10);

			CommandLine cmd; 
			cmd.Parse (argc,argv);

			//-----------------------Create AP & Nodes---------------- 
			NodeContainer ApNode; 
			ApNode.Create (1);

			NodeContainer StaNodes; 
			StaNodes.Create (nNodes); 
			

			//------------------------WifiHelper---------------------- 
			WifiHelper wifi = WifiHelper::Default ();
			if (verbose)
			{
	    		wifi.EnableLogComponents (); // Turn on all Wifi logging
	  		}
			wifi.SetStandard (WIFI_PHY_STANDARD_80211b);

			//---------------------YansWifiPhyHelper---------------------- 
			YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();     //NistErrorRateModel
			phy.Set ("RxGain", DoubleValue (0) );

			//---------------------YansWifiChannelHelper---------------------- 
			YansWifiChannelHelper channel;
			channel.SetPropagationDelay ("ns3::ConstantSpeedPropagationDelayModel"); 
			channel.AddPropagationLoss ("ns3::FriisPropagationLossModel"); 
			phy.SetChannel (channel.Create ());

			//---------------------NqosWifiMacHelper (Control algorithm)---------------------- 
			NqosWifiMacHelper mac = NqosWifiMacHelper::Default ();      // Set to a non-QoS upper mac
			if (contr==0)wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager","DataMode", phyMode, "ControlMode", phyMode);
			if (contr==1)wifi.SetRemoteStationManager ("ns3::IdealWifiManager");
			if (contr==2)wifi.SetRemoteStationManager ("ns3::AarfWifiManager");
			if (contr==3)wifi.SetRemoteStationManager ("ns3::AarfcdWifiManager");
			if (contr==4)wifi.SetRemoteStationManager ("ns3::AmrrWifiManager");
			
			
			//-------------------------------Device---------------------- 
			Ssid ssid = Ssid ("myWifi");
			mac.SetType ("ns3::ApWifiMac", "Ssid", SsidValue (ssid));	
			NetDeviceContainer apDevice = wifi.Install (phy, mac, ApNode);   //apcontainer get(0)
			mac.SetType ("ns3::StaWifiMac","Ssid", SsidValue (ssid), "ActiveProbing", BooleanValue (false));
			NetDeviceContainer staDevices = wifi.Install (phy, mac, StaNodes);


			

			MobilityHelper mobilityAp, mobility;

			Ptr<ListPositionAllocator> positionAllocAp = CreateObject<ListPositionAllocator> ();
			positionAllocAp-> Add (Vector (0.0, 0.0, 0.0));
			mobilityAp.SetPositionAllocator (positionAllocAp);
			mobilityAp.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
			mobilityAp.Install (ApNode);

			if (nNodes==2)
			{
				Ptr<ListPositionAllocator> positionAlloc = CreateObject<ListPositionAllocator> ();
				positionAlloc-> Add (Vector (Distance, 0.0, 0.0));
				mobility.SetPositionAllocator (positionAlloc);
				mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
				mobility.Install (StaNodes);
			}
			
			else
			{
			//int mob = 0;
			//------------------------------Mobility (Constant)---------------------- 
			//if (mob==1)
			//{
				//std::cout << "ConstantPositionMobilityModel" << "\n";
				ObjectFactory pos;
				pos.SetTypeId ("ns3::RandomRectanglePositionAllocator");
				if(Distance>0 && Distance<=100)
				{
					pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=0|Max=100]"));   
					pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=0|Max=100]"));
				}
				else if(Distance>100 && Distance<=200)
				{
					pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=100|Max=200]"));   
					pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=100|Max=200]"));
				}
				else if(Distance>200 && Distance<=300)
				{
					pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=200|Max=300]"));   
					pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=200|Max=300]"));
				}
				else if(Distance>300 && Distance<=400)
				{
					pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=300|Max=400]"));   
					pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=300|Max=400]"));
				}
				else if(Distance>400 && Distance<=500)
				{
					pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=400|Max=500]"));   
					pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=400|Max=500]"));
				}
				else if(Distance>500 && Distance<=600)
				{
					pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=500|Max=600]"));   
					pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=500|Max=600]"));
				}
				else if(Distance>600 && Distance<=700)
				{
					pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=600|Max=700]"));   
					pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=600|Max=700]"));
				}
				else if(Distance>700 && Distance<=800)
				{
					pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=700|Max=800]"));   
					pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=700|Max=800]"));
				}
				else if(Distance>800 && Distance<=900)
				{
					pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=800|Max=900]"));   
					pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=800|Max=900]"));
				}
				else if(Distance>900 && Distance<=1000)
				{
					pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=900|Max=1000]"));   
					pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=900|Max=1000]"));
				}

				Ptr<PositionAllocator> positionAlloc = pos.Create
				()->GetObject<PositionAllocator> ();

				mobility.SetPositionAllocator (positionAlloc);
				mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
				mobility.Install (StaNodes);
			//}
			}

			/*//---------------------------Mobility (Nodes - Walk 2D)---------------------- 
			else if (mob==2)
			{
				//std::cout << "RandomWalk2dMobilityModel" << "\n";
				mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
					"Bounds", RectangleValue (Rectangle (-1000, 1000, -1000, 1000)), 
					"Distance", ns3::DoubleValue (10.0));
				mobility.Install (StaNodes);
			}
			//---------------------------Mobility (Nodes - Constant 3D)---------------------- 
			else if (mob==3)
			{
				std::cout << "ConstantPositionMobilityModel-3D" << "\n";
				ObjectFactory pos;
				pos.SetTypeId ("ns3::RandomBoxPositionAllocator");
				pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=10.0|Max=60.0]"));
				pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=10.0|Max=60.0]"));
				pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=10.0|Max=60.0]"));
				Ptr<PositionAllocator> positionAlloc = pos.Create
				    ()->GetObject<PositionAllocator> ();

				mobility.SetPositionAllocator (positionAlloc);
				mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
				mobility.Install (StaNodes);
			}*/

			//--------------------------Internet stack---------------------- 
			InternetStackHelper internet; 
			internet.Install (ApNode); 
			internet.Install (StaNodes);

			//---------------------Ipv4AddressHelper---------------------- 
			Ipv4AddressHelper address;
			NS_LOG_INFO ("Assign IP Addresses.");
			Ipv4Address addr;
			address.SetBase ("10.1.1.0", "255.255.255.0"); 
			Ipv4InterfaceContainer apNodeInterface = address.Assign (apDevice);
			Ipv4InterfaceContainer staNodesInterface = address.Assign (staDevices); 

			addr = apNodeInterface.GetAddress(0);

			//---------------------Traffic---------------------- 
			UdpServerHelper myServer (9); 

			ApplicationContainer serverApp;
			serverApp = myServer.Install (StaNodes.Get (0));
			serverApp.Start (Seconds(0.0));
			serverApp.Stop (Seconds(simulationTime));

			UdpClientHelper myClient (addr, 9); 
			myClient.SetAttribute ("MaxPackets", UintegerValue (nPacket)); 
			myClient.SetAttribute ("Interval", TimeValue (Time ("0.002"))); //packets/s 
			myClient.SetAttribute ("PacketSize", UintegerValue (packetSize)); 
			ApplicationContainer clientApp = myClient.Install (StaNodes.Get (0)); 
			clientApp.Start (Seconds(0.0));
			clientApp.Stop (Seconds(simulationTime));       


			//---------------------FlowMonitorHelper---------------------- 
			FlowMonitorHelper flowmon;
			Ptr<FlowMonitor> monitor = flowmon.InstallAll();

			NS_LOG_INFO ("Run Simulation");
			Simulator::Stop (Seconds(simulationTime+2)); 
			Simulator::Run ();

			monitor->CheckForLostPackets ();
			Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ()); 
			std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats ();

			double temp_total = 0;
			float temp_ratio = 0;
			int temp_pkloss = 0;
			int temp_pksent = 0;
			int temp_pkreceived = 0;
			Time temp_delay = Seconds(0);

			for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator iter = stats.begin(); iter != stats.end(); ++iter) 
			{
				//Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (iter->first);
				temp_total = iter->second.rxBytes * 8.0 / (iter->second.timeLastRxPacket.GetSeconds() - iter->second.timeFirstTxPacket.GetSeconds())/1024/1024;
				//std::cout << "Flow " << iter->first << " (" << t.sourceAddress << " -> " << t.destinationAddress << ")\n";
				temp_pksent = iter->second.txPackets;
				temp_pkreceived = iter->second.rxPackets;
				temp_pkloss = iter->second.lostPackets;
				temp_ratio = (double)(temp_pksent-temp_pkreceived)/(double)temp_pksent;
				//temp_delay = iter->second.delaySum.GetSeconds() / temp_pkreceived;
				//temp_delay = iter->second.delaySum / iter->second.rxPackets;
				//std::cout << "Delay: " << iter->second.delaySum / iter->second.rxPackets << "\n"; 

				/*if (t.destinationAddress=="10.1.1.1")
				{
					std::cout << "TEST: " << iter->second.txPackets << "\t";
					std::cout << "TEST: " << iter->second.rxPackets << "\n";
				} */
			
			}
		  	total = total + temp_total;
		  	pksent = pksent + temp_pksent;
		  	pkreceived = pkreceived + temp_pkreceived;
		  	pkloss = pkloss + temp_pkloss;
		  	ratio = ratio + temp_ratio;
		  	//delay = delay + temp_delay;
			Simulator::Destroy (); 

			count++;
		}

		std::cout << "Total throughput: " << total/count << "Mbps" <<"\t";
	  	std::cout << "Average throughput: " << total/nNodes/count <<"\n";  //<< "Mbps" <<"\n"
	  	std::cout << "Tx Packets: " << pksent/count << "\n";
	  	std::cout << "Rx Packets: " << pkreceived/count << "\n";
		std::cout << "Lost Packets(flowmonitor): " << pkloss/count << "\n";	
		std::cout << "Lost Packets(subtraction): " << (pksent-pkreceived)/count << "\n";				  
	  	std::cout << "Packet loss ratio: " << ratio/count <<"\n";
	  	//std::cout << "Delay: " << delay/count << "\n";

		//nNodes = nNodes + 1;
	//} 
	return 0;
}