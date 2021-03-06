#ifndef DQM_RPCMonitorClient_DQMDaqInfo_H
# define DQM_RPCMonitorClient_DQMDaqInfo_H

// system include files
#include <memory>
#include <iostream>
#include <fstream>

// FWCore
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

//DQM
#include "DQMServices/Core/interface/DQMStore.h"
#include "DQMServices/Core/interface/MonitorElement.h"


class RPCDaqInfo : public edm::EDAnalyzer {
public:
  explicit RPCDaqInfo(const edm::ParameterSet&);
  ~RPCDaqInfo();
  

private:
  virtual void beginJob() ;
  void beginRun(const edm::Run& , const edm::EventSetup&);
  virtual void beginLuminosityBlock(const edm::LuminosityBlock& , const  edm::EventSetup&);
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endLuminosityBlock(const edm::LuminosityBlock& , const  edm::EventSetup&);
  virtual void endJob() ;
  
  DQMStore *dbe_;  
  
  MonitorElement*  DaqFraction_;
  MonitorElement * DaqMap_;
  MonitorElement* daqWheelFractions[5];
  MonitorElement* daqDiskFractions[10];

  std::pair<int,int> FEDRange_;

  int  numberOfDisks_,NumberOfFeds_;
 
};

#endif
