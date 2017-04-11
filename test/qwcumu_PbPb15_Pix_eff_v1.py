import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuGap")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '75X_dataRun2_v13', '')

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/pixeltracking_1.root")
)


import HLTrigger.HLTfilters.hltHighLevel_cfi

process.hltMB = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltMB.HLTPaths = [
	"HLT_HIL1MinimumBiasHF2AND*",
	"HLT_HIL1MinimumBiasHF1AND*",
]
process.hltMB.andOr = cms.bool(True)
process.hltMB.throw = cms.bool(False)

process.cumugap = cms.EDAnalyzer('QWCumuGap'
	, trackEta = cms.untracked.InputTag('QWEvent', "eta")
	, trackPhi = cms.untracked.InputTag('QWEvent', "phi")
	, trackPt = cms.untracked.InputTag('QWEvent', "pt")
	, trackWeight = cms.untracked.InputTag('QWEvent', "weight")
	, trackCharge = cms.untracked.InputTag('QWEvent', "charge")
	, vertexZ = cms.untracked.InputTag('QWEvent', "vz")
	, centrality = cms.untracked.InputTag('centralityBin', "HFtowers")
	, minvz = cms.untracked.double(-15.0)
	, maxvz = cms.untracked.double(15.0)
	, rfpmineta = cms.untracked.double(-2.4)
	, rfpmaxeta = cms.untracked.double(2.4)
	, rfpminpt = cms.untracked.double(0.3)
	, rfpmaxpt = cms.untracked.double(3.0)
	, cmode = cms.untracked.int32(1)
	, nvtx = cms.untracked.int32(100)
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('cumu.root')
)


process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')

process.clusterCompatibilityFilter.clusterPars = cms.vdouble(0.0,0.006)

process.eventSelection = cms.Sequence(
        process.hfCoincFilter3
        + process.primaryVertexFilter
        + process.clusterCompatibilityFilter
)


process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')

process.CentFilter0_5 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(0, 10)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)

process.CentFilter5_10 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(10, 20)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)

process.CentFilter10_15 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(20, 30)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)

process.CentFilter15_20 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(30, 40)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)

process.CentFilter20_25 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(40, 50)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)

process.CentFilter25_30 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(50, 60)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)

process.CentFilter30_35 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(60, 70)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)

process.CentFilter35_40 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(70, 80)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)

process.CentFilter40_50 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(80, 100)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)

process.CentFilter50_60 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(100, 120)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)
process.CentFilter60_70 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(120, 140)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)

process.CentFilter70_80 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(140, 160)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)
process.CentFilter80_90 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(160, 180)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)

process.CentFilter90_00 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(180, 200)
		),
	BinLabel = cms.InputTag("centralityBin", "HFtowers")
	)




process.QWAcc_Cent05_pT004 = cms.EDAnalyzer("QWEventAccAnalyzer",
		srcPhi = cms.untracked.InputTag("QWEvent", "phi"),
		srcEta = cms.untracked.InputTag("QWEvent", "eta"),
		srcPt = cms.untracked.InputTag("QWEvent", "pt"),
		srcWeight = cms.untracked.InputTag("QWEvent", "weight"),
		minPt = cms.untracked.double(0.3),
		maxPt = cms.untracked.double(0.4)
		)

process.QWAcc_Cent05_pT005 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(0.4),
		maxPt = cms.untracked.double(0.5)
		)


process.QWAcc_Cent05_pT006 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(0.5),
		maxPt = cms.untracked.double(0.6)
		)

process.QWAcc_Cent05_pT008 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(0.6),
		maxPt = cms.untracked.double(0.8)
		)

process.QWAcc_Cent05_pT010 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(0.8),
		maxPt = cms.untracked.double(1.0)
		)

process.QWAcc_Cent05_pT012 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(1.0),
		maxPt = cms.untracked.double(1.25)
		)

process.QWAcc_Cent05_pT015 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(1.25),
		maxPt = cms.untracked.double(1.5)
		)

process.QWAcc_Cent05_pT020 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(1.5),
		maxPt = cms.untracked.double(2.0)
		)

process.QWAcc_Cent05_pT025 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(2.0),
		maxPt = cms.untracked.double(2.5)
		)


process.QWAcc_Cent05_pT030 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(2.5),
		maxPt = cms.untracked.double(3.0)
		)

process.QWAcc_Cent05_pT035 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(3.0),
		maxPt = cms.untracked.double(3.5)
		)

process.QWAcc_Cent05_pT040 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(3.5),
		maxPt = cms.untracked.double(4.0)
		)

process.QWAcc_Cent05_pT050 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(4.0),
		maxPt = cms.untracked.double(5.0)
		)

process.QWAcc_Cent05_pT060 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(5.0),
		maxPt = cms.untracked.double(6.0)
		)

process.QWAcc_Cent05_pT070 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(6.0),
		maxPt = cms.untracked.double(7.0)
		)

process.QWAcc_Cent05_pT080 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(7.0),
		maxPt = cms.untracked.double(8.0)
		)

process.QWAcc_Cent05_pT100 = process.QWAcc_Cent05_pT004.clone(
		minPt = cms.untracked.double(8.0),
		maxPt = cms.untracked.double(10.0)
		)

process.QWAcc_Cent10_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent15_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent20_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent25_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent30_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent35_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent40_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent50_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent60_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent70_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent80_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent90_pT004 = process.QWAcc_Cent05_pT004.clone()
process.QWAcc_Cent00_pT004 = process.QWAcc_Cent05_pT004.clone()

process.QWAcc_Cent10_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent15_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent20_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent25_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent30_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent35_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent40_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent50_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent60_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent70_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent80_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent90_pT005 = process.QWAcc_Cent05_pT005.clone()
process.QWAcc_Cent00_pT005 = process.QWAcc_Cent05_pT005.clone()

process.QWAcc_Cent10_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent15_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent20_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent25_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent30_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent35_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent40_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent50_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent60_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent70_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent80_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent90_pT006 = process.QWAcc_Cent05_pT006.clone()
process.QWAcc_Cent00_pT006 = process.QWAcc_Cent05_pT006.clone()

process.QWAcc_Cent10_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent15_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent20_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent25_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent30_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent35_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent40_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent50_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent60_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent70_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent80_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent90_pT008 = process.QWAcc_Cent05_pT008.clone()
process.QWAcc_Cent00_pT008 = process.QWAcc_Cent05_pT008.clone()

process.QWAcc_Cent10_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent15_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent20_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent25_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent30_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent35_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent40_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent50_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent60_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent70_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent80_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent90_pT010 = process.QWAcc_Cent05_pT010.clone()
process.QWAcc_Cent00_pT010 = process.QWAcc_Cent05_pT010.clone()

process.QWAcc_Cent10_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent15_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent20_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent25_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent30_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent35_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent40_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent50_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent60_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent70_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent80_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent90_pT012 = process.QWAcc_Cent05_pT012.clone()
process.QWAcc_Cent00_pT012 = process.QWAcc_Cent05_pT012.clone()

process.QWAcc_Cent10_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent15_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent20_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent25_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent30_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent35_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent40_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent50_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent60_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent70_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent80_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent90_pT015 = process.QWAcc_Cent05_pT015.clone()
process.QWAcc_Cent00_pT015 = process.QWAcc_Cent05_pT015.clone()

process.QWAcc_Cent10_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent15_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent20_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent25_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent30_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent35_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent40_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent50_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent60_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent70_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent80_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent90_pT020 = process.QWAcc_Cent05_pT020.clone()
process.QWAcc_Cent00_pT020 = process.QWAcc_Cent05_pT020.clone()

process.QWAcc_Cent10_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent15_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent20_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent25_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent30_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent35_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent40_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent50_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent60_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent70_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent80_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent90_pT025 = process.QWAcc_Cent05_pT025.clone()
process.QWAcc_Cent00_pT025 = process.QWAcc_Cent05_pT025.clone()

process.QWAcc_Cent10_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent15_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent20_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent25_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent30_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent35_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent40_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent50_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent60_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent70_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent80_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent90_pT030 = process.QWAcc_Cent05_pT030.clone()
process.QWAcc_Cent00_pT030 = process.QWAcc_Cent05_pT030.clone()

process.QWAcc_Cent10_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent15_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent20_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent25_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent30_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent35_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent40_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent50_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent60_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent70_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent80_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent90_pT035 = process.QWAcc_Cent05_pT035.clone()
process.QWAcc_Cent00_pT035 = process.QWAcc_Cent05_pT035.clone()

process.QWAcc_Cent10_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent15_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent20_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent25_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent30_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent35_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent40_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent50_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent60_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent70_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent80_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent90_pT040 = process.QWAcc_Cent05_pT040.clone()
process.QWAcc_Cent00_pT040 = process.QWAcc_Cent05_pT040.clone()

process.QWAcc_Cent10_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent15_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent20_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent25_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent30_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent35_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent40_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent50_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent60_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent70_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent80_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent90_pT050 = process.QWAcc_Cent05_pT050.clone()
process.QWAcc_Cent00_pT050 = process.QWAcc_Cent05_pT050.clone()

process.QWAcc_Cent10_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent15_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent20_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent25_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent30_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent35_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent40_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent50_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent60_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent70_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent80_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent90_pT060 = process.QWAcc_Cent05_pT060.clone()
process.QWAcc_Cent00_pT060 = process.QWAcc_Cent05_pT060.clone()

process.QWAcc_Cent10_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent15_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent20_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent25_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent30_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent35_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent40_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent50_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent60_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent70_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent80_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent90_pT070 = process.QWAcc_Cent05_pT070.clone()
process.QWAcc_Cent00_pT070 = process.QWAcc_Cent05_pT070.clone()

process.QWAcc_Cent10_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent15_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent20_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent25_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent30_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent35_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent40_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent50_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent60_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent70_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent80_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent90_pT080 = process.QWAcc_Cent05_pT080.clone()
process.QWAcc_Cent00_pT080 = process.QWAcc_Cent05_pT080.clone()

process.QWAcc_Cent10_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent15_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent20_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent25_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent30_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent35_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent40_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent50_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent60_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent70_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent80_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent90_pT100 = process.QWAcc_Cent05_pT100.clone()
process.QWAcc_Cent00_pT100 = process.QWAcc_Cent05_pT100.clone()


process.load('PbPb_HIMB2_pixel_eff')

process.pre_ana = cms.Sequence(process.hltMB*process.eventSelection*process.makeEvent)

process.pre_ana05 = cms.Sequence( process.pre_ana * process.CentFilter0_5 )
process.pre_ana10 = cms.Sequence( process.pre_ana * process.CentFilter5_10 )
process.pre_ana15 = cms.Sequence( process.pre_ana * process.CentFilter10_15 )
process.pre_ana20 = cms.Sequence( process.pre_ana * process.CentFilter15_20 )
process.pre_ana25 = cms.Sequence( process.pre_ana * process.CentFilter20_25 )
process.pre_ana30 = cms.Sequence( process.pre_ana * process.CentFilter25_30 )
process.pre_ana35 = cms.Sequence( process.pre_ana * process.CentFilter30_35 )
process.pre_ana40 = cms.Sequence( process.pre_ana * process.CentFilter35_40 )
process.pre_ana50 = cms.Sequence( process.pre_ana * process.CentFilter40_50 )
process.pre_ana60 = cms.Sequence( process.pre_ana * process.CentFilter50_60 )
process.pre_ana70 = cms.Sequence( process.pre_ana * process.CentFilter60_70 )
process.pre_ana80 = cms.Sequence( process.pre_ana * process.CentFilter70_80 )
process.pre_ana90 = cms.Sequence( process.pre_ana * process.CentFilter80_90 )
process.pre_ana00 = cms.Sequence( process.pre_ana * process.CentFilter90_00 )

process.ana05 = cms.Path(
		process.pre_ana05 *
		process.QWAcc_Cent05_pT004 *
		process.QWAcc_Cent05_pT005 *
		process.QWAcc_Cent05_pT006 *
		process.QWAcc_Cent05_pT008 *
		process.QWAcc_Cent05_pT010 *
		process.QWAcc_Cent05_pT012 *
		process.QWAcc_Cent05_pT015 *
		process.QWAcc_Cent05_pT020 *
		process.QWAcc_Cent05_pT025 *
		process.QWAcc_Cent05_pT030 *
		process.QWAcc_Cent05_pT035 *
		process.QWAcc_Cent05_pT040 *
		process.QWAcc_Cent05_pT050 *
		process.QWAcc_Cent05_pT060 *
		process.QWAcc_Cent05_pT070 *
		process.QWAcc_Cent05_pT080 *
		process.QWAcc_Cent05_pT100 )

process.ana10 = cms.Path(
		process.pre_ana10 *
		process.QWAcc_Cent10_pT004 *
		process.QWAcc_Cent10_pT005 *
		process.QWAcc_Cent10_pT006 *
		process.QWAcc_Cent10_pT008 *
		process.QWAcc_Cent10_pT010 *
		process.QWAcc_Cent10_pT012 *
		process.QWAcc_Cent10_pT015 *
		process.QWAcc_Cent10_pT020 *
		process.QWAcc_Cent10_pT025 *
		process.QWAcc_Cent10_pT030 *
		process.QWAcc_Cent10_pT035 *
		process.QWAcc_Cent10_pT040 *
		process.QWAcc_Cent10_pT050 *
		process.QWAcc_Cent10_pT060 *
		process.QWAcc_Cent10_pT070 *
		process.QWAcc_Cent10_pT080 *
		process.QWAcc_Cent10_pT100 )

process.ana15 = cms.Path(
		process.pre_ana15 *
		process.QWAcc_Cent15_pT004 *
		process.QWAcc_Cent15_pT005 *
		process.QWAcc_Cent15_pT006 *
		process.QWAcc_Cent15_pT008 *
		process.QWAcc_Cent15_pT010 *
		process.QWAcc_Cent15_pT012 *
		process.QWAcc_Cent15_pT015 *
		process.QWAcc_Cent15_pT020 *
		process.QWAcc_Cent15_pT025 *
		process.QWAcc_Cent15_pT030 *
		process.QWAcc_Cent15_pT035 *
		process.QWAcc_Cent15_pT040 *
		process.QWAcc_Cent15_pT050 *
		process.QWAcc_Cent15_pT060 *
		process.QWAcc_Cent15_pT070 *
		process.QWAcc_Cent15_pT080 *
		process.QWAcc_Cent15_pT100 )


process.ana20 = cms.Path(
		process.pre_ana20 *
		process.QWAcc_Cent20_pT004 *
		process.QWAcc_Cent20_pT005 *
		process.QWAcc_Cent20_pT006 *
		process.QWAcc_Cent20_pT008 *
		process.QWAcc_Cent20_pT010 *
		process.QWAcc_Cent20_pT012 *
		process.QWAcc_Cent20_pT015 *
		process.QWAcc_Cent20_pT020 *
		process.QWAcc_Cent20_pT025 *
		process.QWAcc_Cent20_pT030 *
		process.QWAcc_Cent20_pT035 *
		process.QWAcc_Cent20_pT040 *
		process.QWAcc_Cent20_pT050 *
		process.QWAcc_Cent20_pT060 *
		process.QWAcc_Cent20_pT070 *
		process.QWAcc_Cent20_pT080 *
		process.QWAcc_Cent20_pT100 )

process.ana25 = cms.Path(
		process.pre_ana25*
		process.QWAcc_Cent25_pT004 *
		process.QWAcc_Cent25_pT005 *
		process.QWAcc_Cent25_pT006 *
		process.QWAcc_Cent25_pT008 *
		process.QWAcc_Cent25_pT010 *
		process.QWAcc_Cent25_pT012 *
		process.QWAcc_Cent25_pT015 *
		process.QWAcc_Cent25_pT020 *
		process.QWAcc_Cent25_pT025 *
		process.QWAcc_Cent25_pT030 *
		process.QWAcc_Cent25_pT035 *
		process.QWAcc_Cent25_pT040 *
		process.QWAcc_Cent25_pT050 *
		process.QWAcc_Cent25_pT060 *
		process.QWAcc_Cent25_pT070 *
		process.QWAcc_Cent25_pT080 *
		process.QWAcc_Cent25_pT100 )

process.ana30 = cms.Path(
		process.pre_ana30*
		process.QWAcc_Cent30_pT004 *
		process.QWAcc_Cent30_pT005 *
		process.QWAcc_Cent30_pT006 *
		process.QWAcc_Cent30_pT008 *
		process.QWAcc_Cent30_pT010 *
		process.QWAcc_Cent30_pT012 *
		process.QWAcc_Cent30_pT015 *
		process.QWAcc_Cent30_pT020 *
		process.QWAcc_Cent30_pT025 *
		process.QWAcc_Cent30_pT030 *
		process.QWAcc_Cent30_pT035 *
		process.QWAcc_Cent30_pT040 *
		process.QWAcc_Cent30_pT050 *
		process.QWAcc_Cent30_pT060 *
		process.QWAcc_Cent30_pT070 *
		process.QWAcc_Cent30_pT080 *
		process.QWAcc_Cent30_pT100 )

process.ana35 = cms.Path(
		process.pre_ana35*
		process.QWAcc_Cent35_pT004 *
		process.QWAcc_Cent35_pT005 *
		process.QWAcc_Cent35_pT006 *
		process.QWAcc_Cent35_pT008 *
		process.QWAcc_Cent35_pT010 *
		process.QWAcc_Cent35_pT012 *
		process.QWAcc_Cent35_pT015 *
		process.QWAcc_Cent35_pT020 *
		process.QWAcc_Cent35_pT025 *
		process.QWAcc_Cent35_pT030 *
		process.QWAcc_Cent35_pT035 *
		process.QWAcc_Cent35_pT040 *
		process.QWAcc_Cent35_pT050 *
		process.QWAcc_Cent35_pT060 *
		process.QWAcc_Cent35_pT070 *
		process.QWAcc_Cent35_pT080 *
		process.QWAcc_Cent35_pT100 )

process.ana40 = cms.Path(
		process.pre_ana40*
		process.QWAcc_Cent40_pT004 *
		process.QWAcc_Cent40_pT005 *
		process.QWAcc_Cent40_pT006 *
		process.QWAcc_Cent40_pT008 *
		process.QWAcc_Cent40_pT010 *
		process.QWAcc_Cent40_pT012 *
		process.QWAcc_Cent40_pT015 *
		process.QWAcc_Cent40_pT020 *
		process.QWAcc_Cent40_pT025 *
		process.QWAcc_Cent40_pT030 *
		process.QWAcc_Cent40_pT035 *
		process.QWAcc_Cent40_pT040 *
		process.QWAcc_Cent40_pT050 *
		process.QWAcc_Cent40_pT060 *
		process.QWAcc_Cent40_pT070 *
		process.QWAcc_Cent40_pT080 *
		process.QWAcc_Cent40_pT100 )

process.ana50 = cms.Path(
		process.pre_ana50*
		process.QWAcc_Cent50_pT004 *
		process.QWAcc_Cent50_pT005 *
		process.QWAcc_Cent50_pT006 *
		process.QWAcc_Cent50_pT008 *
		process.QWAcc_Cent50_pT010 *
		process.QWAcc_Cent50_pT012 *
		process.QWAcc_Cent50_pT015 *
		process.QWAcc_Cent50_pT020 *
		process.QWAcc_Cent50_pT025 *
		process.QWAcc_Cent50_pT030 *
		process.QWAcc_Cent50_pT035 *
		process.QWAcc_Cent50_pT040 *
		process.QWAcc_Cent50_pT050 *
		process.QWAcc_Cent50_pT060 *
		process.QWAcc_Cent50_pT070 *
		process.QWAcc_Cent50_pT080 *
		process.QWAcc_Cent50_pT100 )


process.ana60 = cms.Path(
		process.pre_ana60*
		process.QWAcc_Cent60_pT004 *
		process.QWAcc_Cent60_pT005 *
		process.QWAcc_Cent60_pT006 *
		process.QWAcc_Cent60_pT008 *
		process.QWAcc_Cent60_pT010 *
		process.QWAcc_Cent60_pT012 *
		process.QWAcc_Cent60_pT015 *
		process.QWAcc_Cent60_pT020 *
		process.QWAcc_Cent60_pT025 *
		process.QWAcc_Cent60_pT030 *
		process.QWAcc_Cent60_pT035 *
		process.QWAcc_Cent60_pT040 *
		process.QWAcc_Cent60_pT050 *
		process.QWAcc_Cent60_pT060 *
		process.QWAcc_Cent60_pT070 *
		process.QWAcc_Cent60_pT080 *
		process.QWAcc_Cent60_pT100 )


process.ana70 = cms.Path(
		process.pre_ana70*
		process.QWAcc_Cent70_pT004 *
		process.QWAcc_Cent70_pT005 *
		process.QWAcc_Cent70_pT006 *
		process.QWAcc_Cent70_pT008 *
		process.QWAcc_Cent70_pT010 *
		process.QWAcc_Cent70_pT012 *
		process.QWAcc_Cent70_pT015 *
		process.QWAcc_Cent70_pT020 *
		process.QWAcc_Cent70_pT025 *
		process.QWAcc_Cent70_pT030 *
		process.QWAcc_Cent70_pT035 *
		process.QWAcc_Cent70_pT040 *
		process.QWAcc_Cent70_pT050 *
		process.QWAcc_Cent70_pT060 *
		process.QWAcc_Cent70_pT070 *
		process.QWAcc_Cent70_pT080 *
		process.QWAcc_Cent70_pT100 )


process.ana80 = cms.Path(
		process.pre_ana80*
		process.QWAcc_Cent80_pT004 *
		process.QWAcc_Cent80_pT005 *
		process.QWAcc_Cent80_pT006 *
		process.QWAcc_Cent80_pT008 *
		process.QWAcc_Cent80_pT010 *
		process.QWAcc_Cent80_pT012 *
		process.QWAcc_Cent80_pT015 *
		process.QWAcc_Cent80_pT020 *
		process.QWAcc_Cent80_pT025 *
		process.QWAcc_Cent80_pT030 *
		process.QWAcc_Cent80_pT035 *
		process.QWAcc_Cent80_pT040 *
		process.QWAcc_Cent80_pT050 *
		process.QWAcc_Cent80_pT060 *
		process.QWAcc_Cent80_pT070 *
		process.QWAcc_Cent80_pT080 *
		process.QWAcc_Cent80_pT100 )


process.ana90 = cms.Path(
		process.pre_ana90*
		process.QWAcc_Cent90_pT004 *
		process.QWAcc_Cent90_pT005 *
		process.QWAcc_Cent90_pT006 *
		process.QWAcc_Cent90_pT008 *
		process.QWAcc_Cent90_pT010 *
		process.QWAcc_Cent90_pT012 *
		process.QWAcc_Cent90_pT015 *
		process.QWAcc_Cent90_pT020 *
		process.QWAcc_Cent90_pT025 *
		process.QWAcc_Cent90_pT030 *
		process.QWAcc_Cent90_pT035 *
		process.QWAcc_Cent90_pT040 *
		process.QWAcc_Cent90_pT050 *
		process.QWAcc_Cent90_pT060 *
		process.QWAcc_Cent90_pT070 *
		process.QWAcc_Cent90_pT080 *
		process.QWAcc_Cent90_pT100 )


process.ana00 = cms.Path(
		process.pre_ana00*
		process.QWAcc_Cent00_pT004 *
		process.QWAcc_Cent00_pT005 *
		process.QWAcc_Cent00_pT006 *
		process.QWAcc_Cent00_pT008 *
		process.QWAcc_Cent00_pT010 *
		process.QWAcc_Cent00_pT012 *
		process.QWAcc_Cent00_pT015 *
		process.QWAcc_Cent00_pT020 *
		process.QWAcc_Cent00_pT025 *
		process.QWAcc_Cent00_pT030 *
		process.QWAcc_Cent00_pT035 *
		process.QWAcc_Cent00_pT040 *
		process.QWAcc_Cent00_pT050 *
		process.QWAcc_Cent00_pT060 *
		process.QWAcc_Cent00_pT070 *
		process.QWAcc_Cent00_pT080 *
		process.QWAcc_Cent00_pT100 )

process.ana = cms.Path(process.pre_ana*process.cumugap )

process.schedule = cms.Schedule(
	process.ana,
	process.ana05,
	process.ana10,
	process.ana15,
	process.ana20,
	process.ana25,
	process.ana30,
	process.ana35,
	process.ana40,
	process.ana50,
	process.ana60,
	process.ana70,
	process.ana80,
	process.ana90,
	process.ana00,
)
