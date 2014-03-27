
import FWCore.ParameterSet.Config as cms

## Use RECO Muons flag
useMuons = False
isOfflineDQM = False

process = cms.Process("RPCDQM")

############# Source File #################
#process.source = cms.Source("EmptySource")
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/c/cimmino/DQM/CMSSW_5_2_7/src/DQM/RPCMonitorDigi/test/out_reco.root')
                            )

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

############### HLT Filter#######################
process.load("HLTrigger.special.HLTTriggerTypeFilter_cfi")
# 0=random, 1=physics, 2=calibration, 3=technical
process.hltTriggerTypeFilter.SelectedTriggerType = 1

############ Geometry ######################
process.load("Configuration.StandardSequences.GeometryDB_cff")

################ Condition #################
process.load("CondCore.DBCommon.CondDBSetup_cfi")

############# Frontier Conditions GT #######
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("DQM.Integration.test.FrontierCondition_GT_cfi")
process.GlobalTag.globaltag = "GR_R_52_V10::All"
process.GlobalTag.RefreshEachRun = cms.untracked.bool(True)


process.GlobalTag.pfnPrefix = cms.untracked.string( 'frontier://FrontierProd/' )
process.GlobalTag.toGet = cms.VPSet()
process.GlobalTag.toGet.append(
    cms.PSet(
    record = cms.string("GeometryFileRcd"),
    # label  = cms.untracked.string("ExtendedPostLS1"),
    tag = cms.string("XMLFILE_Geometry_61YV2_ExtendedPostLS1_mc"),
    connect = cms.untracked.string("frontier://FrontierPrep/CMS_COND_GEOMETRY")
    )
    )
process.GlobalTag.toGet.append(
    cms.PSet(
    record = cms.string("RPCRecoGeometryRcd"),
    # label  = cms.untracked.string(""),
    tag = cms.string("RPCRECO_Geometry_61YV2"),
    connect = cms.untracked.string("frontier://FrontierPrep/CMS_COND_GEOMETRY")
    )
    )
process.GlobalTag.toGet.append(
    cms.PSet(
    record = cms.string("RPCStripNoisesRcd"),
    # label  = cms.untracked.string(""),
    tag = cms.string("RPCStripNoise_upscope_mc_v2"),
    connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_RPC")
    )
    )
process.GlobalTag.toGet.append(
    cms.PSet(
    record = cms.string("RPCClusterSizeRcd"),
    # label  = cms.untracked.string(""),
    tag = cms.string("RPCClusterSize_upscope_mc_v2"),
    connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_36X_RPC")
    )
    )


############# DQM Cetral Modules ################
process.load("DQMServices.Core.DQM_cfg")


############## DQM Enviroment ###################
process.load("DQM.Integration.test.environment_cfi")
process.dqmEnv.subSystemFolder = 'RPC'
process.dqmSaver.dirName = '/afs/cern.ch/user/c/cimmino/DQM/test/CMSSW_5_2_7/src/DQM/RPCMonitorDigi/test'

#process.DQMStore.referenceFileName = '/dqmdata/dqm/reference/rpc_reference.root'


############### Scaler Producer #################
process.load("EventFilter.ScalersRawToDigi.ScalersRawToDigi_cfi")

############## RPC Unpacker ####################
process.rpcunpacker = cms.EDProducer("RPCUnpackingModule",
    InputLabel = cms.InputTag("source"),
    doSynchro = cms.bool(False)
)


################# RPC Rec Hits #################
process.load("RecoLocalMuon.RPCRecHit.rpcRecHits_cfi")
process.rpcRecHits.rpcDigiLabel = 'rpcunpacker'



################ DQM Digi Module ################
process.load("DQM.RPCMonitorDigi.RPCDigiMonitoring_cfi")
process.rpcdigidqm.UseMuon = cms.untracked.bool(useMuons)
process.rpcdigidqm.NoiseFolder = cms.untracked.string("AllHits")

################# DCS Info ######################
process.load("DQM.RPCMonitorDigi.RPCDcsInfo_cfi")

################# DQM Client Modules ############
process.load("DQM.RPCMonitorClient.RPCDqmClient_cfi")
process.rpcdqmclient.RPCDqmClientList = cms.untracked.vstring("RPCMultiplicityTest", "RPCDeadChannelTest", "RPCClusterSizeTest", "RPCOccupancyTest","RPCNoisyStripTest")
process.rpcdqmclient.DiagnosticPrescale = cms.untracked.int32(1)
process.rpcdqmclient.MinimumRPCEvents = cms.untracked.int32(100)
process.rpcdqmclient.OfflineDQM = cms.untracked.bool(isOfflineDQM)
process.rpcdqmclient.RecHitTypeFolder = cms.untracked.string("AllHits")



################### FED #########################
process.load("DQM.RPCMonitorClient.RPCMonitorRaw_cfi")
process.load("DQM.RPCMonitorClient.RPCFEDIntegrity_cfi")
process.load("DQM.RPCMonitorClient.RPCMonitorLinkSynchro_cfi")



########### RPC Event Summary Module ############
process.load("DQM.RPCMonitorClient.RPCEventSummary_cfi")
process.rpcEventSummary.OfflineDQM = cms.untracked.bool(isOfflineDQM )
process.rpcEventSummary.MinimumRPCEvents = cms.untracked.int32(10000)
process.rpcEventSummary.RecHitTypeFolder = cms.untracked.string("AllHits")


################# Quality Tests #################
process.qTesterRPC = cms.EDAnalyzer("QualityTester",
    qtList = cms.untracked.FileInPath('DQM/RPCMonitorClient/test/RPCQualityTests.xml'),
    prescaleFactor = cms.untracked.int32(5),
    qtestOnEndLumi = cms.untracked.bool(True),
    qtestOnEndRun = cms.untracked.bool(True)
)

############## Chamber Quality ##################
process.load("DQM.RPCMonitorClient.RPCChamberQuality_cfi")
process.rpcChamberQuality.OfflineDQM = cms.untracked.bool(isOfflineDQM )
process.rpcChamberQuality.RecHitTypeFolder = cms.untracked.string("AllHits")
process.rpcChamberQuality.MinimumRPCEvents = cms.untracked.int32(10000)


############### Sequences ######################
process.rpcSource = cms.Sequence(process.rpcdigidqm*process.rpcDcsInfo*process.qTesterRPC)
process.rpcClient = cms.Sequence(process.rpcdqmclient*process.rpcChamberQuality*process.rpcEventSummary*process.dqmEnv*process.dqmSaver)
#process.p = cms.Path(process.rpcSource*process.rpcClient)
process.p = cms.Path(process.hltTriggerTypeFilter*process.rpcSource*process.rpcClient)
