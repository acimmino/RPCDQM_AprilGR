
import FWCore.ParameterSet.Config as cms

## Use RECO Muons flag
useMuons = False
isOfflineDQM = False

process = cms.Process("RPCDQM")

############## Event Source #####################
process.load("DQM.Integration.test.inputsource_cfi")
process.DQMEventStreamHttpReader.consumerName = 'RPC DQM Consumer'
 #process.DQMEventStreamHttpReader.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('HLT_MinBia*','HLT_CSCBeamHaloOverlapRing2','HLT_CSCBeamHaloRing2or3', 'HLT_L1Mu*','HLT_L1Mu','HLT_TrackerCosmics'))
process.DQMEventStreamHttpReader.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('*'))

############### HLT Filter#######################
process.load("HLTrigger.special.HLTTriggerTypeFilter_cfi")
# 0=random, 1=physics, 2=calibration, 3=technical
process.hltTriggerTypeFilter.SelectedTriggerType = 1

################# Geometry  #####################
#process.load("Geometry.MuonCommonData.muonIdealGeometryXML_cfi")
#process.load("Geometry.RPCGeometry.rpcGeometry_cfi")
#process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
################ Condition ######################
process.load("CondCore.DBCommon.CondDBSetup_cfi")

############# DQM Cetral Modules ################
process.load("DQMServices.Core.DQM_cfg")
process.load("DQM.Integration.test.FrontierCondition_GT_cfi")
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


############## DQM Enviroment ###################
process.load("DQM.Integration.test.environment_cfi")
process.dqmEnv.subSystemFolder = 'RPC'
process.load("DQMServices.Components.DQMEnvironment_cfi")

process.DQMStore.referenceFileName = '/dqmdata/dqm/reference/rpc_reference.root'

############### Scaler Producer #################
process.load("EventFilter.ScalersRawToDigi.ScalersRawToDigi_cfi")

############## RPC Unpacker  ####################
process.rpcunpacker = cms.EDProducer("RPCUnpackingModule",
    InputLabel = cms.InputTag("source"),
    doSynchro = cms.bool(False)
)

################# RPC Rec Hits  #################
process.load("RecoLocalMuon.RPCRecHit.rpcRecHits_cfi")
process.rpcRecHits.rpcDigiLabel = 'rpcunpacker'


################ DQM Digi Module ################
process.load("DQM.RPCMonitorDigi.RPCDigiMonitoring_cfi")
process.rpcdigidqm.UseMuon =  cms.untracked.bool(useMuons)
process.rpcdigidqm.NoiseFolder  = cms.untracked.string("AllHits")

################# DCS Info ######################
process.load("DQM.RPCMonitorDigi.RPCDcsInfo_cfi")

################# DQM Client Modules ############
process.load("DQM.RPCMonitorClient.RPCDqmClient_cfi")
process.rpcdqmclient.RPCDqmClientList = cms.untracked.vstring("RPCMultiplicityTest", "RPCDeadChannelTest", "RPCClusterSizeTest", "RPCOccupancyTest","RPCNoisyStripTest")
process.rpcdqmclient.DiagnosticPrescale = cms.untracked.int32(1)
process.rpcdqmclient.MinimumRPCEvents  = cms.untracked.int32(100)
process.rpcdqmclient.OfflineDQM = cms.untracked.bool(isOfflineDQM)
process.rpcdqmclient.RecHitTypeFolder = cms.untracked.string("AllHits")
    
################# Other Clients #################
#process.load("DQM.RPCMonitorClient.RPCMon_SS_Dbx_Global_cfi")

################### FED #########################
process.load("DQM.RPCMonitorClient.RPCMonitorRaw_cfi")
process.load("DQM.RPCMonitorClient.RPCFEDIntegrity_cfi")
process.load("DQM.RPCMonitorClient.RPCMonitorLinkSynchro_cfi")

########### RPC Event Summary Module ############
process.load("DQM.RPCMonitorClient.RPCEventSummary_cfi")
process.rpcEventSummary.OfflineDQM = cms.untracked.bool(isOfflineDQM )
process.rpcEventSummary.MinimumRPCEvents  = cms.untracked.int32(10000)
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
process.rpcChamberQuality.MinimumRPCEvents  = cms.untracked.int32(10000)
                             
###############  Sequences ######################
process.rpcSource = cms.Sequence(process.rpcunpacker*process.rpcRecHits*process.scalersRawToDigi*process.rpcdigidqm*process.rpcMonitorRaw*process.rpcDcsInfo*process.qTesterRPC)
process.rpcClient = cms.Sequence(process.rpcdqmclient*process.rpcChamberQuality*process.rpcEventSummary*process.dqmEnv*process.dqmSaver)
#process.p = cms.Path(process.rpcSource*process.rpcClient)
process.p = cms.Path(process.hltTriggerTypeFilter*process.rpcSource*process.rpcClient)

process.rpcunpacker.InputLabel = cms.InputTag("rawDataCollector")
process.scalersRawToDigi.scalersInputTag = cms.InputTag("rawDataCollector")
#--------------------------------------------------
# Heavy Ion Specific Fed Raw Data Collection Label
#--------------------------------------------------

print "Running with run type = ", process.runType.getRunType()

if (process.runType.getRunType() == process.runType.hi_run):
    process.rpcunpacker.InputLabel = cms.InputTag("rawDataRepacker")
    process.scalersRawToDigi.scalersInputTag = cms.InputTag("rawDataRepacker")
    process.rpcEventSummary.MinimumRPCEvents  = cms.untracked.int32(100000)
