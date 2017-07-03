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

process.PrimaryVz = cms.EDProducer('QWVectorSelector',
		vectSrc = cms.untracked.InputTag('QWEvent', 'vz')
		)

process.VzFilter0 = cms.EDFilter('QWDoubleFilter',
		src = cms.untracked.InputTag('PrimaryVz'),
		dmin = cms.untracked.double(-15.),
		dmax = cms.untracked.double(-12.),
		)
process.VzFilter1 = process.VzFilter0.clone(
		dmin = cms.untracked.double(-12.),
		dmax = cms.untracked.double(-9.),
		)
process.VzFilter2 = process.VzFilter0.clone(
		dmin = cms.untracked.double(-9.),
		dmax = cms.untracked.double(-6.),
		)
process.VzFilter3 = process.VzFilter0.clone(
		dmin = cms.untracked.double(-6.),
		dmax = cms.untracked.double(-3.),
		)
process.VzFilter4 = process.VzFilter0.clone(
		dmin = cms.untracked.double(-3.),
		dmax = cms.untracked.double(0.),
		)
process.VzFilter5 = process.VzFilter0.clone(
		dmin = cms.untracked.double(0.),
		dmax = cms.untracked.double(3.),
		)
process.VzFilter6 = process.VzFilter0.clone(
		dmin = cms.untracked.double(3.),
		dmax = cms.untracked.double(6.),
		)
process.VzFilter7 = process.VzFilter0.clone(
		dmin = cms.untracked.double(6.),
		dmax = cms.untracked.double(9.),
		)
process.VzFilter8 = process.VzFilter0.clone(
		dmin = cms.untracked.double(9.),
		dmax = cms.untracked.double(12.),
		)
process.VzFilter9 = process.VzFilter0.clone(
		dmin = cms.untracked.double(12.),
		dmax = cms.untracked.double(15.),
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



process.QWAcc_Cent05Vz0_pT004 = cms.EDAnalyzer("QWEventAccAnalyzer",
		srcPhi = cms.untracked.InputTag("QWEvent", "phi"),
		srcEta = cms.untracked.InputTag("QWEvent", "eta"),
		srcPt = cms.untracked.InputTag("QWEvent", "pt"),
		srcWeight = cms.untracked.InputTag("QWEvent", "weight"),
		minPt = cms.untracked.double(0.3),
		maxPt = cms.untracked.double(0.4)
		)

process.QWAcc_Cent05Vz0_pT005 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(0.4),
		maxPt = cms.untracked.double(0.5)
		)


process.QWAcc_Cent05Vz0_pT006 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(0.5),
		maxPt = cms.untracked.double(0.6)
		)

process.QWAcc_Cent05Vz0_pT008 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(0.6),
		maxPt = cms.untracked.double(0.8)
		)

process.QWAcc_Cent05Vz0_pT010 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(0.8),
		maxPt = cms.untracked.double(1.0)
		)

process.QWAcc_Cent05Vz0_pT012 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(1.0),
		maxPt = cms.untracked.double(1.25)
		)

process.QWAcc_Cent05Vz0_pT015 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(1.25),
		maxPt = cms.untracked.double(1.5)
		)

process.QWAcc_Cent05Vz0_pT020 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(1.5),
		maxPt = cms.untracked.double(2.0)
		)

process.QWAcc_Cent05Vz0_pT025 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(2.0),
		maxPt = cms.untracked.double(2.5)
		)


process.QWAcc_Cent05Vz0_pT030 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(2.5),
		maxPt = cms.untracked.double(3.0)
		)

process.QWAcc_Cent05Vz0_pT035 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(3.0),
		maxPt = cms.untracked.double(3.5)
		)

process.QWAcc_Cent05Vz0_pT040 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(3.5),
		maxPt = cms.untracked.double(4.0)
		)

process.QWAcc_Cent05Vz0_pT050 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(4.0),
		maxPt = cms.untracked.double(5.0)
		)

process.QWAcc_Cent05Vz0_pT060 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(5.0),
		maxPt = cms.untracked.double(6.0)
		)

process.QWAcc_Cent05Vz0_pT070 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(6.0),
		maxPt = cms.untracked.double(7.0)
		)

process.QWAcc_Cent05Vz0_pT080 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(7.0),
		maxPt = cms.untracked.double(8.0)
		)

process.QWAcc_Cent05Vz0_pT100 = process.QWAcc_Cent05Vz0_pT004.clone(
		minPt = cms.untracked.double(8.0),
		maxPt = cms.untracked.double(10.0)
		)



# Vz0

process.QWAcc_Cent10Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent15Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent20Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent25Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent30Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent35Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent40Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent50Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent60Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent70Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent80Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent90Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent00Vz0_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()

process.QWAcc_Cent10Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent15Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent20Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent25Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent30Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent35Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent40Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent50Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent60Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent70Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent80Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent90Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent00Vz0_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()

process.QWAcc_Cent10Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent15Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent20Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent25Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent30Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent35Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent40Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent50Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent60Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent70Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent80Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent90Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent00Vz0_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()

process.QWAcc_Cent10Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent15Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent20Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent25Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent30Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent35Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent40Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent50Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent60Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent70Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent80Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent90Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent00Vz0_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()

process.QWAcc_Cent10Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent15Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent20Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent25Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent30Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent35Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent40Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent50Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent60Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent70Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent80Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent90Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent00Vz0_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()

process.QWAcc_Cent10Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent15Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent20Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent25Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent30Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent35Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent40Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent50Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent60Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent70Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent80Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent90Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent00Vz0_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()

process.QWAcc_Cent10Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent15Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent20Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent25Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent30Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent35Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent40Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent50Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent60Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent70Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent80Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent90Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent00Vz0_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()

process.QWAcc_Cent10Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent15Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent20Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent25Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent30Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent35Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent40Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent50Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent60Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent70Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent80Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent90Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent00Vz0_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()

process.QWAcc_Cent10Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent15Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent20Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent25Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent30Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent35Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent40Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent50Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent60Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent70Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent80Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent90Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent00Vz0_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()

process.QWAcc_Cent10Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent15Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent20Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent25Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent30Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent35Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent40Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent50Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent60Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent70Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent80Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent90Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent00Vz0_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()

process.QWAcc_Cent10Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent15Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent20Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent25Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent30Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent35Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent40Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent50Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent60Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent70Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent80Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent90Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent00Vz0_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()

process.QWAcc_Cent10Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent15Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent20Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent25Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent30Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent35Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent40Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent50Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent60Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent70Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent80Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent90Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent00Vz0_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()

process.QWAcc_Cent10Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent15Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent20Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent25Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent30Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent35Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent40Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent50Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent60Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent70Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent80Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent90Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent00Vz0_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()

process.QWAcc_Cent10Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent15Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent20Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent25Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent30Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent35Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent40Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent50Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent60Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent70Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent80Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent90Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent00Vz0_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()

process.QWAcc_Cent10Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent15Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent20Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent25Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent30Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent35Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent40Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent50Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent60Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent70Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent80Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent90Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent00Vz0_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()

process.QWAcc_Cent10Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent15Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent20Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent25Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent30Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent35Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent40Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent50Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent60Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent70Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent80Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent90Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent00Vz0_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()

process.QWAcc_Cent10Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent15Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent20Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent25Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent30Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent35Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent40Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent50Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent60Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent70Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent80Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent90Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent00Vz0_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()

# Vz1
process.QWAcc_Cent05Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent10Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent15Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent20Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent25Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent30Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent35Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent40Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent50Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent60Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent70Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent80Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent90Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent00Vz1_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()

process.QWAcc_Cent05Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent10Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent15Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent20Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent25Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent30Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent35Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent40Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent50Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent60Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent70Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent80Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent90Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent00Vz1_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()

process.QWAcc_Cent05Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent10Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent15Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent20Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent25Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent30Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent35Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent40Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent50Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent60Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent70Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent80Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent90Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent00Vz1_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()

process.QWAcc_Cent05Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent10Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent15Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent20Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent25Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent30Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent35Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent40Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent50Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent60Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent70Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent80Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent90Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent00Vz1_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()

process.QWAcc_Cent05Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent10Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent15Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent20Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent25Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent30Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent35Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent40Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent50Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent60Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent70Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent80Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent90Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent00Vz1_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()

process.QWAcc_Cent05Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent10Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent15Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent20Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent25Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent30Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent35Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent40Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent50Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent60Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent70Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent80Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent90Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent00Vz1_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()

process.QWAcc_Cent05Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent10Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent15Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent20Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent25Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent30Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent35Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent40Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent50Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent60Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent70Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent80Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent90Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent00Vz1_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()

process.QWAcc_Cent05Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent10Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent15Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent20Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent25Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent30Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent35Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent40Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent50Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent60Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent70Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent80Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent90Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent00Vz1_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()

process.QWAcc_Cent05Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent10Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent15Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent20Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent25Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent30Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent35Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent40Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent50Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent60Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent70Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent80Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent90Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent00Vz1_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()

process.QWAcc_Cent05Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent10Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent15Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent20Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent25Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent30Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent35Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent40Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent50Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent60Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent70Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent80Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent90Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent00Vz1_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()

process.QWAcc_Cent05Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent10Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent15Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent20Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent25Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent30Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent35Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent40Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent50Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent60Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent70Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent80Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent90Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent00Vz1_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()

process.QWAcc_Cent05Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent10Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent15Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent20Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent25Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent30Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent35Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent40Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent50Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent60Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent70Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent80Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent90Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent00Vz1_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()

process.QWAcc_Cent05Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent10Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent15Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent20Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent25Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent30Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent35Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent40Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent50Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent60Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent70Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent80Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent90Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent00Vz1_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()

process.QWAcc_Cent05Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent10Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent15Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent20Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent25Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent30Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent35Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent40Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent50Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent60Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent70Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent80Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent90Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent00Vz1_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()

process.QWAcc_Cent05Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent10Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent15Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent20Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent25Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent30Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent35Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent40Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent50Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent60Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent70Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent80Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent90Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent00Vz1_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()

process.QWAcc_Cent05Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent10Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent15Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent20Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent25Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent30Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent35Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent40Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent50Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent60Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent70Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent80Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent90Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent00Vz1_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()

process.QWAcc_Cent05Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent10Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent15Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent20Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent25Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent30Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent35Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent40Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent50Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent60Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent70Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent80Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent90Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent00Vz1_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()







# Vz2
process.QWAcc_Cent05Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent10Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent15Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent20Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent25Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent30Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent35Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent40Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent50Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent60Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent70Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent80Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent90Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent00Vz2_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()

process.QWAcc_Cent05Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent10Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent15Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent20Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent25Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent30Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent35Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent40Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent50Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent60Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent70Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent80Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent90Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent00Vz2_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()

process.QWAcc_Cent05Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent10Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent15Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent20Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent25Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent30Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent35Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent40Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent50Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent60Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent70Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent80Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent90Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent00Vz2_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()

process.QWAcc_Cent05Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent10Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent15Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent20Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent25Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent30Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent35Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent40Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent50Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent60Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent70Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent80Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent90Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent00Vz2_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()

process.QWAcc_Cent05Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent10Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent15Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent20Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent25Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent30Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent35Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent40Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent50Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent60Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent70Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent80Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent90Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent00Vz2_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()

process.QWAcc_Cent05Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent10Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent15Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent20Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent25Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent30Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent35Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent40Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent50Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent60Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent70Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent80Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent90Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent00Vz2_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()

process.QWAcc_Cent05Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent10Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent15Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent20Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent25Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent30Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent35Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent40Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent50Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent60Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent70Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent80Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent90Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent00Vz2_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()

process.QWAcc_Cent05Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent10Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent15Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent20Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent25Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent30Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent35Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent40Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent50Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent60Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent70Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent80Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent90Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent00Vz2_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()

process.QWAcc_Cent05Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent10Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent15Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent20Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent25Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent30Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent35Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent40Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent50Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent60Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent70Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent80Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent90Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent00Vz2_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()

process.QWAcc_Cent05Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent10Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent15Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent20Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent25Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent30Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent35Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent40Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent50Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent60Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent70Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent80Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent90Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent00Vz2_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()

process.QWAcc_Cent05Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent10Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent15Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent20Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent25Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent30Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent35Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent40Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent50Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent60Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent70Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent80Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent90Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent00Vz2_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()

process.QWAcc_Cent05Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent10Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent15Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent20Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent25Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent30Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent35Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent40Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent50Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent60Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent70Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent80Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent90Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent00Vz2_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()

process.QWAcc_Cent05Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent10Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent15Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent20Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent25Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent30Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent35Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent40Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent50Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent60Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent70Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent80Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent90Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent00Vz2_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()

process.QWAcc_Cent05Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent10Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent15Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent20Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent25Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent30Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent35Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent40Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent50Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent60Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent70Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent80Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent90Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent00Vz2_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()

process.QWAcc_Cent05Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent10Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent15Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent20Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent25Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent30Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent35Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent40Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent50Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent60Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent70Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent80Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent90Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent00Vz2_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()

process.QWAcc_Cent05Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent10Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent15Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent20Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent25Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent30Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent35Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent40Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent50Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent60Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent70Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent80Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent90Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent00Vz2_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()

process.QWAcc_Cent05Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent10Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent15Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent20Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent25Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent30Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent35Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent40Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent50Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent60Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent70Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent80Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent90Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent00Vz2_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()



# Vz3
process.QWAcc_Cent05Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent10Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent15Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent20Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent25Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent30Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent35Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent40Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent50Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent60Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent70Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent80Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent90Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent00Vz3_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()

process.QWAcc_Cent05Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent10Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent15Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent20Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent25Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent30Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent35Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent40Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent50Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent60Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent70Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent80Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent90Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent00Vz3_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()

process.QWAcc_Cent05Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent10Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent15Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent20Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent25Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent30Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent35Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent40Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent50Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent60Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent70Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent80Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent90Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent00Vz3_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()

process.QWAcc_Cent05Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent10Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent15Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent20Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent25Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent30Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent35Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent40Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent50Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent60Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent70Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent80Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent90Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent00Vz3_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()

process.QWAcc_Cent05Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent10Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent15Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent20Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent25Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent30Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent35Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent40Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent50Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent60Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent70Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent80Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent90Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent00Vz3_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()

process.QWAcc_Cent05Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent10Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent15Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent20Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent25Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent30Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent35Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent40Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent50Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent60Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent70Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent80Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent90Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent00Vz3_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()

process.QWAcc_Cent05Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent10Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent15Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent20Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent25Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent30Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent35Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent40Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent50Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent60Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent70Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent80Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent90Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent00Vz3_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()

process.QWAcc_Cent05Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent10Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent15Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent20Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent25Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent30Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent35Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent40Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent50Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent60Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent70Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent80Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent90Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent00Vz3_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()

process.QWAcc_Cent05Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent10Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent15Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent20Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent25Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent30Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent35Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent40Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent50Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent60Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent70Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent80Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent90Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent00Vz3_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()

process.QWAcc_Cent05Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent10Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent15Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent20Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent25Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent30Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent35Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent40Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent50Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent60Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent70Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent80Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent90Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent00Vz3_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()

process.QWAcc_Cent05Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent10Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent15Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent20Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent25Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent30Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent35Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent40Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent50Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent60Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent70Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent80Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent90Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent00Vz3_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()

process.QWAcc_Cent05Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent10Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent15Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent20Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent25Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent30Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent35Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent40Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent50Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent60Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent70Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent80Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent90Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent00Vz3_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()

process.QWAcc_Cent05Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent10Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent15Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent20Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent25Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent30Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent35Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent40Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent50Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent60Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent70Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent80Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent90Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent00Vz3_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()

process.QWAcc_Cent05Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent10Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent15Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent20Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent25Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent30Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent35Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent40Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent50Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent60Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent70Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent80Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent90Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent00Vz3_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()

process.QWAcc_Cent05Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent10Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent15Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent20Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent25Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent30Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent35Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent40Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent50Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent60Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent70Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent80Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent90Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent00Vz3_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()

process.QWAcc_Cent05Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent10Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent15Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent20Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent25Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent30Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent35Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent40Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent50Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent60Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent70Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent80Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent90Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent00Vz3_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()

process.QWAcc_Cent05Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent10Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent15Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent20Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent25Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent30Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent35Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent40Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent50Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent60Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent70Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent80Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent90Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent00Vz3_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()


# Vz4
process.QWAcc_Cent05Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent10Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent15Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent20Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent25Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent30Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent35Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent40Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent50Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent60Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent70Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent80Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent90Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent00Vz4_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()

process.QWAcc_Cent05Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent10Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent15Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent20Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent25Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent30Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent35Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent40Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent50Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent60Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent70Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent80Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent90Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent00Vz4_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()

process.QWAcc_Cent05Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent10Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent15Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent20Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent25Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent30Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent35Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent40Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent50Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent60Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent70Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent80Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent90Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent00Vz4_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()

process.QWAcc_Cent05Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent10Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent15Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent20Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent25Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent30Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent35Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent40Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent50Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent60Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent70Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent80Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent90Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent00Vz4_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()

process.QWAcc_Cent05Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent10Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent15Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent20Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent25Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent30Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent35Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent40Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent50Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent60Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent70Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent80Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent90Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent00Vz4_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()

process.QWAcc_Cent05Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent10Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent15Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent20Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent25Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent30Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent35Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent40Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent50Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent60Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent70Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent80Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent90Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent00Vz4_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()

process.QWAcc_Cent05Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent10Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent15Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent20Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent25Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent30Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent35Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent40Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent50Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent60Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent70Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent80Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent90Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent00Vz4_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()

process.QWAcc_Cent05Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent10Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent15Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent20Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent25Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent30Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent35Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent40Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent50Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent60Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent70Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent80Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent90Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent00Vz4_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()

process.QWAcc_Cent05Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent10Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent15Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent20Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent25Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent30Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent35Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent40Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent50Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent60Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent70Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent80Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent90Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent00Vz4_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()

process.QWAcc_Cent05Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent10Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent15Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent20Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent25Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent30Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent35Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent40Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent50Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent60Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent70Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent80Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent90Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent00Vz4_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()

process.QWAcc_Cent05Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent10Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent15Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent20Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent25Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent30Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent35Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent40Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent50Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent60Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent70Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent80Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent90Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent00Vz4_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()

process.QWAcc_Cent05Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent10Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent15Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent20Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent25Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent30Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent35Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent40Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent50Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent60Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent70Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent80Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent90Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent00Vz4_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()

process.QWAcc_Cent05Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent10Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent15Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent20Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent25Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent30Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent35Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent40Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent50Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent60Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent70Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent80Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent90Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent00Vz4_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()

process.QWAcc_Cent05Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent10Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent15Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent20Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent25Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent30Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent35Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent40Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent50Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent60Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent70Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent80Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent90Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent00Vz4_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()

process.QWAcc_Cent05Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent10Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent15Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent20Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent25Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent30Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent35Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent40Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent50Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent60Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent70Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent80Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent90Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent00Vz4_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()

process.QWAcc_Cent05Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent10Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent15Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent20Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent25Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent30Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent35Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent40Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent50Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent60Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent70Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent80Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent90Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent00Vz4_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()

process.QWAcc_Cent05Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent10Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent15Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent20Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent25Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent30Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent35Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent40Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent50Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent60Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent70Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent80Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent90Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent00Vz4_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()



# Vz5
process.QWAcc_Cent05Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent10Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent15Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent20Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent25Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent30Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent35Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent40Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent50Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent60Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent70Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent80Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent90Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent00Vz5_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()

process.QWAcc_Cent05Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent10Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent15Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent20Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent25Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent30Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent35Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent40Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent50Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent60Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent70Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent80Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent90Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent00Vz5_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()

process.QWAcc_Cent05Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent10Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent15Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent20Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent25Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent30Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent35Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent40Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent50Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent60Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent70Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent80Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent90Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent00Vz5_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()

process.QWAcc_Cent05Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent10Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent15Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent20Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent25Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent30Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent35Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent40Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent50Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent60Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent70Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent80Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent90Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent00Vz5_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()

process.QWAcc_Cent05Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent10Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent15Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent20Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent25Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent30Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent35Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent40Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent50Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent60Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent70Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent80Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent90Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent00Vz5_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()

process.QWAcc_Cent05Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent10Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent15Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent20Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent25Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent30Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent35Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent40Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent50Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent60Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent70Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent80Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent90Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent00Vz5_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()

process.QWAcc_Cent05Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent10Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent15Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent20Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent25Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent30Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent35Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent40Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent50Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent60Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent70Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent80Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent90Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent00Vz5_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()

process.QWAcc_Cent05Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent10Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent15Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent20Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent25Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent30Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent35Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent40Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent50Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent60Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent70Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent80Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent90Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent00Vz5_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()

process.QWAcc_Cent05Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent10Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent15Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent20Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent25Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent30Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent35Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent40Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent50Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent60Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent70Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent80Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent90Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent00Vz5_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()

process.QWAcc_Cent05Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent10Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent15Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent20Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent25Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent30Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent35Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent40Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent50Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent60Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent70Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent80Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent90Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent00Vz5_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()

process.QWAcc_Cent05Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent10Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent15Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent20Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent25Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent30Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent35Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent40Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent50Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent60Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent70Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent80Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent90Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent00Vz5_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()

process.QWAcc_Cent05Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent10Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent15Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent20Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent25Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent30Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent35Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent40Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent50Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent60Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent70Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent80Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent90Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent00Vz5_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()

process.QWAcc_Cent05Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent10Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent15Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent20Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent25Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent30Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent35Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent40Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent50Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent60Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent70Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent80Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent90Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent00Vz5_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()

process.QWAcc_Cent05Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent10Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent15Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent20Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent25Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent30Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent35Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent40Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent50Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent60Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent70Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent80Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent90Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent00Vz5_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()

process.QWAcc_Cent05Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent10Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent15Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent20Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent25Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent30Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent35Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent40Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent50Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent60Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent70Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent80Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent90Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent00Vz5_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()

process.QWAcc_Cent05Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent10Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent15Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent20Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent25Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent30Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent35Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent40Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent50Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent60Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent70Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent80Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent90Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent00Vz5_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()

process.QWAcc_Cent05Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent10Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent15Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent20Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent25Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent30Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent35Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent40Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent50Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent60Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent70Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent80Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent90Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent00Vz5_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()



# Vz6
process.QWAcc_Cent05Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent10Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent15Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent20Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent25Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent30Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent35Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent40Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent50Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent60Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent70Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent80Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent90Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent00Vz6_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()

process.QWAcc_Cent05Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent10Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent15Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent20Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent25Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent30Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent35Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent40Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent50Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent60Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent70Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent80Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent90Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent00Vz6_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()

process.QWAcc_Cent05Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent10Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent15Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent20Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent25Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent30Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent35Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent40Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent50Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent60Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent70Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent80Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent90Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent00Vz6_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()

process.QWAcc_Cent05Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent10Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent15Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent20Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent25Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent30Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent35Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent40Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent50Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent60Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent70Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent80Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent90Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent00Vz6_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()

process.QWAcc_Cent05Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent10Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent15Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent20Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent25Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent30Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent35Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent40Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent50Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent60Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent70Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent80Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent90Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent00Vz6_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()

process.QWAcc_Cent05Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent10Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent15Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent20Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent25Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent30Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent35Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent40Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent50Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent60Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent70Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent80Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent90Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent00Vz6_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()

process.QWAcc_Cent05Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent10Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent15Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent20Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent25Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent30Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent35Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent40Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent50Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent60Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent70Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent80Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent90Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent00Vz6_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()

process.QWAcc_Cent05Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent10Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent15Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent20Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent25Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent30Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent35Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent40Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent50Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent60Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent70Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent80Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent90Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent00Vz6_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()

process.QWAcc_Cent05Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent10Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent15Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent20Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent25Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent30Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent35Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent40Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent50Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent60Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent70Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent80Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent90Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent00Vz6_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()

process.QWAcc_Cent05Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent10Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent15Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent20Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent25Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent30Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent35Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent40Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent50Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent60Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent70Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent80Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent90Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent00Vz6_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()

process.QWAcc_Cent05Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent10Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent15Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent20Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent25Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent30Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent35Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent40Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent50Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent60Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent70Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent80Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent90Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent00Vz6_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()

process.QWAcc_Cent05Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent10Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent15Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent20Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent25Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent30Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent35Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent40Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent50Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent60Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent70Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent80Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent90Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent00Vz6_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()

process.QWAcc_Cent05Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent10Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent15Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent20Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent25Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent30Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent35Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent40Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent50Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent60Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent70Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent80Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent90Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent00Vz6_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()

process.QWAcc_Cent05Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent10Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent15Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent20Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent25Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent30Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent35Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent40Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent50Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent60Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent70Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent80Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent90Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent00Vz6_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()

process.QWAcc_Cent05Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent10Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent15Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent20Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent25Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent30Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent35Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent40Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent50Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent60Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent70Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent80Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent90Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent00Vz6_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()

process.QWAcc_Cent05Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent10Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent15Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent20Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent25Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent30Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent35Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent40Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent50Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent60Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent70Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent80Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent90Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent00Vz6_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()

process.QWAcc_Cent05Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent10Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent15Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent20Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent25Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent30Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent35Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent40Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent50Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent60Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent70Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent80Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent90Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent00Vz6_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()



# Vz7
process.QWAcc_Cent05Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent10Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent15Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent20Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent25Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent30Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent35Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent40Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent50Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent60Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent70Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent80Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent90Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent00Vz7_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()

process.QWAcc_Cent05Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent10Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent15Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent20Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent25Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent30Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent35Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent40Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent50Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent60Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent70Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent80Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent90Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent00Vz7_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()

process.QWAcc_Cent05Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent10Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent15Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent20Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent25Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent30Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent35Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent40Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent50Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent60Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent70Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent80Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent90Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent00Vz7_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()

process.QWAcc_Cent05Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent10Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent15Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent20Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent25Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent30Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent35Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent40Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent50Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent60Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent70Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent80Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent90Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent00Vz7_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()

process.QWAcc_Cent05Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent10Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent15Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent20Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent25Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent30Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent35Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent40Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent50Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent60Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent70Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent80Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent90Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent00Vz7_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()

process.QWAcc_Cent05Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent10Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent15Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent20Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent25Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent30Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent35Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent40Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent50Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent60Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent70Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent80Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent90Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent00Vz7_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()

process.QWAcc_Cent05Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent10Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent15Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent20Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent25Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent30Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent35Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent40Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent50Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent60Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent70Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent80Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent90Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent00Vz7_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()

process.QWAcc_Cent05Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent10Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent15Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent20Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent25Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent30Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent35Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent40Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent50Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent60Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent70Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent80Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent90Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent00Vz7_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()

process.QWAcc_Cent05Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent10Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent15Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent20Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent25Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent30Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent35Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent40Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent50Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent60Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent70Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent80Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent90Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent00Vz7_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()

process.QWAcc_Cent05Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent10Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent15Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent20Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent25Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent30Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent35Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent40Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent50Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent60Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent70Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent80Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent90Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent00Vz7_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()

process.QWAcc_Cent05Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent10Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent15Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent20Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent25Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent30Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent35Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent40Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent50Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent60Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent70Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent80Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent90Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent00Vz7_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()

process.QWAcc_Cent05Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent10Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent15Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent20Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent25Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent30Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent35Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent40Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent50Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent60Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent70Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent80Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent90Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent00Vz7_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()

process.QWAcc_Cent05Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent10Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent15Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent20Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent25Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent30Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent35Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent40Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent50Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent60Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent70Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent80Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent90Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent00Vz7_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()

process.QWAcc_Cent05Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent10Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent15Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent20Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent25Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent30Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent35Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent40Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent50Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent60Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent70Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent80Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent90Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent00Vz7_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()

process.QWAcc_Cent05Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent10Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent15Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent20Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent25Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent30Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent35Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent40Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent50Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent60Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent70Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent80Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent90Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent00Vz7_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()

process.QWAcc_Cent05Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent10Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent15Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent20Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent25Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent30Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent35Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent40Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent50Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent60Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent70Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent80Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent90Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent00Vz7_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()

process.QWAcc_Cent05Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent10Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent15Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent20Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent25Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent30Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent35Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent40Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent50Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent60Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent70Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent80Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent90Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent00Vz7_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()



# Vz8
process.QWAcc_Cent05Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent10Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent15Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent20Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent25Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent30Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent35Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent40Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent50Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent60Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent70Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent80Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent90Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent00Vz8_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()

process.QWAcc_Cent05Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent10Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent15Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent20Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent25Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent30Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent35Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent40Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent50Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent60Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent70Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent80Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent90Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent00Vz8_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()

process.QWAcc_Cent05Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent10Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent15Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent20Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent25Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent30Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent35Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent40Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent50Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent60Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent70Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent80Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent90Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent00Vz8_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()

process.QWAcc_Cent05Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent10Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent15Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent20Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent25Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent30Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent35Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent40Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent50Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent60Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent70Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent80Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent90Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent00Vz8_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()

process.QWAcc_Cent05Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent10Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent15Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent20Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent25Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent30Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent35Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent40Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent50Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent60Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent70Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent80Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent90Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent00Vz8_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()

process.QWAcc_Cent05Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent10Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent15Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent20Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent25Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent30Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent35Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent40Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent50Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent60Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent70Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent80Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent90Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent00Vz8_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()

process.QWAcc_Cent05Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent10Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent15Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent20Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent25Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent30Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent35Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent40Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent50Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent60Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent70Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent80Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent90Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent00Vz8_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()

process.QWAcc_Cent05Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent10Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent15Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent20Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent25Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent30Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent35Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent40Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent50Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent60Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent70Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent80Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent90Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent00Vz8_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()

process.QWAcc_Cent05Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent10Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent15Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent20Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent25Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent30Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent35Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent40Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent50Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent60Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent70Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent80Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent90Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent00Vz8_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()

process.QWAcc_Cent05Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent10Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent15Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent20Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent25Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent30Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent35Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent40Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent50Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent60Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent70Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent80Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent90Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent00Vz8_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()

process.QWAcc_Cent05Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent10Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent15Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent20Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent25Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent30Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent35Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent40Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent50Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent60Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent70Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent80Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent90Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent00Vz8_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()

process.QWAcc_Cent05Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent10Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent15Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent20Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent25Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent30Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent35Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent40Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent50Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent60Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent70Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent80Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent90Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent00Vz8_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()

process.QWAcc_Cent05Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent10Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent15Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent20Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent25Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent30Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent35Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent40Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent50Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent60Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent70Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent80Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent90Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent00Vz8_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()

process.QWAcc_Cent05Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent10Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent15Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent20Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent25Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent30Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent35Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent40Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent50Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent60Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent70Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent80Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent90Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent00Vz8_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()

process.QWAcc_Cent05Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent10Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent15Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent20Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent25Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent30Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent35Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent40Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent50Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent60Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent70Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent80Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent90Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent00Vz8_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()

process.QWAcc_Cent05Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent10Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent15Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent20Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent25Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent30Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent35Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent40Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent50Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent60Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent70Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent80Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent90Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent00Vz8_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()

process.QWAcc_Cent05Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent10Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent15Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent20Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent25Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent30Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent35Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent40Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent50Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent60Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent70Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent80Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent90Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent00Vz8_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()


# Vz9
process.QWAcc_Cent05Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent10Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent15Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent20Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent25Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent30Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent35Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent40Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent50Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent60Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent70Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent80Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent90Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()
process.QWAcc_Cent00Vz9_pT004 = process.QWAcc_Cent05Vz0_pT004.clone()

process.QWAcc_Cent05Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent10Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent15Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent20Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent25Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent30Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent35Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent40Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent50Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent60Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent70Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent80Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent90Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()
process.QWAcc_Cent00Vz9_pT005 = process.QWAcc_Cent05Vz0_pT005.clone()

process.QWAcc_Cent05Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent10Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent15Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent20Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent25Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent30Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent35Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent40Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent50Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent60Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent70Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent80Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent90Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()
process.QWAcc_Cent00Vz9_pT006 = process.QWAcc_Cent05Vz0_pT006.clone()

process.QWAcc_Cent05Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent10Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent15Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent20Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent25Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent30Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent35Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent40Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent50Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent60Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent70Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent80Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent90Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()
process.QWAcc_Cent00Vz9_pT008 = process.QWAcc_Cent05Vz0_pT008.clone()

process.QWAcc_Cent05Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent10Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent15Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent20Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent25Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent30Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent35Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent40Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent50Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent60Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent70Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent80Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent90Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()
process.QWAcc_Cent00Vz9_pT010 = process.QWAcc_Cent05Vz0_pT010.clone()

process.QWAcc_Cent05Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent10Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent15Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent20Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent25Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent30Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent35Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent40Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent50Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent60Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent70Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent80Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent90Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()
process.QWAcc_Cent00Vz9_pT012 = process.QWAcc_Cent05Vz0_pT012.clone()

process.QWAcc_Cent05Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent10Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent15Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent20Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent25Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent30Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent35Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent40Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent50Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent60Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent70Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent80Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent90Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()
process.QWAcc_Cent00Vz9_pT015 = process.QWAcc_Cent05Vz0_pT015.clone()

process.QWAcc_Cent05Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent10Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent15Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent20Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent25Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent30Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent35Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent40Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent50Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent60Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent70Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent80Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent90Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()
process.QWAcc_Cent00Vz9_pT020 = process.QWAcc_Cent05Vz0_pT020.clone()

process.QWAcc_Cent05Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent10Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent15Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent20Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent25Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent30Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent35Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent40Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent50Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent60Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent70Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent80Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent90Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()
process.QWAcc_Cent00Vz9_pT025 = process.QWAcc_Cent05Vz0_pT025.clone()

process.QWAcc_Cent05Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent10Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent15Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent20Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent25Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent30Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent35Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent40Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent50Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent60Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent70Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent80Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent90Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()
process.QWAcc_Cent00Vz9_pT030 = process.QWAcc_Cent05Vz0_pT030.clone()

process.QWAcc_Cent05Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent10Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent15Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent20Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent25Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent30Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent35Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent40Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent50Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent60Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent70Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent80Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent90Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()
process.QWAcc_Cent00Vz9_pT035 = process.QWAcc_Cent05Vz0_pT035.clone()

process.QWAcc_Cent05Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent10Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent15Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent20Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent25Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent30Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent35Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent40Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent50Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent60Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent70Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent80Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent90Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()
process.QWAcc_Cent00Vz9_pT040 = process.QWAcc_Cent05Vz0_pT040.clone()

process.QWAcc_Cent05Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent10Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent15Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent20Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent25Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent30Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent35Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent40Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent50Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent60Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent70Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent80Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent90Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()
process.QWAcc_Cent00Vz9_pT050 = process.QWAcc_Cent05Vz0_pT050.clone()

process.QWAcc_Cent05Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent10Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent15Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent20Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent25Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent30Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent35Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent40Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent50Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent60Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent70Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent80Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent90Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()
process.QWAcc_Cent00Vz9_pT060 = process.QWAcc_Cent05Vz0_pT060.clone()

process.QWAcc_Cent05Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent10Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent15Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent20Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent25Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent30Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent35Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent40Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent50Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent60Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent70Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent80Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent90Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()
process.QWAcc_Cent00Vz9_pT070 = process.QWAcc_Cent05Vz0_pT070.clone()

process.QWAcc_Cent05Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent10Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent15Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent20Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent25Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent30Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent35Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent40Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent50Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent60Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent70Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent80Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent90Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()
process.QWAcc_Cent00Vz9_pT080 = process.QWAcc_Cent05Vz0_pT080.clone()

process.QWAcc_Cent05Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent10Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent15Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent20Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent25Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent30Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent35Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent40Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent50Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent60Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent70Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent80Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent90Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()
process.QWAcc_Cent00Vz9_pT100 = process.QWAcc_Cent05Vz0_pT100.clone()


process.load('PbPb_HIMB2_pixel_eff')

process.pre_ana = cms.Sequence(process.hltMB*process.eventSelection*process.makeEvent*process.PrimaryVz)

process.pre_ana05Vz0 = cms.Sequence( process.pre_ana * process.CentFilter0_5   * process.VzFilter0)
process.pre_ana10Vz0 = cms.Sequence( process.pre_ana * process.CentFilter5_10  * process.VzFilter0)
process.pre_ana15Vz0 = cms.Sequence( process.pre_ana * process.CentFilter10_15 * process.VzFilter0)
process.pre_ana20Vz0 = cms.Sequence( process.pre_ana * process.CentFilter15_20 * process.VzFilter0)
process.pre_ana25Vz0 = cms.Sequence( process.pre_ana * process.CentFilter20_25 * process.VzFilter0)
process.pre_ana30Vz0 = cms.Sequence( process.pre_ana * process.CentFilter25_30 * process.VzFilter0)
process.pre_ana35Vz0 = cms.Sequence( process.pre_ana * process.CentFilter30_35 * process.VzFilter0)
process.pre_ana40Vz0 = cms.Sequence( process.pre_ana * process.CentFilter35_40 * process.VzFilter0)
process.pre_ana50Vz0 = cms.Sequence( process.pre_ana * process.CentFilter40_50 * process.VzFilter0)
process.pre_ana60Vz0 = cms.Sequence( process.pre_ana * process.CentFilter50_60 * process.VzFilter0)
process.pre_ana70Vz0 = cms.Sequence( process.pre_ana * process.CentFilter60_70 * process.VzFilter0)
process.pre_ana80Vz0 = cms.Sequence( process.pre_ana * process.CentFilter70_80 * process.VzFilter0)
process.pre_ana90Vz0 = cms.Sequence( process.pre_ana * process.CentFilter80_90 * process.VzFilter0)
process.pre_ana00Vz0 = cms.Sequence( process.pre_ana * process.CentFilter90_00 * process.VzFilter0)

process.pre_ana05Vz1 = cms.Sequence( process.pre_ana * process.CentFilter0_5   * process.VzFilter1)
process.pre_ana10Vz1 = cms.Sequence( process.pre_ana * process.CentFilter5_10  * process.VzFilter1)
process.pre_ana15Vz1 = cms.Sequence( process.pre_ana * process.CentFilter10_15 * process.VzFilter1)
process.pre_ana20Vz1 = cms.Sequence( process.pre_ana * process.CentFilter15_20 * process.VzFilter1)
process.pre_ana25Vz1 = cms.Sequence( process.pre_ana * process.CentFilter20_25 * process.VzFilter1)
process.pre_ana30Vz1 = cms.Sequence( process.pre_ana * process.CentFilter25_30 * process.VzFilter1)
process.pre_ana35Vz1 = cms.Sequence( process.pre_ana * process.CentFilter30_35 * process.VzFilter1)
process.pre_ana40Vz1 = cms.Sequence( process.pre_ana * process.CentFilter35_40 * process.VzFilter1)
process.pre_ana50Vz1 = cms.Sequence( process.pre_ana * process.CentFilter40_50 * process.VzFilter1)
process.pre_ana60Vz1 = cms.Sequence( process.pre_ana * process.CentFilter50_60 * process.VzFilter1)
process.pre_ana70Vz1 = cms.Sequence( process.pre_ana * process.CentFilter60_70 * process.VzFilter1)
process.pre_ana80Vz1 = cms.Sequence( process.pre_ana * process.CentFilter70_80 * process.VzFilter1)
process.pre_ana90Vz1 = cms.Sequence( process.pre_ana * process.CentFilter80_90 * process.VzFilter1)
process.pre_ana00Vz1 = cms.Sequence( process.pre_ana * process.CentFilter90_00 * process.VzFilter1)

process.pre_ana05Vz2 = cms.Sequence( process.pre_ana * process.CentFilter0_5   * process.VzFilter2)
process.pre_ana10Vz2 = cms.Sequence( process.pre_ana * process.CentFilter5_10  * process.VzFilter2)
process.pre_ana15Vz2 = cms.Sequence( process.pre_ana * process.CentFilter10_15 * process.VzFilter2)
process.pre_ana20Vz2 = cms.Sequence( process.pre_ana * process.CentFilter15_20 * process.VzFilter2)
process.pre_ana25Vz2 = cms.Sequence( process.pre_ana * process.CentFilter20_25 * process.VzFilter2)
process.pre_ana30Vz2 = cms.Sequence( process.pre_ana * process.CentFilter25_30 * process.VzFilter2)
process.pre_ana35Vz2 = cms.Sequence( process.pre_ana * process.CentFilter30_35 * process.VzFilter2)
process.pre_ana40Vz2 = cms.Sequence( process.pre_ana * process.CentFilter35_40 * process.VzFilter2)
process.pre_ana50Vz2 = cms.Sequence( process.pre_ana * process.CentFilter40_50 * process.VzFilter2)
process.pre_ana60Vz2 = cms.Sequence( process.pre_ana * process.CentFilter50_60 * process.VzFilter2)
process.pre_ana70Vz2 = cms.Sequence( process.pre_ana * process.CentFilter60_70 * process.VzFilter2)
process.pre_ana80Vz2 = cms.Sequence( process.pre_ana * process.CentFilter70_80 * process.VzFilter2)
process.pre_ana90Vz2 = cms.Sequence( process.pre_ana * process.CentFilter80_90 * process.VzFilter2)
process.pre_ana00Vz2 = cms.Sequence( process.pre_ana * process.CentFilter90_00 * process.VzFilter2)


process.pre_ana05Vz3 = cms.Sequence( process.pre_ana * process.CentFilter0_5   * process.VzFilter3)
process.pre_ana10Vz3 = cms.Sequence( process.pre_ana * process.CentFilter5_10  * process.VzFilter3)
process.pre_ana15Vz3 = cms.Sequence( process.pre_ana * process.CentFilter10_15 * process.VzFilter3)
process.pre_ana20Vz3 = cms.Sequence( process.pre_ana * process.CentFilter15_20 * process.VzFilter3)
process.pre_ana25Vz3 = cms.Sequence( process.pre_ana * process.CentFilter20_25 * process.VzFilter3)
process.pre_ana30Vz3 = cms.Sequence( process.pre_ana * process.CentFilter25_30 * process.VzFilter3)
process.pre_ana35Vz3 = cms.Sequence( process.pre_ana * process.CentFilter30_35 * process.VzFilter3)
process.pre_ana40Vz3 = cms.Sequence( process.pre_ana * process.CentFilter35_40 * process.VzFilter3)
process.pre_ana50Vz3 = cms.Sequence( process.pre_ana * process.CentFilter40_50 * process.VzFilter3)
process.pre_ana60Vz3 = cms.Sequence( process.pre_ana * process.CentFilter50_60 * process.VzFilter3)
process.pre_ana70Vz3 = cms.Sequence( process.pre_ana * process.CentFilter60_70 * process.VzFilter3)
process.pre_ana80Vz3 = cms.Sequence( process.pre_ana * process.CentFilter70_80 * process.VzFilter3)
process.pre_ana90Vz3 = cms.Sequence( process.pre_ana * process.CentFilter80_90 * process.VzFilter3)
process.pre_ana00Vz3 = cms.Sequence( process.pre_ana * process.CentFilter90_00 * process.VzFilter3)


process.pre_ana05Vz4 = cms.Sequence( process.pre_ana * process.CentFilter0_5   * process.VzFilter4)
process.pre_ana10Vz4 = cms.Sequence( process.pre_ana * process.CentFilter5_10  * process.VzFilter4)
process.pre_ana15Vz4 = cms.Sequence( process.pre_ana * process.CentFilter10_15 * process.VzFilter4)
process.pre_ana20Vz4 = cms.Sequence( process.pre_ana * process.CentFilter15_20 * process.VzFilter4)
process.pre_ana25Vz4 = cms.Sequence( process.pre_ana * process.CentFilter20_25 * process.VzFilter4)
process.pre_ana30Vz4 = cms.Sequence( process.pre_ana * process.CentFilter25_30 * process.VzFilter4)
process.pre_ana35Vz4 = cms.Sequence( process.pre_ana * process.CentFilter30_35 * process.VzFilter4)
process.pre_ana40Vz4 = cms.Sequence( process.pre_ana * process.CentFilter35_40 * process.VzFilter4)
process.pre_ana50Vz4 = cms.Sequence( process.pre_ana * process.CentFilter40_50 * process.VzFilter4)
process.pre_ana60Vz4 = cms.Sequence( process.pre_ana * process.CentFilter50_60 * process.VzFilter4)
process.pre_ana70Vz4 = cms.Sequence( process.pre_ana * process.CentFilter60_70 * process.VzFilter4)
process.pre_ana80Vz4 = cms.Sequence( process.pre_ana * process.CentFilter70_80 * process.VzFilter4)
process.pre_ana90Vz4 = cms.Sequence( process.pre_ana * process.CentFilter80_90 * process.VzFilter4)
process.pre_ana00Vz4 = cms.Sequence( process.pre_ana * process.CentFilter90_00 * process.VzFilter4)


process.pre_ana05Vz5 = cms.Sequence( process.pre_ana * process.CentFilter0_5   * process.VzFilter5)
process.pre_ana10Vz5 = cms.Sequence( process.pre_ana * process.CentFilter5_10  * process.VzFilter5)
process.pre_ana15Vz5 = cms.Sequence( process.pre_ana * process.CentFilter10_15 * process.VzFilter5)
process.pre_ana20Vz5 = cms.Sequence( process.pre_ana * process.CentFilter15_20 * process.VzFilter5)
process.pre_ana25Vz5 = cms.Sequence( process.pre_ana * process.CentFilter20_25 * process.VzFilter5)
process.pre_ana30Vz5 = cms.Sequence( process.pre_ana * process.CentFilter25_30 * process.VzFilter5)
process.pre_ana35Vz5 = cms.Sequence( process.pre_ana * process.CentFilter30_35 * process.VzFilter5)
process.pre_ana40Vz5 = cms.Sequence( process.pre_ana * process.CentFilter35_40 * process.VzFilter5)
process.pre_ana50Vz5 = cms.Sequence( process.pre_ana * process.CentFilter40_50 * process.VzFilter5)
process.pre_ana60Vz5 = cms.Sequence( process.pre_ana * process.CentFilter50_60 * process.VzFilter5)
process.pre_ana70Vz5 = cms.Sequence( process.pre_ana * process.CentFilter60_70 * process.VzFilter5)
process.pre_ana80Vz5 = cms.Sequence( process.pre_ana * process.CentFilter70_80 * process.VzFilter5)
process.pre_ana90Vz5 = cms.Sequence( process.pre_ana * process.CentFilter80_90 * process.VzFilter5)
process.pre_ana00Vz5 = cms.Sequence( process.pre_ana * process.CentFilter90_00 * process.VzFilter5)


process.pre_ana05Vz6 = cms.Sequence( process.pre_ana * process.CentFilter0_5   * process.VzFilter6)
process.pre_ana10Vz6 = cms.Sequence( process.pre_ana * process.CentFilter5_10  * process.VzFilter6)
process.pre_ana15Vz6 = cms.Sequence( process.pre_ana * process.CentFilter10_15 * process.VzFilter6)
process.pre_ana20Vz6 = cms.Sequence( process.pre_ana * process.CentFilter15_20 * process.VzFilter6)
process.pre_ana25Vz6 = cms.Sequence( process.pre_ana * process.CentFilter20_25 * process.VzFilter6)
process.pre_ana30Vz6 = cms.Sequence( process.pre_ana * process.CentFilter25_30 * process.VzFilter6)
process.pre_ana35Vz6 = cms.Sequence( process.pre_ana * process.CentFilter30_35 * process.VzFilter6)
process.pre_ana40Vz6 = cms.Sequence( process.pre_ana * process.CentFilter35_40 * process.VzFilter6)
process.pre_ana50Vz6 = cms.Sequence( process.pre_ana * process.CentFilter40_50 * process.VzFilter6)
process.pre_ana60Vz6 = cms.Sequence( process.pre_ana * process.CentFilter50_60 * process.VzFilter6)
process.pre_ana70Vz6 = cms.Sequence( process.pre_ana * process.CentFilter60_70 * process.VzFilter6)
process.pre_ana80Vz6 = cms.Sequence( process.pre_ana * process.CentFilter70_80 * process.VzFilter6)
process.pre_ana90Vz6 = cms.Sequence( process.pre_ana * process.CentFilter80_90 * process.VzFilter6)
process.pre_ana00Vz6 = cms.Sequence( process.pre_ana * process.CentFilter90_00 * process.VzFilter6)


process.pre_ana05Vz7 = cms.Sequence( process.pre_ana * process.CentFilter0_5   * process.VzFilter7)
process.pre_ana10Vz7 = cms.Sequence( process.pre_ana * process.CentFilter5_10  * process.VzFilter7)
process.pre_ana15Vz7 = cms.Sequence( process.pre_ana * process.CentFilter10_15 * process.VzFilter7)
process.pre_ana20Vz7 = cms.Sequence( process.pre_ana * process.CentFilter15_20 * process.VzFilter7)
process.pre_ana25Vz7 = cms.Sequence( process.pre_ana * process.CentFilter20_25 * process.VzFilter7)
process.pre_ana30Vz7 = cms.Sequence( process.pre_ana * process.CentFilter25_30 * process.VzFilter7)
process.pre_ana35Vz7 = cms.Sequence( process.pre_ana * process.CentFilter30_35 * process.VzFilter7)
process.pre_ana40Vz7 = cms.Sequence( process.pre_ana * process.CentFilter35_40 * process.VzFilter7)
process.pre_ana50Vz7 = cms.Sequence( process.pre_ana * process.CentFilter40_50 * process.VzFilter7)
process.pre_ana60Vz7 = cms.Sequence( process.pre_ana * process.CentFilter50_60 * process.VzFilter7)
process.pre_ana70Vz7 = cms.Sequence( process.pre_ana * process.CentFilter60_70 * process.VzFilter7)
process.pre_ana80Vz7 = cms.Sequence( process.pre_ana * process.CentFilter70_80 * process.VzFilter7)
process.pre_ana90Vz7 = cms.Sequence( process.pre_ana * process.CentFilter80_90 * process.VzFilter7)
process.pre_ana00Vz7 = cms.Sequence( process.pre_ana * process.CentFilter90_00 * process.VzFilter7)


process.pre_ana05Vz8 = cms.Sequence( process.pre_ana * process.CentFilter0_5   * process.VzFilter8)
process.pre_ana10Vz8 = cms.Sequence( process.pre_ana * process.CentFilter5_10  * process.VzFilter8)
process.pre_ana15Vz8 = cms.Sequence( process.pre_ana * process.CentFilter10_15 * process.VzFilter8)
process.pre_ana20Vz8 = cms.Sequence( process.pre_ana * process.CentFilter15_20 * process.VzFilter8)
process.pre_ana25Vz8 = cms.Sequence( process.pre_ana * process.CentFilter20_25 * process.VzFilter8)
process.pre_ana30Vz8 = cms.Sequence( process.pre_ana * process.CentFilter25_30 * process.VzFilter8)
process.pre_ana35Vz8 = cms.Sequence( process.pre_ana * process.CentFilter30_35 * process.VzFilter8)
process.pre_ana40Vz8 = cms.Sequence( process.pre_ana * process.CentFilter35_40 * process.VzFilter8)
process.pre_ana50Vz8 = cms.Sequence( process.pre_ana * process.CentFilter40_50 * process.VzFilter8)
process.pre_ana60Vz8 = cms.Sequence( process.pre_ana * process.CentFilter50_60 * process.VzFilter8)
process.pre_ana70Vz8 = cms.Sequence( process.pre_ana * process.CentFilter60_70 * process.VzFilter8)
process.pre_ana80Vz8 = cms.Sequence( process.pre_ana * process.CentFilter70_80 * process.VzFilter8)
process.pre_ana90Vz8 = cms.Sequence( process.pre_ana * process.CentFilter80_90 * process.VzFilter8)
process.pre_ana00Vz8 = cms.Sequence( process.pre_ana * process.CentFilter90_00 * process.VzFilter8)


process.pre_ana05Vz9 = cms.Sequence( process.pre_ana * process.CentFilter0_5   * process.VzFilter9)
process.pre_ana10Vz9 = cms.Sequence( process.pre_ana * process.CentFilter5_10  * process.VzFilter9)
process.pre_ana15Vz9 = cms.Sequence( process.pre_ana * process.CentFilter10_15 * process.VzFilter9)
process.pre_ana20Vz9 = cms.Sequence( process.pre_ana * process.CentFilter15_20 * process.VzFilter9)
process.pre_ana25Vz9 = cms.Sequence( process.pre_ana * process.CentFilter20_25 * process.VzFilter9)
process.pre_ana30Vz9 = cms.Sequence( process.pre_ana * process.CentFilter25_30 * process.VzFilter9)
process.pre_ana35Vz9 = cms.Sequence( process.pre_ana * process.CentFilter30_35 * process.VzFilter9)
process.pre_ana40Vz9 = cms.Sequence( process.pre_ana * process.CentFilter35_40 * process.VzFilter9)
process.pre_ana50Vz9 = cms.Sequence( process.pre_ana * process.CentFilter40_50 * process.VzFilter9)
process.pre_ana60Vz9 = cms.Sequence( process.pre_ana * process.CentFilter50_60 * process.VzFilter9)
process.pre_ana70Vz9 = cms.Sequence( process.pre_ana * process.CentFilter60_70 * process.VzFilter9)
process.pre_ana80Vz9 = cms.Sequence( process.pre_ana * process.CentFilter70_80 * process.VzFilter9)
process.pre_ana90Vz9 = cms.Sequence( process.pre_ana * process.CentFilter80_90 * process.VzFilter9)
process.pre_ana00Vz9 = cms.Sequence( process.pre_ana * process.CentFilter90_00 * process.VzFilter9)

## Vz0
process.ana05Vz0 = cms.Path(
		process.pre_ana05Vz0*
		process.QWAcc_Cent05Vz0_pT004 *
		process.QWAcc_Cent05Vz0_pT005 *
		process.QWAcc_Cent05Vz0_pT006 *
		process.QWAcc_Cent05Vz0_pT008 *
		process.QWAcc_Cent05Vz0_pT010 *
		process.QWAcc_Cent05Vz0_pT012 *
		process.QWAcc_Cent05Vz0_pT015 *
		process.QWAcc_Cent05Vz0_pT020 *
		process.QWAcc_Cent05Vz0_pT025 *
		process.QWAcc_Cent05Vz0_pT030 *
		process.QWAcc_Cent05Vz0_pT035 *
		process.QWAcc_Cent05Vz0_pT040 *
		process.QWAcc_Cent05Vz0_pT050 *
		process.QWAcc_Cent05Vz0_pT060 *
		process.QWAcc_Cent05Vz0_pT070 *
		process.QWAcc_Cent05Vz0_pT080 *
		process.QWAcc_Cent05Vz0_pT100 )

process.ana10Vz0 = cms.Path(
		process.pre_ana10Vz0*
		process.QWAcc_Cent10Vz0_pT004 *
		process.QWAcc_Cent10Vz0_pT005 *
		process.QWAcc_Cent10Vz0_pT006 *
		process.QWAcc_Cent10Vz0_pT008 *
		process.QWAcc_Cent10Vz0_pT010 *
		process.QWAcc_Cent10Vz0_pT012 *
		process.QWAcc_Cent10Vz0_pT015 *
		process.QWAcc_Cent10Vz0_pT020 *
		process.QWAcc_Cent10Vz0_pT025 *
		process.QWAcc_Cent10Vz0_pT030 *
		process.QWAcc_Cent10Vz0_pT035 *
		process.QWAcc_Cent10Vz0_pT040 *
		process.QWAcc_Cent10Vz0_pT050 *
		process.QWAcc_Cent10Vz0_pT060 *
		process.QWAcc_Cent10Vz0_pT070 *
		process.QWAcc_Cent10Vz0_pT080 *
		process.QWAcc_Cent10Vz0_pT100 )

process.ana15Vz0 = cms.Path(
		process.pre_ana15Vz0*
		process.QWAcc_Cent15Vz0_pT004 *
		process.QWAcc_Cent15Vz0_pT005 *
		process.QWAcc_Cent15Vz0_pT006 *
		process.QWAcc_Cent15Vz0_pT008 *
		process.QWAcc_Cent15Vz0_pT010 *
		process.QWAcc_Cent15Vz0_pT012 *
		process.QWAcc_Cent15Vz0_pT015 *
		process.QWAcc_Cent15Vz0_pT020 *
		process.QWAcc_Cent15Vz0_pT025 *
		process.QWAcc_Cent15Vz0_pT030 *
		process.QWAcc_Cent15Vz0_pT035 *
		process.QWAcc_Cent15Vz0_pT040 *
		process.QWAcc_Cent15Vz0_pT050 *
		process.QWAcc_Cent15Vz0_pT060 *
		process.QWAcc_Cent15Vz0_pT070 *
		process.QWAcc_Cent15Vz0_pT080 *
		process.QWAcc_Cent15Vz0_pT100 )


process.ana20Vz0 = cms.Path(
		process.pre_ana20Vz0*
		process.QWAcc_Cent20Vz0_pT004 *
		process.QWAcc_Cent20Vz0_pT005 *
		process.QWAcc_Cent20Vz0_pT006 *
		process.QWAcc_Cent20Vz0_pT008 *
		process.QWAcc_Cent20Vz0_pT010 *
		process.QWAcc_Cent20Vz0_pT012 *
		process.QWAcc_Cent20Vz0_pT015 *
		process.QWAcc_Cent20Vz0_pT020 *
		process.QWAcc_Cent20Vz0_pT025 *
		process.QWAcc_Cent20Vz0_pT030 *
		process.QWAcc_Cent20Vz0_pT035 *
		process.QWAcc_Cent20Vz0_pT040 *
		process.QWAcc_Cent20Vz0_pT050 *
		process.QWAcc_Cent20Vz0_pT060 *
		process.QWAcc_Cent20Vz0_pT070 *
		process.QWAcc_Cent20Vz0_pT080 *
		process.QWAcc_Cent20Vz0_pT100 )

process.ana25Vz0 = cms.Path(
		process.pre_ana25Vz0*
		process.QWAcc_Cent25Vz0_pT004 *
		process.QWAcc_Cent25Vz0_pT005 *
		process.QWAcc_Cent25Vz0_pT006 *
		process.QWAcc_Cent25Vz0_pT008 *
		process.QWAcc_Cent25Vz0_pT010 *
		process.QWAcc_Cent25Vz0_pT012 *
		process.QWAcc_Cent25Vz0_pT015 *
		process.QWAcc_Cent25Vz0_pT020 *
		process.QWAcc_Cent25Vz0_pT025 *
		process.QWAcc_Cent25Vz0_pT030 *
		process.QWAcc_Cent25Vz0_pT035 *
		process.QWAcc_Cent25Vz0_pT040 *
		process.QWAcc_Cent25Vz0_pT050 *
		process.QWAcc_Cent25Vz0_pT060 *
		process.QWAcc_Cent25Vz0_pT070 *
		process.QWAcc_Cent25Vz0_pT080 *
		process.QWAcc_Cent25Vz0_pT100 )

process.ana30Vz0 = cms.Path(
		process.pre_ana30Vz0*
		process.QWAcc_Cent30Vz0_pT004 *
		process.QWAcc_Cent30Vz0_pT005 *
		process.QWAcc_Cent30Vz0_pT006 *
		process.QWAcc_Cent30Vz0_pT008 *
		process.QWAcc_Cent30Vz0_pT010 *
		process.QWAcc_Cent30Vz0_pT012 *
		process.QWAcc_Cent30Vz0_pT015 *
		process.QWAcc_Cent30Vz0_pT020 *
		process.QWAcc_Cent30Vz0_pT025 *
		process.QWAcc_Cent30Vz0_pT030 *
		process.QWAcc_Cent30Vz0_pT035 *
		process.QWAcc_Cent30Vz0_pT040 *
		process.QWAcc_Cent30Vz0_pT050 *
		process.QWAcc_Cent30Vz0_pT060 *
		process.QWAcc_Cent30Vz0_pT070 *
		process.QWAcc_Cent30Vz0_pT080 *
		process.QWAcc_Cent30Vz0_pT100 )

process.ana35Vz0 = cms.Path(
		process.pre_ana35Vz0*
		process.QWAcc_Cent35Vz0_pT004 *
		process.QWAcc_Cent35Vz0_pT005 *
		process.QWAcc_Cent35Vz0_pT006 *
		process.QWAcc_Cent35Vz0_pT008 *
		process.QWAcc_Cent35Vz0_pT010 *
		process.QWAcc_Cent35Vz0_pT012 *
		process.QWAcc_Cent35Vz0_pT015 *
		process.QWAcc_Cent35Vz0_pT020 *
		process.QWAcc_Cent35Vz0_pT025 *
		process.QWAcc_Cent35Vz0_pT030 *
		process.QWAcc_Cent35Vz0_pT035 *
		process.QWAcc_Cent35Vz0_pT040 *
		process.QWAcc_Cent35Vz0_pT050 *
		process.QWAcc_Cent35Vz0_pT060 *
		process.QWAcc_Cent35Vz0_pT070 *
		process.QWAcc_Cent35Vz0_pT080 *
		process.QWAcc_Cent35Vz0_pT100 )

process.ana40Vz0 = cms.Path(
		process.pre_ana40Vz0*
		process.QWAcc_Cent40Vz0_pT004 *
		process.QWAcc_Cent40Vz0_pT005 *
		process.QWAcc_Cent40Vz0_pT006 *
		process.QWAcc_Cent40Vz0_pT008 *
		process.QWAcc_Cent40Vz0_pT010 *
		process.QWAcc_Cent40Vz0_pT012 *
		process.QWAcc_Cent40Vz0_pT015 *
		process.QWAcc_Cent40Vz0_pT020 *
		process.QWAcc_Cent40Vz0_pT025 *
		process.QWAcc_Cent40Vz0_pT030 *
		process.QWAcc_Cent40Vz0_pT035 *
		process.QWAcc_Cent40Vz0_pT040 *
		process.QWAcc_Cent40Vz0_pT050 *
		process.QWAcc_Cent40Vz0_pT060 *
		process.QWAcc_Cent40Vz0_pT070 *
		process.QWAcc_Cent40Vz0_pT080 *
		process.QWAcc_Cent40Vz0_pT100 )

process.ana50Vz0 = cms.Path(
		process.pre_ana50Vz0*
		process.QWAcc_Cent50Vz0_pT004 *
		process.QWAcc_Cent50Vz0_pT005 *
		process.QWAcc_Cent50Vz0_pT006 *
		process.QWAcc_Cent50Vz0_pT008 *
		process.QWAcc_Cent50Vz0_pT010 *
		process.QWAcc_Cent50Vz0_pT012 *
		process.QWAcc_Cent50Vz0_pT015 *
		process.QWAcc_Cent50Vz0_pT020 *
		process.QWAcc_Cent50Vz0_pT025 *
		process.QWAcc_Cent50Vz0_pT030 *
		process.QWAcc_Cent50Vz0_pT035 *
		process.QWAcc_Cent50Vz0_pT040 *
		process.QWAcc_Cent50Vz0_pT050 *
		process.QWAcc_Cent50Vz0_pT060 *
		process.QWAcc_Cent50Vz0_pT070 *
		process.QWAcc_Cent50Vz0_pT080 *
		process.QWAcc_Cent50Vz0_pT100 )


process.ana60Vz0 = cms.Path(
		process.pre_ana60Vz0*
		process.QWAcc_Cent60Vz0_pT004 *
		process.QWAcc_Cent60Vz0_pT005 *
		process.QWAcc_Cent60Vz0_pT006 *
		process.QWAcc_Cent60Vz0_pT008 *
		process.QWAcc_Cent60Vz0_pT010 *
		process.QWAcc_Cent60Vz0_pT012 *
		process.QWAcc_Cent60Vz0_pT015 *
		process.QWAcc_Cent60Vz0_pT020 *
		process.QWAcc_Cent60Vz0_pT025 *
		process.QWAcc_Cent60Vz0_pT030 *
		process.QWAcc_Cent60Vz0_pT035 *
		process.QWAcc_Cent60Vz0_pT040 *
		process.QWAcc_Cent60Vz0_pT050 *
		process.QWAcc_Cent60Vz0_pT060 *
		process.QWAcc_Cent60Vz0_pT070 *
		process.QWAcc_Cent60Vz0_pT080 *
		process.QWAcc_Cent60Vz0_pT100 )


process.ana70Vz0 = cms.Path(
		process.pre_ana70Vz0*
		process.QWAcc_Cent70Vz0_pT004 *
		process.QWAcc_Cent70Vz0_pT005 *
		process.QWAcc_Cent70Vz0_pT006 *
		process.QWAcc_Cent70Vz0_pT008 *
		process.QWAcc_Cent70Vz0_pT010 *
		process.QWAcc_Cent70Vz0_pT012 *
		process.QWAcc_Cent70Vz0_pT015 *
		process.QWAcc_Cent70Vz0_pT020 *
		process.QWAcc_Cent70Vz0_pT025 *
		process.QWAcc_Cent70Vz0_pT030 *
		process.QWAcc_Cent70Vz0_pT035 *
		process.QWAcc_Cent70Vz0_pT040 *
		process.QWAcc_Cent70Vz0_pT050 *
		process.QWAcc_Cent70Vz0_pT060 *
		process.QWAcc_Cent70Vz0_pT070 *
		process.QWAcc_Cent70Vz0_pT080 *
		process.QWAcc_Cent70Vz0_pT100 )


process.ana80Vz0 = cms.Path(
		process.pre_ana80Vz0*
		process.QWAcc_Cent80Vz0_pT004 *
		process.QWAcc_Cent80Vz0_pT005 *
		process.QWAcc_Cent80Vz0_pT006 *
		process.QWAcc_Cent80Vz0_pT008 *
		process.QWAcc_Cent80Vz0_pT010 *
		process.QWAcc_Cent80Vz0_pT012 *
		process.QWAcc_Cent80Vz0_pT015 *
		process.QWAcc_Cent80Vz0_pT020 *
		process.QWAcc_Cent80Vz0_pT025 *
		process.QWAcc_Cent80Vz0_pT030 *
		process.QWAcc_Cent80Vz0_pT035 *
		process.QWAcc_Cent80Vz0_pT040 *
		process.QWAcc_Cent80Vz0_pT050 *
		process.QWAcc_Cent80Vz0_pT060 *
		process.QWAcc_Cent80Vz0_pT070 *
		process.QWAcc_Cent80Vz0_pT080 *
		process.QWAcc_Cent80Vz0_pT100 )


process.ana90Vz0 = cms.Path(
		process.pre_ana90Vz0*
		process.QWAcc_Cent90Vz0_pT004 *
		process.QWAcc_Cent90Vz0_pT005 *
		process.QWAcc_Cent90Vz0_pT006 *
		process.QWAcc_Cent90Vz0_pT008 *
		process.QWAcc_Cent90Vz0_pT010 *
		process.QWAcc_Cent90Vz0_pT012 *
		process.QWAcc_Cent90Vz0_pT015 *
		process.QWAcc_Cent90Vz0_pT020 *
		process.QWAcc_Cent90Vz0_pT025 *
		process.QWAcc_Cent90Vz0_pT030 *
		process.QWAcc_Cent90Vz0_pT035 *
		process.QWAcc_Cent90Vz0_pT040 *
		process.QWAcc_Cent90Vz0_pT050 *
		process.QWAcc_Cent90Vz0_pT060 *
		process.QWAcc_Cent90Vz0_pT070 *
		process.QWAcc_Cent90Vz0_pT080 *
		process.QWAcc_Cent90Vz0_pT100 )


process.ana00Vz0 = cms.Path(
		process.pre_ana00Vz0*
		process.QWAcc_Cent00Vz0_pT004 *
		process.QWAcc_Cent00Vz0_pT005 *
		process.QWAcc_Cent00Vz0_pT006 *
		process.QWAcc_Cent00Vz0_pT008 *
		process.QWAcc_Cent00Vz0_pT010 *
		process.QWAcc_Cent00Vz0_pT012 *
		process.QWAcc_Cent00Vz0_pT015 *
		process.QWAcc_Cent00Vz0_pT020 *
		process.QWAcc_Cent00Vz0_pT025 *
		process.QWAcc_Cent00Vz0_pT030 *
		process.QWAcc_Cent00Vz0_pT035 *
		process.QWAcc_Cent00Vz0_pT040 *
		process.QWAcc_Cent00Vz0_pT050 *
		process.QWAcc_Cent00Vz0_pT060 *
		process.QWAcc_Cent00Vz0_pT070 *
		process.QWAcc_Cent00Vz0_pT080 *
		process.QWAcc_Cent00Vz0_pT100 )


## Vz1
process.ana05Vz1 = cms.Path(
		process.pre_ana05Vz1*
		process.QWAcc_Cent05Vz1_pT004 *
		process.QWAcc_Cent05Vz1_pT005 *
		process.QWAcc_Cent05Vz1_pT006 *
		process.QWAcc_Cent05Vz1_pT008 *
		process.QWAcc_Cent05Vz1_pT010 *
		process.QWAcc_Cent05Vz1_pT012 *
		process.QWAcc_Cent05Vz1_pT015 *
		process.QWAcc_Cent05Vz1_pT020 *
		process.QWAcc_Cent05Vz1_pT025 *
		process.QWAcc_Cent05Vz1_pT030 *
		process.QWAcc_Cent05Vz1_pT035 *
		process.QWAcc_Cent05Vz1_pT040 *
		process.QWAcc_Cent05Vz1_pT050 *
		process.QWAcc_Cent05Vz1_pT060 *
		process.QWAcc_Cent05Vz1_pT070 *
		process.QWAcc_Cent05Vz1_pT080 *
		process.QWAcc_Cent05Vz1_pT100 )

process.ana10Vz1 = cms.Path(
		process.pre_ana10Vz1*
		process.QWAcc_Cent10Vz1_pT004 *
		process.QWAcc_Cent10Vz1_pT005 *
		process.QWAcc_Cent10Vz1_pT006 *
		process.QWAcc_Cent10Vz1_pT008 *
		process.QWAcc_Cent10Vz1_pT010 *
		process.QWAcc_Cent10Vz1_pT012 *
		process.QWAcc_Cent10Vz1_pT015 *
		process.QWAcc_Cent10Vz1_pT020 *
		process.QWAcc_Cent10Vz1_pT025 *
		process.QWAcc_Cent10Vz1_pT030 *
		process.QWAcc_Cent10Vz1_pT035 *
		process.QWAcc_Cent10Vz1_pT040 *
		process.QWAcc_Cent10Vz1_pT050 *
		process.QWAcc_Cent10Vz1_pT060 *
		process.QWAcc_Cent10Vz1_pT070 *
		process.QWAcc_Cent10Vz1_pT080 *
		process.QWAcc_Cent10Vz1_pT100 )

process.ana15Vz1 = cms.Path(
		process.pre_ana15Vz1*
		process.QWAcc_Cent15Vz1_pT004 *
		process.QWAcc_Cent15Vz1_pT005 *
		process.QWAcc_Cent15Vz1_pT006 *
		process.QWAcc_Cent15Vz1_pT008 *
		process.QWAcc_Cent15Vz1_pT010 *
		process.QWAcc_Cent15Vz1_pT012 *
		process.QWAcc_Cent15Vz1_pT015 *
		process.QWAcc_Cent15Vz1_pT020 *
		process.QWAcc_Cent15Vz1_pT025 *
		process.QWAcc_Cent15Vz1_pT030 *
		process.QWAcc_Cent15Vz1_pT035 *
		process.QWAcc_Cent15Vz1_pT040 *
		process.QWAcc_Cent15Vz1_pT050 *
		process.QWAcc_Cent15Vz1_pT060 *
		process.QWAcc_Cent15Vz1_pT070 *
		process.QWAcc_Cent15Vz1_pT080 *
		process.QWAcc_Cent15Vz1_pT100 )


process.ana20Vz1 = cms.Path(
		process.pre_ana20Vz1*
		process.QWAcc_Cent20Vz1_pT004 *
		process.QWAcc_Cent20Vz1_pT005 *
		process.QWAcc_Cent20Vz1_pT006 *
		process.QWAcc_Cent20Vz1_pT008 *
		process.QWAcc_Cent20Vz1_pT010 *
		process.QWAcc_Cent20Vz1_pT012 *
		process.QWAcc_Cent20Vz1_pT015 *
		process.QWAcc_Cent20Vz1_pT020 *
		process.QWAcc_Cent20Vz1_pT025 *
		process.QWAcc_Cent20Vz1_pT030 *
		process.QWAcc_Cent20Vz1_pT035 *
		process.QWAcc_Cent20Vz1_pT040 *
		process.QWAcc_Cent20Vz1_pT050 *
		process.QWAcc_Cent20Vz1_pT060 *
		process.QWAcc_Cent20Vz1_pT070 *
		process.QWAcc_Cent20Vz1_pT080 *
		process.QWAcc_Cent20Vz1_pT100 )

process.ana25Vz1 = cms.Path(
		process.pre_ana25Vz1*
		process.QWAcc_Cent25Vz1_pT004 *
		process.QWAcc_Cent25Vz1_pT005 *
		process.QWAcc_Cent25Vz1_pT006 *
		process.QWAcc_Cent25Vz1_pT008 *
		process.QWAcc_Cent25Vz1_pT010 *
		process.QWAcc_Cent25Vz1_pT012 *
		process.QWAcc_Cent25Vz1_pT015 *
		process.QWAcc_Cent25Vz1_pT020 *
		process.QWAcc_Cent25Vz1_pT025 *
		process.QWAcc_Cent25Vz1_pT030 *
		process.QWAcc_Cent25Vz1_pT035 *
		process.QWAcc_Cent25Vz1_pT040 *
		process.QWAcc_Cent25Vz1_pT050 *
		process.QWAcc_Cent25Vz1_pT060 *
		process.QWAcc_Cent25Vz1_pT070 *
		process.QWAcc_Cent25Vz1_pT080 *
		process.QWAcc_Cent25Vz1_pT100 )

process.ana30Vz1 = cms.Path(
		process.pre_ana30Vz1*
		process.QWAcc_Cent30Vz1_pT004 *
		process.QWAcc_Cent30Vz1_pT005 *
		process.QWAcc_Cent30Vz1_pT006 *
		process.QWAcc_Cent30Vz1_pT008 *
		process.QWAcc_Cent30Vz1_pT010 *
		process.QWAcc_Cent30Vz1_pT012 *
		process.QWAcc_Cent30Vz1_pT015 *
		process.QWAcc_Cent30Vz1_pT020 *
		process.QWAcc_Cent30Vz1_pT025 *
		process.QWAcc_Cent30Vz1_pT030 *
		process.QWAcc_Cent30Vz1_pT035 *
		process.QWAcc_Cent30Vz1_pT040 *
		process.QWAcc_Cent30Vz1_pT050 *
		process.QWAcc_Cent30Vz1_pT060 *
		process.QWAcc_Cent30Vz1_pT070 *
		process.QWAcc_Cent30Vz1_pT080 *
		process.QWAcc_Cent30Vz1_pT100 )

process.ana35Vz1 = cms.Path(
		process.pre_ana35Vz1*
		process.QWAcc_Cent35Vz1_pT004 *
		process.QWAcc_Cent35Vz1_pT005 *
		process.QWAcc_Cent35Vz1_pT006 *
		process.QWAcc_Cent35Vz1_pT008 *
		process.QWAcc_Cent35Vz1_pT010 *
		process.QWAcc_Cent35Vz1_pT012 *
		process.QWAcc_Cent35Vz1_pT015 *
		process.QWAcc_Cent35Vz1_pT020 *
		process.QWAcc_Cent35Vz1_pT025 *
		process.QWAcc_Cent35Vz1_pT030 *
		process.QWAcc_Cent35Vz1_pT035 *
		process.QWAcc_Cent35Vz1_pT040 *
		process.QWAcc_Cent35Vz1_pT050 *
		process.QWAcc_Cent35Vz1_pT060 *
		process.QWAcc_Cent35Vz1_pT070 *
		process.QWAcc_Cent35Vz1_pT080 *
		process.QWAcc_Cent35Vz1_pT100 )

process.ana40Vz1 = cms.Path(
		process.pre_ana40Vz1*
		process.QWAcc_Cent40Vz1_pT004 *
		process.QWAcc_Cent40Vz1_pT005 *
		process.QWAcc_Cent40Vz1_pT006 *
		process.QWAcc_Cent40Vz1_pT008 *
		process.QWAcc_Cent40Vz1_pT010 *
		process.QWAcc_Cent40Vz1_pT012 *
		process.QWAcc_Cent40Vz1_pT015 *
		process.QWAcc_Cent40Vz1_pT020 *
		process.QWAcc_Cent40Vz1_pT025 *
		process.QWAcc_Cent40Vz1_pT030 *
		process.QWAcc_Cent40Vz1_pT035 *
		process.QWAcc_Cent40Vz1_pT040 *
		process.QWAcc_Cent40Vz1_pT050 *
		process.QWAcc_Cent40Vz1_pT060 *
		process.QWAcc_Cent40Vz1_pT070 *
		process.QWAcc_Cent40Vz1_pT080 *
		process.QWAcc_Cent40Vz1_pT100 )

process.ana50Vz1 = cms.Path(
		process.pre_ana50Vz1*
		process.QWAcc_Cent50Vz1_pT004 *
		process.QWAcc_Cent50Vz1_pT005 *
		process.QWAcc_Cent50Vz1_pT006 *
		process.QWAcc_Cent50Vz1_pT008 *
		process.QWAcc_Cent50Vz1_pT010 *
		process.QWAcc_Cent50Vz1_pT012 *
		process.QWAcc_Cent50Vz1_pT015 *
		process.QWAcc_Cent50Vz1_pT020 *
		process.QWAcc_Cent50Vz1_pT025 *
		process.QWAcc_Cent50Vz1_pT030 *
		process.QWAcc_Cent50Vz1_pT035 *
		process.QWAcc_Cent50Vz1_pT040 *
		process.QWAcc_Cent50Vz1_pT050 *
		process.QWAcc_Cent50Vz1_pT060 *
		process.QWAcc_Cent50Vz1_pT070 *
		process.QWAcc_Cent50Vz1_pT080 *
		process.QWAcc_Cent50Vz1_pT100 )


process.ana60Vz1 = cms.Path(
		process.pre_ana60Vz1*
		process.QWAcc_Cent60Vz1_pT004 *
		process.QWAcc_Cent60Vz1_pT005 *
		process.QWAcc_Cent60Vz1_pT006 *
		process.QWAcc_Cent60Vz1_pT008 *
		process.QWAcc_Cent60Vz1_pT010 *
		process.QWAcc_Cent60Vz1_pT012 *
		process.QWAcc_Cent60Vz1_pT015 *
		process.QWAcc_Cent60Vz1_pT020 *
		process.QWAcc_Cent60Vz1_pT025 *
		process.QWAcc_Cent60Vz1_pT030 *
		process.QWAcc_Cent60Vz1_pT035 *
		process.QWAcc_Cent60Vz1_pT040 *
		process.QWAcc_Cent60Vz1_pT050 *
		process.QWAcc_Cent60Vz1_pT060 *
		process.QWAcc_Cent60Vz1_pT070 *
		process.QWAcc_Cent60Vz1_pT080 *
		process.QWAcc_Cent60Vz1_pT100 )


process.ana70Vz1 = cms.Path(
		process.pre_ana70Vz1*
		process.QWAcc_Cent70Vz1_pT004 *
		process.QWAcc_Cent70Vz1_pT005 *
		process.QWAcc_Cent70Vz1_pT006 *
		process.QWAcc_Cent70Vz1_pT008 *
		process.QWAcc_Cent70Vz1_pT010 *
		process.QWAcc_Cent70Vz1_pT012 *
		process.QWAcc_Cent70Vz1_pT015 *
		process.QWAcc_Cent70Vz1_pT020 *
		process.QWAcc_Cent70Vz1_pT025 *
		process.QWAcc_Cent70Vz1_pT030 *
		process.QWAcc_Cent70Vz1_pT035 *
		process.QWAcc_Cent70Vz1_pT040 *
		process.QWAcc_Cent70Vz1_pT050 *
		process.QWAcc_Cent70Vz1_pT060 *
		process.QWAcc_Cent70Vz1_pT070 *
		process.QWAcc_Cent70Vz1_pT080 *
		process.QWAcc_Cent70Vz1_pT100 )


process.ana80Vz1 = cms.Path(
		process.pre_ana80Vz1*
		process.QWAcc_Cent80Vz1_pT004 *
		process.QWAcc_Cent80Vz1_pT005 *
		process.QWAcc_Cent80Vz1_pT006 *
		process.QWAcc_Cent80Vz1_pT008 *
		process.QWAcc_Cent80Vz1_pT010 *
		process.QWAcc_Cent80Vz1_pT012 *
		process.QWAcc_Cent80Vz1_pT015 *
		process.QWAcc_Cent80Vz1_pT020 *
		process.QWAcc_Cent80Vz1_pT025 *
		process.QWAcc_Cent80Vz1_pT030 *
		process.QWAcc_Cent80Vz1_pT035 *
		process.QWAcc_Cent80Vz1_pT040 *
		process.QWAcc_Cent80Vz1_pT050 *
		process.QWAcc_Cent80Vz1_pT060 *
		process.QWAcc_Cent80Vz1_pT070 *
		process.QWAcc_Cent80Vz1_pT080 *
		process.QWAcc_Cent80Vz1_pT100 )


process.ana90Vz1 = cms.Path(
		process.pre_ana90Vz1*
		process.QWAcc_Cent90Vz1_pT004 *
		process.QWAcc_Cent90Vz1_pT005 *
		process.QWAcc_Cent90Vz1_pT006 *
		process.QWAcc_Cent90Vz1_pT008 *
		process.QWAcc_Cent90Vz1_pT010 *
		process.QWAcc_Cent90Vz1_pT012 *
		process.QWAcc_Cent90Vz1_pT015 *
		process.QWAcc_Cent90Vz1_pT020 *
		process.QWAcc_Cent90Vz1_pT025 *
		process.QWAcc_Cent90Vz1_pT030 *
		process.QWAcc_Cent90Vz1_pT035 *
		process.QWAcc_Cent90Vz1_pT040 *
		process.QWAcc_Cent90Vz1_pT050 *
		process.QWAcc_Cent90Vz1_pT060 *
		process.QWAcc_Cent90Vz1_pT070 *
		process.QWAcc_Cent90Vz1_pT080 *
		process.QWAcc_Cent90Vz1_pT100 )


process.ana00Vz1 = cms.Path(
		process.pre_ana00Vz1*
		process.QWAcc_Cent00Vz1_pT004 *
		process.QWAcc_Cent00Vz1_pT005 *
		process.QWAcc_Cent00Vz1_pT006 *
		process.QWAcc_Cent00Vz1_pT008 *
		process.QWAcc_Cent00Vz1_pT010 *
		process.QWAcc_Cent00Vz1_pT012 *
		process.QWAcc_Cent00Vz1_pT015 *
		process.QWAcc_Cent00Vz1_pT020 *
		process.QWAcc_Cent00Vz1_pT025 *
		process.QWAcc_Cent00Vz1_pT030 *
		process.QWAcc_Cent00Vz1_pT035 *
		process.QWAcc_Cent00Vz1_pT040 *
		process.QWAcc_Cent00Vz1_pT050 *
		process.QWAcc_Cent00Vz1_pT060 *
		process.QWAcc_Cent00Vz1_pT070 *
		process.QWAcc_Cent00Vz1_pT080 *
		process.QWAcc_Cent00Vz1_pT100 )


## Vz2
process.ana05Vz2 = cms.Path(
		process.pre_ana05Vz2*
		process.QWAcc_Cent05Vz2_pT004 *
		process.QWAcc_Cent05Vz2_pT005 *
		process.QWAcc_Cent05Vz2_pT006 *
		process.QWAcc_Cent05Vz2_pT008 *
		process.QWAcc_Cent05Vz2_pT010 *
		process.QWAcc_Cent05Vz2_pT012 *
		process.QWAcc_Cent05Vz2_pT015 *
		process.QWAcc_Cent05Vz2_pT020 *
		process.QWAcc_Cent05Vz2_pT025 *
		process.QWAcc_Cent05Vz2_pT030 *
		process.QWAcc_Cent05Vz2_pT035 *
		process.QWAcc_Cent05Vz2_pT040 *
		process.QWAcc_Cent05Vz2_pT050 *
		process.QWAcc_Cent05Vz2_pT060 *
		process.QWAcc_Cent05Vz2_pT070 *
		process.QWAcc_Cent05Vz2_pT080 *
		process.QWAcc_Cent05Vz2_pT100 )

process.ana10Vz2 = cms.Path(
		process.pre_ana10Vz2*
		process.QWAcc_Cent10Vz2_pT004 *
		process.QWAcc_Cent10Vz2_pT005 *
		process.QWAcc_Cent10Vz2_pT006 *
		process.QWAcc_Cent10Vz2_pT008 *
		process.QWAcc_Cent10Vz2_pT010 *
		process.QWAcc_Cent10Vz2_pT012 *
		process.QWAcc_Cent10Vz2_pT015 *
		process.QWAcc_Cent10Vz2_pT020 *
		process.QWAcc_Cent10Vz2_pT025 *
		process.QWAcc_Cent10Vz2_pT030 *
		process.QWAcc_Cent10Vz2_pT035 *
		process.QWAcc_Cent10Vz2_pT040 *
		process.QWAcc_Cent10Vz2_pT050 *
		process.QWAcc_Cent10Vz2_pT060 *
		process.QWAcc_Cent10Vz2_pT070 *
		process.QWAcc_Cent10Vz2_pT080 *
		process.QWAcc_Cent10Vz2_pT100 )

process.ana15Vz2 = cms.Path(
		process.pre_ana15Vz2*
		process.QWAcc_Cent15Vz2_pT004 *
		process.QWAcc_Cent15Vz2_pT005 *
		process.QWAcc_Cent15Vz2_pT006 *
		process.QWAcc_Cent15Vz2_pT008 *
		process.QWAcc_Cent15Vz2_pT010 *
		process.QWAcc_Cent15Vz2_pT012 *
		process.QWAcc_Cent15Vz2_pT015 *
		process.QWAcc_Cent15Vz2_pT020 *
		process.QWAcc_Cent15Vz2_pT025 *
		process.QWAcc_Cent15Vz2_pT030 *
		process.QWAcc_Cent15Vz2_pT035 *
		process.QWAcc_Cent15Vz2_pT040 *
		process.QWAcc_Cent15Vz2_pT050 *
		process.QWAcc_Cent15Vz2_pT060 *
		process.QWAcc_Cent15Vz2_pT070 *
		process.QWAcc_Cent15Vz2_pT080 *
		process.QWAcc_Cent15Vz2_pT100 )


process.ana20Vz2 = cms.Path(
		process.pre_ana20Vz2*
		process.QWAcc_Cent20Vz2_pT004 *
		process.QWAcc_Cent20Vz2_pT005 *
		process.QWAcc_Cent20Vz2_pT006 *
		process.QWAcc_Cent20Vz2_pT008 *
		process.QWAcc_Cent20Vz2_pT010 *
		process.QWAcc_Cent20Vz2_pT012 *
		process.QWAcc_Cent20Vz2_pT015 *
		process.QWAcc_Cent20Vz2_pT020 *
		process.QWAcc_Cent20Vz2_pT025 *
		process.QWAcc_Cent20Vz2_pT030 *
		process.QWAcc_Cent20Vz2_pT035 *
		process.QWAcc_Cent20Vz2_pT040 *
		process.QWAcc_Cent20Vz2_pT050 *
		process.QWAcc_Cent20Vz2_pT060 *
		process.QWAcc_Cent20Vz2_pT070 *
		process.QWAcc_Cent20Vz2_pT080 *
		process.QWAcc_Cent20Vz2_pT100 )

process.ana25Vz2 = cms.Path(
		process.pre_ana25Vz2*
		process.QWAcc_Cent25Vz2_pT004 *
		process.QWAcc_Cent25Vz2_pT005 *
		process.QWAcc_Cent25Vz2_pT006 *
		process.QWAcc_Cent25Vz2_pT008 *
		process.QWAcc_Cent25Vz2_pT010 *
		process.QWAcc_Cent25Vz2_pT012 *
		process.QWAcc_Cent25Vz2_pT015 *
		process.QWAcc_Cent25Vz2_pT020 *
		process.QWAcc_Cent25Vz2_pT025 *
		process.QWAcc_Cent25Vz2_pT030 *
		process.QWAcc_Cent25Vz2_pT035 *
		process.QWAcc_Cent25Vz2_pT040 *
		process.QWAcc_Cent25Vz2_pT050 *
		process.QWAcc_Cent25Vz2_pT060 *
		process.QWAcc_Cent25Vz2_pT070 *
		process.QWAcc_Cent25Vz2_pT080 *
		process.QWAcc_Cent25Vz2_pT100 )

process.ana30Vz2 = cms.Path(
		process.pre_ana30Vz2*
		process.QWAcc_Cent30Vz2_pT004 *
		process.QWAcc_Cent30Vz2_pT005 *
		process.QWAcc_Cent30Vz2_pT006 *
		process.QWAcc_Cent30Vz2_pT008 *
		process.QWAcc_Cent30Vz2_pT010 *
		process.QWAcc_Cent30Vz2_pT012 *
		process.QWAcc_Cent30Vz2_pT015 *
		process.QWAcc_Cent30Vz2_pT020 *
		process.QWAcc_Cent30Vz2_pT025 *
		process.QWAcc_Cent30Vz2_pT030 *
		process.QWAcc_Cent30Vz2_pT035 *
		process.QWAcc_Cent30Vz2_pT040 *
		process.QWAcc_Cent30Vz2_pT050 *
		process.QWAcc_Cent30Vz2_pT060 *
		process.QWAcc_Cent30Vz2_pT070 *
		process.QWAcc_Cent30Vz2_pT080 *
		process.QWAcc_Cent30Vz2_pT100 )

process.ana35Vz2 = cms.Path(
		process.pre_ana35Vz2*
		process.QWAcc_Cent35Vz2_pT004 *
		process.QWAcc_Cent35Vz2_pT005 *
		process.QWAcc_Cent35Vz2_pT006 *
		process.QWAcc_Cent35Vz2_pT008 *
		process.QWAcc_Cent35Vz2_pT010 *
		process.QWAcc_Cent35Vz2_pT012 *
		process.QWAcc_Cent35Vz2_pT015 *
		process.QWAcc_Cent35Vz2_pT020 *
		process.QWAcc_Cent35Vz2_pT025 *
		process.QWAcc_Cent35Vz2_pT030 *
		process.QWAcc_Cent35Vz2_pT035 *
		process.QWAcc_Cent35Vz2_pT040 *
		process.QWAcc_Cent35Vz2_pT050 *
		process.QWAcc_Cent35Vz2_pT060 *
		process.QWAcc_Cent35Vz2_pT070 *
		process.QWAcc_Cent35Vz2_pT080 *
		process.QWAcc_Cent35Vz2_pT100 )

process.ana40Vz2 = cms.Path(
		process.pre_ana40Vz2*
		process.QWAcc_Cent40Vz2_pT004 *
		process.QWAcc_Cent40Vz2_pT005 *
		process.QWAcc_Cent40Vz2_pT006 *
		process.QWAcc_Cent40Vz2_pT008 *
		process.QWAcc_Cent40Vz2_pT010 *
		process.QWAcc_Cent40Vz2_pT012 *
		process.QWAcc_Cent40Vz2_pT015 *
		process.QWAcc_Cent40Vz2_pT020 *
		process.QWAcc_Cent40Vz2_pT025 *
		process.QWAcc_Cent40Vz2_pT030 *
		process.QWAcc_Cent40Vz2_pT035 *
		process.QWAcc_Cent40Vz2_pT040 *
		process.QWAcc_Cent40Vz2_pT050 *
		process.QWAcc_Cent40Vz2_pT060 *
		process.QWAcc_Cent40Vz2_pT070 *
		process.QWAcc_Cent40Vz2_pT080 *
		process.QWAcc_Cent40Vz2_pT100 )

process.ana50Vz2 = cms.Path(
		process.pre_ana50Vz2*
		process.QWAcc_Cent50Vz2_pT004 *
		process.QWAcc_Cent50Vz2_pT005 *
		process.QWAcc_Cent50Vz2_pT006 *
		process.QWAcc_Cent50Vz2_pT008 *
		process.QWAcc_Cent50Vz2_pT010 *
		process.QWAcc_Cent50Vz2_pT012 *
		process.QWAcc_Cent50Vz2_pT015 *
		process.QWAcc_Cent50Vz2_pT020 *
		process.QWAcc_Cent50Vz2_pT025 *
		process.QWAcc_Cent50Vz2_pT030 *
		process.QWAcc_Cent50Vz2_pT035 *
		process.QWAcc_Cent50Vz2_pT040 *
		process.QWAcc_Cent50Vz2_pT050 *
		process.QWAcc_Cent50Vz2_pT060 *
		process.QWAcc_Cent50Vz2_pT070 *
		process.QWAcc_Cent50Vz2_pT080 *
		process.QWAcc_Cent50Vz2_pT100 )


process.ana60Vz2 = cms.Path(
		process.pre_ana60Vz2*
		process.QWAcc_Cent60Vz2_pT004 *
		process.QWAcc_Cent60Vz2_pT005 *
		process.QWAcc_Cent60Vz2_pT006 *
		process.QWAcc_Cent60Vz2_pT008 *
		process.QWAcc_Cent60Vz2_pT010 *
		process.QWAcc_Cent60Vz2_pT012 *
		process.QWAcc_Cent60Vz2_pT015 *
		process.QWAcc_Cent60Vz2_pT020 *
		process.QWAcc_Cent60Vz2_pT025 *
		process.QWAcc_Cent60Vz2_pT030 *
		process.QWAcc_Cent60Vz2_pT035 *
		process.QWAcc_Cent60Vz2_pT040 *
		process.QWAcc_Cent60Vz2_pT050 *
		process.QWAcc_Cent60Vz2_pT060 *
		process.QWAcc_Cent60Vz2_pT070 *
		process.QWAcc_Cent60Vz2_pT080 *
		process.QWAcc_Cent60Vz2_pT100 )


process.ana70Vz2 = cms.Path(
		process.pre_ana70Vz2*
		process.QWAcc_Cent70Vz2_pT004 *
		process.QWAcc_Cent70Vz2_pT005 *
		process.QWAcc_Cent70Vz2_pT006 *
		process.QWAcc_Cent70Vz2_pT008 *
		process.QWAcc_Cent70Vz2_pT010 *
		process.QWAcc_Cent70Vz2_pT012 *
		process.QWAcc_Cent70Vz2_pT015 *
		process.QWAcc_Cent70Vz2_pT020 *
		process.QWAcc_Cent70Vz2_pT025 *
		process.QWAcc_Cent70Vz2_pT030 *
		process.QWAcc_Cent70Vz2_pT035 *
		process.QWAcc_Cent70Vz2_pT040 *
		process.QWAcc_Cent70Vz2_pT050 *
		process.QWAcc_Cent70Vz2_pT060 *
		process.QWAcc_Cent70Vz2_pT070 *
		process.QWAcc_Cent70Vz2_pT080 *
		process.QWAcc_Cent70Vz2_pT100 )


process.ana80Vz2 = cms.Path(
		process.pre_ana80Vz2*
		process.QWAcc_Cent80Vz2_pT004 *
		process.QWAcc_Cent80Vz2_pT005 *
		process.QWAcc_Cent80Vz2_pT006 *
		process.QWAcc_Cent80Vz2_pT008 *
		process.QWAcc_Cent80Vz2_pT010 *
		process.QWAcc_Cent80Vz2_pT012 *
		process.QWAcc_Cent80Vz2_pT015 *
		process.QWAcc_Cent80Vz2_pT020 *
		process.QWAcc_Cent80Vz2_pT025 *
		process.QWAcc_Cent80Vz2_pT030 *
		process.QWAcc_Cent80Vz2_pT035 *
		process.QWAcc_Cent80Vz2_pT040 *
		process.QWAcc_Cent80Vz2_pT050 *
		process.QWAcc_Cent80Vz2_pT060 *
		process.QWAcc_Cent80Vz2_pT070 *
		process.QWAcc_Cent80Vz2_pT080 *
		process.QWAcc_Cent80Vz2_pT100 )


process.ana90Vz2 = cms.Path(
		process.pre_ana90Vz2*
		process.QWAcc_Cent90Vz2_pT004 *
		process.QWAcc_Cent90Vz2_pT005 *
		process.QWAcc_Cent90Vz2_pT006 *
		process.QWAcc_Cent90Vz2_pT008 *
		process.QWAcc_Cent90Vz2_pT010 *
		process.QWAcc_Cent90Vz2_pT012 *
		process.QWAcc_Cent90Vz2_pT015 *
		process.QWAcc_Cent90Vz2_pT020 *
		process.QWAcc_Cent90Vz2_pT025 *
		process.QWAcc_Cent90Vz2_pT030 *
		process.QWAcc_Cent90Vz2_pT035 *
		process.QWAcc_Cent90Vz2_pT040 *
		process.QWAcc_Cent90Vz2_pT050 *
		process.QWAcc_Cent90Vz2_pT060 *
		process.QWAcc_Cent90Vz2_pT070 *
		process.QWAcc_Cent90Vz2_pT080 *
		process.QWAcc_Cent90Vz2_pT100 )


process.ana00Vz2 = cms.Path(
		process.pre_ana00Vz2*
		process.QWAcc_Cent00Vz2_pT004 *
		process.QWAcc_Cent00Vz2_pT005 *
		process.QWAcc_Cent00Vz2_pT006 *
		process.QWAcc_Cent00Vz2_pT008 *
		process.QWAcc_Cent00Vz2_pT010 *
		process.QWAcc_Cent00Vz2_pT012 *
		process.QWAcc_Cent00Vz2_pT015 *
		process.QWAcc_Cent00Vz2_pT020 *
		process.QWAcc_Cent00Vz2_pT025 *
		process.QWAcc_Cent00Vz2_pT030 *
		process.QWAcc_Cent00Vz2_pT035 *
		process.QWAcc_Cent00Vz2_pT040 *
		process.QWAcc_Cent00Vz2_pT050 *
		process.QWAcc_Cent00Vz2_pT060 *
		process.QWAcc_Cent00Vz2_pT070 *
		process.QWAcc_Cent00Vz2_pT080 *
		process.QWAcc_Cent00Vz2_pT100 )


## Vz3
process.ana05Vz3 = cms.Path(
		process.pre_ana05Vz3*
		process.QWAcc_Cent05Vz3_pT004 *
		process.QWAcc_Cent05Vz3_pT005 *
		process.QWAcc_Cent05Vz3_pT006 *
		process.QWAcc_Cent05Vz3_pT008 *
		process.QWAcc_Cent05Vz3_pT010 *
		process.QWAcc_Cent05Vz3_pT012 *
		process.QWAcc_Cent05Vz3_pT015 *
		process.QWAcc_Cent05Vz3_pT020 *
		process.QWAcc_Cent05Vz3_pT025 *
		process.QWAcc_Cent05Vz3_pT030 *
		process.QWAcc_Cent05Vz3_pT035 *
		process.QWAcc_Cent05Vz3_pT040 *
		process.QWAcc_Cent05Vz3_pT050 *
		process.QWAcc_Cent05Vz3_pT060 *
		process.QWAcc_Cent05Vz3_pT070 *
		process.QWAcc_Cent05Vz3_pT080 *
		process.QWAcc_Cent05Vz3_pT100 )

process.ana10Vz3 = cms.Path(
		process.pre_ana10Vz3*
		process.QWAcc_Cent10Vz3_pT004 *
		process.QWAcc_Cent10Vz3_pT005 *
		process.QWAcc_Cent10Vz3_pT006 *
		process.QWAcc_Cent10Vz3_pT008 *
		process.QWAcc_Cent10Vz3_pT010 *
		process.QWAcc_Cent10Vz3_pT012 *
		process.QWAcc_Cent10Vz3_pT015 *
		process.QWAcc_Cent10Vz3_pT020 *
		process.QWAcc_Cent10Vz3_pT025 *
		process.QWAcc_Cent10Vz3_pT030 *
		process.QWAcc_Cent10Vz3_pT035 *
		process.QWAcc_Cent10Vz3_pT040 *
		process.QWAcc_Cent10Vz3_pT050 *
		process.QWAcc_Cent10Vz3_pT060 *
		process.QWAcc_Cent10Vz3_pT070 *
		process.QWAcc_Cent10Vz3_pT080 *
		process.QWAcc_Cent10Vz3_pT100 )

process.ana15Vz3 = cms.Path(
		process.pre_ana15Vz3*
		process.QWAcc_Cent15Vz3_pT004 *
		process.QWAcc_Cent15Vz3_pT005 *
		process.QWAcc_Cent15Vz3_pT006 *
		process.QWAcc_Cent15Vz3_pT008 *
		process.QWAcc_Cent15Vz3_pT010 *
		process.QWAcc_Cent15Vz3_pT012 *
		process.QWAcc_Cent15Vz3_pT015 *
		process.QWAcc_Cent15Vz3_pT020 *
		process.QWAcc_Cent15Vz3_pT025 *
		process.QWAcc_Cent15Vz3_pT030 *
		process.QWAcc_Cent15Vz3_pT035 *
		process.QWAcc_Cent15Vz3_pT040 *
		process.QWAcc_Cent15Vz3_pT050 *
		process.QWAcc_Cent15Vz3_pT060 *
		process.QWAcc_Cent15Vz3_pT070 *
		process.QWAcc_Cent15Vz3_pT080 *
		process.QWAcc_Cent15Vz3_pT100 )


process.ana20Vz3 = cms.Path(
		process.pre_ana20Vz3*
		process.QWAcc_Cent20Vz3_pT004 *
		process.QWAcc_Cent20Vz3_pT005 *
		process.QWAcc_Cent20Vz3_pT006 *
		process.QWAcc_Cent20Vz3_pT008 *
		process.QWAcc_Cent20Vz3_pT010 *
		process.QWAcc_Cent20Vz3_pT012 *
		process.QWAcc_Cent20Vz3_pT015 *
		process.QWAcc_Cent20Vz3_pT020 *
		process.QWAcc_Cent20Vz3_pT025 *
		process.QWAcc_Cent20Vz3_pT030 *
		process.QWAcc_Cent20Vz3_pT035 *
		process.QWAcc_Cent20Vz3_pT040 *
		process.QWAcc_Cent20Vz3_pT050 *
		process.QWAcc_Cent20Vz3_pT060 *
		process.QWAcc_Cent20Vz3_pT070 *
		process.QWAcc_Cent20Vz3_pT080 *
		process.QWAcc_Cent20Vz3_pT100 )

process.ana25Vz3 = cms.Path(
		process.pre_ana25Vz3*
		process.QWAcc_Cent25Vz3_pT004 *
		process.QWAcc_Cent25Vz3_pT005 *
		process.QWAcc_Cent25Vz3_pT006 *
		process.QWAcc_Cent25Vz3_pT008 *
		process.QWAcc_Cent25Vz3_pT010 *
		process.QWAcc_Cent25Vz3_pT012 *
		process.QWAcc_Cent25Vz3_pT015 *
		process.QWAcc_Cent25Vz3_pT020 *
		process.QWAcc_Cent25Vz3_pT025 *
		process.QWAcc_Cent25Vz3_pT030 *
		process.QWAcc_Cent25Vz3_pT035 *
		process.QWAcc_Cent25Vz3_pT040 *
		process.QWAcc_Cent25Vz3_pT050 *
		process.QWAcc_Cent25Vz3_pT060 *
		process.QWAcc_Cent25Vz3_pT070 *
		process.QWAcc_Cent25Vz3_pT080 *
		process.QWAcc_Cent25Vz3_pT100 )

process.ana30Vz3 = cms.Path(
		process.pre_ana30Vz3*
		process.QWAcc_Cent30Vz3_pT004 *
		process.QWAcc_Cent30Vz3_pT005 *
		process.QWAcc_Cent30Vz3_pT006 *
		process.QWAcc_Cent30Vz3_pT008 *
		process.QWAcc_Cent30Vz3_pT010 *
		process.QWAcc_Cent30Vz3_pT012 *
		process.QWAcc_Cent30Vz3_pT015 *
		process.QWAcc_Cent30Vz3_pT020 *
		process.QWAcc_Cent30Vz3_pT025 *
		process.QWAcc_Cent30Vz3_pT030 *
		process.QWAcc_Cent30Vz3_pT035 *
		process.QWAcc_Cent30Vz3_pT040 *
		process.QWAcc_Cent30Vz3_pT050 *
		process.QWAcc_Cent30Vz3_pT060 *
		process.QWAcc_Cent30Vz3_pT070 *
		process.QWAcc_Cent30Vz3_pT080 *
		process.QWAcc_Cent30Vz3_pT100 )

process.ana35Vz3 = cms.Path(
		process.pre_ana35Vz3*
		process.QWAcc_Cent35Vz3_pT004 *
		process.QWAcc_Cent35Vz3_pT005 *
		process.QWAcc_Cent35Vz3_pT006 *
		process.QWAcc_Cent35Vz3_pT008 *
		process.QWAcc_Cent35Vz3_pT010 *
		process.QWAcc_Cent35Vz3_pT012 *
		process.QWAcc_Cent35Vz3_pT015 *
		process.QWAcc_Cent35Vz3_pT020 *
		process.QWAcc_Cent35Vz3_pT025 *
		process.QWAcc_Cent35Vz3_pT030 *
		process.QWAcc_Cent35Vz3_pT035 *
		process.QWAcc_Cent35Vz3_pT040 *
		process.QWAcc_Cent35Vz3_pT050 *
		process.QWAcc_Cent35Vz3_pT060 *
		process.QWAcc_Cent35Vz3_pT070 *
		process.QWAcc_Cent35Vz3_pT080 *
		process.QWAcc_Cent35Vz3_pT100 )

process.ana40Vz3 = cms.Path(
		process.pre_ana40Vz3*
		process.QWAcc_Cent40Vz3_pT004 *
		process.QWAcc_Cent40Vz3_pT005 *
		process.QWAcc_Cent40Vz3_pT006 *
		process.QWAcc_Cent40Vz3_pT008 *
		process.QWAcc_Cent40Vz3_pT010 *
		process.QWAcc_Cent40Vz3_pT012 *
		process.QWAcc_Cent40Vz3_pT015 *
		process.QWAcc_Cent40Vz3_pT020 *
		process.QWAcc_Cent40Vz3_pT025 *
		process.QWAcc_Cent40Vz3_pT030 *
		process.QWAcc_Cent40Vz3_pT035 *
		process.QWAcc_Cent40Vz3_pT040 *
		process.QWAcc_Cent40Vz3_pT050 *
		process.QWAcc_Cent40Vz3_pT060 *
		process.QWAcc_Cent40Vz3_pT070 *
		process.QWAcc_Cent40Vz3_pT080 *
		process.QWAcc_Cent40Vz3_pT100 )

process.ana50Vz3 = cms.Path(
		process.pre_ana50Vz3*
		process.QWAcc_Cent50Vz3_pT004 *
		process.QWAcc_Cent50Vz3_pT005 *
		process.QWAcc_Cent50Vz3_pT006 *
		process.QWAcc_Cent50Vz3_pT008 *
		process.QWAcc_Cent50Vz3_pT010 *
		process.QWAcc_Cent50Vz3_pT012 *
		process.QWAcc_Cent50Vz3_pT015 *
		process.QWAcc_Cent50Vz3_pT020 *
		process.QWAcc_Cent50Vz3_pT025 *
		process.QWAcc_Cent50Vz3_pT030 *
		process.QWAcc_Cent50Vz3_pT035 *
		process.QWAcc_Cent50Vz3_pT040 *
		process.QWAcc_Cent50Vz3_pT050 *
		process.QWAcc_Cent50Vz3_pT060 *
		process.QWAcc_Cent50Vz3_pT070 *
		process.QWAcc_Cent50Vz3_pT080 *
		process.QWAcc_Cent50Vz3_pT100 )


process.ana60Vz3 = cms.Path(
		process.pre_ana60Vz3*
		process.QWAcc_Cent60Vz3_pT004 *
		process.QWAcc_Cent60Vz3_pT005 *
		process.QWAcc_Cent60Vz3_pT006 *
		process.QWAcc_Cent60Vz3_pT008 *
		process.QWAcc_Cent60Vz3_pT010 *
		process.QWAcc_Cent60Vz3_pT012 *
		process.QWAcc_Cent60Vz3_pT015 *
		process.QWAcc_Cent60Vz3_pT020 *
		process.QWAcc_Cent60Vz3_pT025 *
		process.QWAcc_Cent60Vz3_pT030 *
		process.QWAcc_Cent60Vz3_pT035 *
		process.QWAcc_Cent60Vz3_pT040 *
		process.QWAcc_Cent60Vz3_pT050 *
		process.QWAcc_Cent60Vz3_pT060 *
		process.QWAcc_Cent60Vz3_pT070 *
		process.QWAcc_Cent60Vz3_pT080 *
		process.QWAcc_Cent60Vz3_pT100 )


process.ana70Vz3 = cms.Path(
		process.pre_ana70Vz3*
		process.QWAcc_Cent70Vz3_pT004 *
		process.QWAcc_Cent70Vz3_pT005 *
		process.QWAcc_Cent70Vz3_pT006 *
		process.QWAcc_Cent70Vz3_pT008 *
		process.QWAcc_Cent70Vz3_pT010 *
		process.QWAcc_Cent70Vz3_pT012 *
		process.QWAcc_Cent70Vz3_pT015 *
		process.QWAcc_Cent70Vz3_pT020 *
		process.QWAcc_Cent70Vz3_pT025 *
		process.QWAcc_Cent70Vz3_pT030 *
		process.QWAcc_Cent70Vz3_pT035 *
		process.QWAcc_Cent70Vz3_pT040 *
		process.QWAcc_Cent70Vz3_pT050 *
		process.QWAcc_Cent70Vz3_pT060 *
		process.QWAcc_Cent70Vz3_pT070 *
		process.QWAcc_Cent70Vz3_pT080 *
		process.QWAcc_Cent70Vz3_pT100 )


process.ana80Vz3 = cms.Path(
		process.pre_ana80Vz3*
		process.QWAcc_Cent80Vz3_pT004 *
		process.QWAcc_Cent80Vz3_pT005 *
		process.QWAcc_Cent80Vz3_pT006 *
		process.QWAcc_Cent80Vz3_pT008 *
		process.QWAcc_Cent80Vz3_pT010 *
		process.QWAcc_Cent80Vz3_pT012 *
		process.QWAcc_Cent80Vz3_pT015 *
		process.QWAcc_Cent80Vz3_pT020 *
		process.QWAcc_Cent80Vz3_pT025 *
		process.QWAcc_Cent80Vz3_pT030 *
		process.QWAcc_Cent80Vz3_pT035 *
		process.QWAcc_Cent80Vz3_pT040 *
		process.QWAcc_Cent80Vz3_pT050 *
		process.QWAcc_Cent80Vz3_pT060 *
		process.QWAcc_Cent80Vz3_pT070 *
		process.QWAcc_Cent80Vz3_pT080 *
		process.QWAcc_Cent80Vz3_pT100 )


process.ana90Vz3 = cms.Path(
		process.pre_ana90Vz3*
		process.QWAcc_Cent90Vz3_pT004 *
		process.QWAcc_Cent90Vz3_pT005 *
		process.QWAcc_Cent90Vz3_pT006 *
		process.QWAcc_Cent90Vz3_pT008 *
		process.QWAcc_Cent90Vz3_pT010 *
		process.QWAcc_Cent90Vz3_pT012 *
		process.QWAcc_Cent90Vz3_pT015 *
		process.QWAcc_Cent90Vz3_pT020 *
		process.QWAcc_Cent90Vz3_pT025 *
		process.QWAcc_Cent90Vz3_pT030 *
		process.QWAcc_Cent90Vz3_pT035 *
		process.QWAcc_Cent90Vz3_pT040 *
		process.QWAcc_Cent90Vz3_pT050 *
		process.QWAcc_Cent90Vz3_pT060 *
		process.QWAcc_Cent90Vz3_pT070 *
		process.QWAcc_Cent90Vz3_pT080 *
		process.QWAcc_Cent90Vz3_pT100 )


process.ana00Vz3 = cms.Path(
		process.pre_ana00Vz3*
		process.QWAcc_Cent00Vz3_pT004 *
		process.QWAcc_Cent00Vz3_pT005 *
		process.QWAcc_Cent00Vz3_pT006 *
		process.QWAcc_Cent00Vz3_pT008 *
		process.QWAcc_Cent00Vz3_pT010 *
		process.QWAcc_Cent00Vz3_pT012 *
		process.QWAcc_Cent00Vz3_pT015 *
		process.QWAcc_Cent00Vz3_pT020 *
		process.QWAcc_Cent00Vz3_pT025 *
		process.QWAcc_Cent00Vz3_pT030 *
		process.QWAcc_Cent00Vz3_pT035 *
		process.QWAcc_Cent00Vz3_pT040 *
		process.QWAcc_Cent00Vz3_pT050 *
		process.QWAcc_Cent00Vz3_pT060 *
		process.QWAcc_Cent00Vz3_pT070 *
		process.QWAcc_Cent00Vz3_pT080 *
		process.QWAcc_Cent00Vz3_pT100 )


## Vz4
process.ana05Vz4 = cms.Path(
		process.pre_ana05Vz4*
		process.QWAcc_Cent05Vz4_pT004 *
		process.QWAcc_Cent05Vz4_pT005 *
		process.QWAcc_Cent05Vz4_pT006 *
		process.QWAcc_Cent05Vz4_pT008 *
		process.QWAcc_Cent05Vz4_pT010 *
		process.QWAcc_Cent05Vz4_pT012 *
		process.QWAcc_Cent05Vz4_pT015 *
		process.QWAcc_Cent05Vz4_pT020 *
		process.QWAcc_Cent05Vz4_pT025 *
		process.QWAcc_Cent05Vz4_pT030 *
		process.QWAcc_Cent05Vz4_pT035 *
		process.QWAcc_Cent05Vz4_pT040 *
		process.QWAcc_Cent05Vz4_pT050 *
		process.QWAcc_Cent05Vz4_pT060 *
		process.QWAcc_Cent05Vz4_pT070 *
		process.QWAcc_Cent05Vz4_pT080 *
		process.QWAcc_Cent05Vz4_pT100 )

process.ana10Vz4 = cms.Path(
		process.pre_ana10Vz4*
		process.QWAcc_Cent10Vz4_pT004 *
		process.QWAcc_Cent10Vz4_pT005 *
		process.QWAcc_Cent10Vz4_pT006 *
		process.QWAcc_Cent10Vz4_pT008 *
		process.QWAcc_Cent10Vz4_pT010 *
		process.QWAcc_Cent10Vz4_pT012 *
		process.QWAcc_Cent10Vz4_pT015 *
		process.QWAcc_Cent10Vz4_pT020 *
		process.QWAcc_Cent10Vz4_pT025 *
		process.QWAcc_Cent10Vz4_pT030 *
		process.QWAcc_Cent10Vz4_pT035 *
		process.QWAcc_Cent10Vz4_pT040 *
		process.QWAcc_Cent10Vz4_pT050 *
		process.QWAcc_Cent10Vz4_pT060 *
		process.QWAcc_Cent10Vz4_pT070 *
		process.QWAcc_Cent10Vz4_pT080 *
		process.QWAcc_Cent10Vz4_pT100 )

process.ana15Vz4 = cms.Path(
		process.pre_ana15Vz4*
		process.QWAcc_Cent15Vz4_pT004 *
		process.QWAcc_Cent15Vz4_pT005 *
		process.QWAcc_Cent15Vz4_pT006 *
		process.QWAcc_Cent15Vz4_pT008 *
		process.QWAcc_Cent15Vz4_pT010 *
		process.QWAcc_Cent15Vz4_pT012 *
		process.QWAcc_Cent15Vz4_pT015 *
		process.QWAcc_Cent15Vz4_pT020 *
		process.QWAcc_Cent15Vz4_pT025 *
		process.QWAcc_Cent15Vz4_pT030 *
		process.QWAcc_Cent15Vz4_pT035 *
		process.QWAcc_Cent15Vz4_pT040 *
		process.QWAcc_Cent15Vz4_pT050 *
		process.QWAcc_Cent15Vz4_pT060 *
		process.QWAcc_Cent15Vz4_pT070 *
		process.QWAcc_Cent15Vz4_pT080 *
		process.QWAcc_Cent15Vz4_pT100 )


process.ana20Vz4 = cms.Path(
		process.pre_ana20Vz4*
		process.QWAcc_Cent20Vz4_pT004 *
		process.QWAcc_Cent20Vz4_pT005 *
		process.QWAcc_Cent20Vz4_pT006 *
		process.QWAcc_Cent20Vz4_pT008 *
		process.QWAcc_Cent20Vz4_pT010 *
		process.QWAcc_Cent20Vz4_pT012 *
		process.QWAcc_Cent20Vz4_pT015 *
		process.QWAcc_Cent20Vz4_pT020 *
		process.QWAcc_Cent20Vz4_pT025 *
		process.QWAcc_Cent20Vz4_pT030 *
		process.QWAcc_Cent20Vz4_pT035 *
		process.QWAcc_Cent20Vz4_pT040 *
		process.QWAcc_Cent20Vz4_pT050 *
		process.QWAcc_Cent20Vz4_pT060 *
		process.QWAcc_Cent20Vz4_pT070 *
		process.QWAcc_Cent20Vz4_pT080 *
		process.QWAcc_Cent20Vz4_pT100 )

process.ana25Vz4 = cms.Path(
		process.pre_ana25Vz4*
		process.QWAcc_Cent25Vz4_pT004 *
		process.QWAcc_Cent25Vz4_pT005 *
		process.QWAcc_Cent25Vz4_pT006 *
		process.QWAcc_Cent25Vz4_pT008 *
		process.QWAcc_Cent25Vz4_pT010 *
		process.QWAcc_Cent25Vz4_pT012 *
		process.QWAcc_Cent25Vz4_pT015 *
		process.QWAcc_Cent25Vz4_pT020 *
		process.QWAcc_Cent25Vz4_pT025 *
		process.QWAcc_Cent25Vz4_pT030 *
		process.QWAcc_Cent25Vz4_pT035 *
		process.QWAcc_Cent25Vz4_pT040 *
		process.QWAcc_Cent25Vz4_pT050 *
		process.QWAcc_Cent25Vz4_pT060 *
		process.QWAcc_Cent25Vz4_pT070 *
		process.QWAcc_Cent25Vz4_pT080 *
		process.QWAcc_Cent25Vz4_pT100 )

process.ana30Vz4 = cms.Path(
		process.pre_ana30Vz4*
		process.QWAcc_Cent30Vz4_pT004 *
		process.QWAcc_Cent30Vz4_pT005 *
		process.QWAcc_Cent30Vz4_pT006 *
		process.QWAcc_Cent30Vz4_pT008 *
		process.QWAcc_Cent30Vz4_pT010 *
		process.QWAcc_Cent30Vz4_pT012 *
		process.QWAcc_Cent30Vz4_pT015 *
		process.QWAcc_Cent30Vz4_pT020 *
		process.QWAcc_Cent30Vz4_pT025 *
		process.QWAcc_Cent30Vz4_pT030 *
		process.QWAcc_Cent30Vz4_pT035 *
		process.QWAcc_Cent30Vz4_pT040 *
		process.QWAcc_Cent30Vz4_pT050 *
		process.QWAcc_Cent30Vz4_pT060 *
		process.QWAcc_Cent30Vz4_pT070 *
		process.QWAcc_Cent30Vz4_pT080 *
		process.QWAcc_Cent30Vz4_pT100 )

process.ana35Vz4 = cms.Path(
		process.pre_ana35Vz4*
		process.QWAcc_Cent35Vz4_pT004 *
		process.QWAcc_Cent35Vz4_pT005 *
		process.QWAcc_Cent35Vz4_pT006 *
		process.QWAcc_Cent35Vz4_pT008 *
		process.QWAcc_Cent35Vz4_pT010 *
		process.QWAcc_Cent35Vz4_pT012 *
		process.QWAcc_Cent35Vz4_pT015 *
		process.QWAcc_Cent35Vz4_pT020 *
		process.QWAcc_Cent35Vz4_pT025 *
		process.QWAcc_Cent35Vz4_pT030 *
		process.QWAcc_Cent35Vz4_pT035 *
		process.QWAcc_Cent35Vz4_pT040 *
		process.QWAcc_Cent35Vz4_pT050 *
		process.QWAcc_Cent35Vz4_pT060 *
		process.QWAcc_Cent35Vz4_pT070 *
		process.QWAcc_Cent35Vz4_pT080 *
		process.QWAcc_Cent35Vz4_pT100 )

process.ana40Vz4 = cms.Path(
		process.pre_ana40Vz4*
		process.QWAcc_Cent40Vz4_pT004 *
		process.QWAcc_Cent40Vz4_pT005 *
		process.QWAcc_Cent40Vz4_pT006 *
		process.QWAcc_Cent40Vz4_pT008 *
		process.QWAcc_Cent40Vz4_pT010 *
		process.QWAcc_Cent40Vz4_pT012 *
		process.QWAcc_Cent40Vz4_pT015 *
		process.QWAcc_Cent40Vz4_pT020 *
		process.QWAcc_Cent40Vz4_pT025 *
		process.QWAcc_Cent40Vz4_pT030 *
		process.QWAcc_Cent40Vz4_pT035 *
		process.QWAcc_Cent40Vz4_pT040 *
		process.QWAcc_Cent40Vz4_pT050 *
		process.QWAcc_Cent40Vz4_pT060 *
		process.QWAcc_Cent40Vz4_pT070 *
		process.QWAcc_Cent40Vz4_pT080 *
		process.QWAcc_Cent40Vz4_pT100 )

process.ana50Vz4 = cms.Path(
		process.pre_ana50Vz4*
		process.QWAcc_Cent50Vz4_pT004 *
		process.QWAcc_Cent50Vz4_pT005 *
		process.QWAcc_Cent50Vz4_pT006 *
		process.QWAcc_Cent50Vz4_pT008 *
		process.QWAcc_Cent50Vz4_pT010 *
		process.QWAcc_Cent50Vz4_pT012 *
		process.QWAcc_Cent50Vz4_pT015 *
		process.QWAcc_Cent50Vz4_pT020 *
		process.QWAcc_Cent50Vz4_pT025 *
		process.QWAcc_Cent50Vz4_pT030 *
		process.QWAcc_Cent50Vz4_pT035 *
		process.QWAcc_Cent50Vz4_pT040 *
		process.QWAcc_Cent50Vz4_pT050 *
		process.QWAcc_Cent50Vz4_pT060 *
		process.QWAcc_Cent50Vz4_pT070 *
		process.QWAcc_Cent50Vz4_pT080 *
		process.QWAcc_Cent50Vz4_pT100 )


process.ana60Vz4 = cms.Path(
		process.pre_ana60Vz4*
		process.QWAcc_Cent60Vz4_pT004 *
		process.QWAcc_Cent60Vz4_pT005 *
		process.QWAcc_Cent60Vz4_pT006 *
		process.QWAcc_Cent60Vz4_pT008 *
		process.QWAcc_Cent60Vz4_pT010 *
		process.QWAcc_Cent60Vz4_pT012 *
		process.QWAcc_Cent60Vz4_pT015 *
		process.QWAcc_Cent60Vz4_pT020 *
		process.QWAcc_Cent60Vz4_pT025 *
		process.QWAcc_Cent60Vz4_pT030 *
		process.QWAcc_Cent60Vz4_pT035 *
		process.QWAcc_Cent60Vz4_pT040 *
		process.QWAcc_Cent60Vz4_pT050 *
		process.QWAcc_Cent60Vz4_pT060 *
		process.QWAcc_Cent60Vz4_pT070 *
		process.QWAcc_Cent60Vz4_pT080 *
		process.QWAcc_Cent60Vz4_pT100 )


process.ana70Vz4 = cms.Path(
		process.pre_ana70Vz4*
		process.QWAcc_Cent70Vz4_pT004 *
		process.QWAcc_Cent70Vz4_pT005 *
		process.QWAcc_Cent70Vz4_pT006 *
		process.QWAcc_Cent70Vz4_pT008 *
		process.QWAcc_Cent70Vz4_pT010 *
		process.QWAcc_Cent70Vz4_pT012 *
		process.QWAcc_Cent70Vz4_pT015 *
		process.QWAcc_Cent70Vz4_pT020 *
		process.QWAcc_Cent70Vz4_pT025 *
		process.QWAcc_Cent70Vz4_pT030 *
		process.QWAcc_Cent70Vz4_pT035 *
		process.QWAcc_Cent70Vz4_pT040 *
		process.QWAcc_Cent70Vz4_pT050 *
		process.QWAcc_Cent70Vz4_pT060 *
		process.QWAcc_Cent70Vz4_pT070 *
		process.QWAcc_Cent70Vz4_pT080 *
		process.QWAcc_Cent70Vz4_pT100 )


process.ana80Vz4 = cms.Path(
		process.pre_ana80Vz4*
		process.QWAcc_Cent80Vz4_pT004 *
		process.QWAcc_Cent80Vz4_pT005 *
		process.QWAcc_Cent80Vz4_pT006 *
		process.QWAcc_Cent80Vz4_pT008 *
		process.QWAcc_Cent80Vz4_pT010 *
		process.QWAcc_Cent80Vz4_pT012 *
		process.QWAcc_Cent80Vz4_pT015 *
		process.QWAcc_Cent80Vz4_pT020 *
		process.QWAcc_Cent80Vz4_pT025 *
		process.QWAcc_Cent80Vz4_pT030 *
		process.QWAcc_Cent80Vz4_pT035 *
		process.QWAcc_Cent80Vz4_pT040 *
		process.QWAcc_Cent80Vz4_pT050 *
		process.QWAcc_Cent80Vz4_pT060 *
		process.QWAcc_Cent80Vz4_pT070 *
		process.QWAcc_Cent80Vz4_pT080 *
		process.QWAcc_Cent80Vz4_pT100 )


process.ana90Vz4 = cms.Path(
		process.pre_ana90Vz4*
		process.QWAcc_Cent90Vz4_pT004 *
		process.QWAcc_Cent90Vz4_pT005 *
		process.QWAcc_Cent90Vz4_pT006 *
		process.QWAcc_Cent90Vz4_pT008 *
		process.QWAcc_Cent90Vz4_pT010 *
		process.QWAcc_Cent90Vz4_pT012 *
		process.QWAcc_Cent90Vz4_pT015 *
		process.QWAcc_Cent90Vz4_pT020 *
		process.QWAcc_Cent90Vz4_pT025 *
		process.QWAcc_Cent90Vz4_pT030 *
		process.QWAcc_Cent90Vz4_pT035 *
		process.QWAcc_Cent90Vz4_pT040 *
		process.QWAcc_Cent90Vz4_pT050 *
		process.QWAcc_Cent90Vz4_pT060 *
		process.QWAcc_Cent90Vz4_pT070 *
		process.QWAcc_Cent90Vz4_pT080 *
		process.QWAcc_Cent90Vz4_pT100 )


process.ana00Vz4 = cms.Path(
		process.pre_ana00Vz4*
		process.QWAcc_Cent00Vz4_pT004 *
		process.QWAcc_Cent00Vz4_pT005 *
		process.QWAcc_Cent00Vz4_pT006 *
		process.QWAcc_Cent00Vz4_pT008 *
		process.QWAcc_Cent00Vz4_pT010 *
		process.QWAcc_Cent00Vz4_pT012 *
		process.QWAcc_Cent00Vz4_pT015 *
		process.QWAcc_Cent00Vz4_pT020 *
		process.QWAcc_Cent00Vz4_pT025 *
		process.QWAcc_Cent00Vz4_pT030 *
		process.QWAcc_Cent00Vz4_pT035 *
		process.QWAcc_Cent00Vz4_pT040 *
		process.QWAcc_Cent00Vz4_pT050 *
		process.QWAcc_Cent00Vz4_pT060 *
		process.QWAcc_Cent00Vz4_pT070 *
		process.QWAcc_Cent00Vz4_pT080 *
		process.QWAcc_Cent00Vz4_pT100 )


## Vz5
process.ana05Vz5 = cms.Path(
		process.pre_ana05Vz5*
		process.QWAcc_Cent05Vz5_pT004 *
		process.QWAcc_Cent05Vz5_pT005 *
		process.QWAcc_Cent05Vz5_pT006 *
		process.QWAcc_Cent05Vz5_pT008 *
		process.QWAcc_Cent05Vz5_pT010 *
		process.QWAcc_Cent05Vz5_pT012 *
		process.QWAcc_Cent05Vz5_pT015 *
		process.QWAcc_Cent05Vz5_pT020 *
		process.QWAcc_Cent05Vz5_pT025 *
		process.QWAcc_Cent05Vz5_pT030 *
		process.QWAcc_Cent05Vz5_pT035 *
		process.QWAcc_Cent05Vz5_pT040 *
		process.QWAcc_Cent05Vz5_pT050 *
		process.QWAcc_Cent05Vz5_pT060 *
		process.QWAcc_Cent05Vz5_pT070 *
		process.QWAcc_Cent05Vz5_pT080 *
		process.QWAcc_Cent05Vz5_pT100 )

process.ana10Vz5 = cms.Path(
		process.pre_ana10Vz5*
		process.QWAcc_Cent10Vz5_pT004 *
		process.QWAcc_Cent10Vz5_pT005 *
		process.QWAcc_Cent10Vz5_pT006 *
		process.QWAcc_Cent10Vz5_pT008 *
		process.QWAcc_Cent10Vz5_pT010 *
		process.QWAcc_Cent10Vz5_pT012 *
		process.QWAcc_Cent10Vz5_pT015 *
		process.QWAcc_Cent10Vz5_pT020 *
		process.QWAcc_Cent10Vz5_pT025 *
		process.QWAcc_Cent10Vz5_pT030 *
		process.QWAcc_Cent10Vz5_pT035 *
		process.QWAcc_Cent10Vz5_pT040 *
		process.QWAcc_Cent10Vz5_pT050 *
		process.QWAcc_Cent10Vz5_pT060 *
		process.QWAcc_Cent10Vz5_pT070 *
		process.QWAcc_Cent10Vz5_pT080 *
		process.QWAcc_Cent10Vz5_pT100 )

process.ana15Vz5 = cms.Path(
		process.pre_ana15Vz5*
		process.QWAcc_Cent15Vz5_pT004 *
		process.QWAcc_Cent15Vz5_pT005 *
		process.QWAcc_Cent15Vz5_pT006 *
		process.QWAcc_Cent15Vz5_pT008 *
		process.QWAcc_Cent15Vz5_pT010 *
		process.QWAcc_Cent15Vz5_pT012 *
		process.QWAcc_Cent15Vz5_pT015 *
		process.QWAcc_Cent15Vz5_pT020 *
		process.QWAcc_Cent15Vz5_pT025 *
		process.QWAcc_Cent15Vz5_pT030 *
		process.QWAcc_Cent15Vz5_pT035 *
		process.QWAcc_Cent15Vz5_pT040 *
		process.QWAcc_Cent15Vz5_pT050 *
		process.QWAcc_Cent15Vz5_pT060 *
		process.QWAcc_Cent15Vz5_pT070 *
		process.QWAcc_Cent15Vz5_pT080 *
		process.QWAcc_Cent15Vz5_pT100 )


process.ana20Vz5 = cms.Path(
		process.pre_ana20Vz5*
		process.QWAcc_Cent20Vz5_pT004 *
		process.QWAcc_Cent20Vz5_pT005 *
		process.QWAcc_Cent20Vz5_pT006 *
		process.QWAcc_Cent20Vz5_pT008 *
		process.QWAcc_Cent20Vz5_pT010 *
		process.QWAcc_Cent20Vz5_pT012 *
		process.QWAcc_Cent20Vz5_pT015 *
		process.QWAcc_Cent20Vz5_pT020 *
		process.QWAcc_Cent20Vz5_pT025 *
		process.QWAcc_Cent20Vz5_pT030 *
		process.QWAcc_Cent20Vz5_pT035 *
		process.QWAcc_Cent20Vz5_pT040 *
		process.QWAcc_Cent20Vz5_pT050 *
		process.QWAcc_Cent20Vz5_pT060 *
		process.QWAcc_Cent20Vz5_pT070 *
		process.QWAcc_Cent20Vz5_pT080 *
		process.QWAcc_Cent20Vz5_pT100 )

process.ana25Vz5 = cms.Path(
		process.pre_ana25Vz5*
		process.QWAcc_Cent25Vz5_pT004 *
		process.QWAcc_Cent25Vz5_pT005 *
		process.QWAcc_Cent25Vz5_pT006 *
		process.QWAcc_Cent25Vz5_pT008 *
		process.QWAcc_Cent25Vz5_pT010 *
		process.QWAcc_Cent25Vz5_pT012 *
		process.QWAcc_Cent25Vz5_pT015 *
		process.QWAcc_Cent25Vz5_pT020 *
		process.QWAcc_Cent25Vz5_pT025 *
		process.QWAcc_Cent25Vz5_pT030 *
		process.QWAcc_Cent25Vz5_pT035 *
		process.QWAcc_Cent25Vz5_pT040 *
		process.QWAcc_Cent25Vz5_pT050 *
		process.QWAcc_Cent25Vz5_pT060 *
		process.QWAcc_Cent25Vz5_pT070 *
		process.QWAcc_Cent25Vz5_pT080 *
		process.QWAcc_Cent25Vz5_pT100 )

process.ana30Vz5 = cms.Path(
		process.pre_ana30Vz5*
		process.QWAcc_Cent30Vz5_pT004 *
		process.QWAcc_Cent30Vz5_pT005 *
		process.QWAcc_Cent30Vz5_pT006 *
		process.QWAcc_Cent30Vz5_pT008 *
		process.QWAcc_Cent30Vz5_pT010 *
		process.QWAcc_Cent30Vz5_pT012 *
		process.QWAcc_Cent30Vz5_pT015 *
		process.QWAcc_Cent30Vz5_pT020 *
		process.QWAcc_Cent30Vz5_pT025 *
		process.QWAcc_Cent30Vz5_pT030 *
		process.QWAcc_Cent30Vz5_pT035 *
		process.QWAcc_Cent30Vz5_pT040 *
		process.QWAcc_Cent30Vz5_pT050 *
		process.QWAcc_Cent30Vz5_pT060 *
		process.QWAcc_Cent30Vz5_pT070 *
		process.QWAcc_Cent30Vz5_pT080 *
		process.QWAcc_Cent30Vz5_pT100 )

process.ana35Vz5 = cms.Path(
		process.pre_ana35Vz5*
		process.QWAcc_Cent35Vz5_pT004 *
		process.QWAcc_Cent35Vz5_pT005 *
		process.QWAcc_Cent35Vz5_pT006 *
		process.QWAcc_Cent35Vz5_pT008 *
		process.QWAcc_Cent35Vz5_pT010 *
		process.QWAcc_Cent35Vz5_pT012 *
		process.QWAcc_Cent35Vz5_pT015 *
		process.QWAcc_Cent35Vz5_pT020 *
		process.QWAcc_Cent35Vz5_pT025 *
		process.QWAcc_Cent35Vz5_pT030 *
		process.QWAcc_Cent35Vz5_pT035 *
		process.QWAcc_Cent35Vz5_pT040 *
		process.QWAcc_Cent35Vz5_pT050 *
		process.QWAcc_Cent35Vz5_pT060 *
		process.QWAcc_Cent35Vz5_pT070 *
		process.QWAcc_Cent35Vz5_pT080 *
		process.QWAcc_Cent35Vz5_pT100 )

process.ana40Vz5 = cms.Path(
		process.pre_ana40Vz5*
		process.QWAcc_Cent40Vz5_pT004 *
		process.QWAcc_Cent40Vz5_pT005 *
		process.QWAcc_Cent40Vz5_pT006 *
		process.QWAcc_Cent40Vz5_pT008 *
		process.QWAcc_Cent40Vz5_pT010 *
		process.QWAcc_Cent40Vz5_pT012 *
		process.QWAcc_Cent40Vz5_pT015 *
		process.QWAcc_Cent40Vz5_pT020 *
		process.QWAcc_Cent40Vz5_pT025 *
		process.QWAcc_Cent40Vz5_pT030 *
		process.QWAcc_Cent40Vz5_pT035 *
		process.QWAcc_Cent40Vz5_pT040 *
		process.QWAcc_Cent40Vz5_pT050 *
		process.QWAcc_Cent40Vz5_pT060 *
		process.QWAcc_Cent40Vz5_pT070 *
		process.QWAcc_Cent40Vz5_pT080 *
		process.QWAcc_Cent40Vz5_pT100 )

process.ana50Vz5 = cms.Path(
		process.pre_ana50Vz5*
		process.QWAcc_Cent50Vz5_pT004 *
		process.QWAcc_Cent50Vz5_pT005 *
		process.QWAcc_Cent50Vz5_pT006 *
		process.QWAcc_Cent50Vz5_pT008 *
		process.QWAcc_Cent50Vz5_pT010 *
		process.QWAcc_Cent50Vz5_pT012 *
		process.QWAcc_Cent50Vz5_pT015 *
		process.QWAcc_Cent50Vz5_pT020 *
		process.QWAcc_Cent50Vz5_pT025 *
		process.QWAcc_Cent50Vz5_pT030 *
		process.QWAcc_Cent50Vz5_pT035 *
		process.QWAcc_Cent50Vz5_pT040 *
		process.QWAcc_Cent50Vz5_pT050 *
		process.QWAcc_Cent50Vz5_pT060 *
		process.QWAcc_Cent50Vz5_pT070 *
		process.QWAcc_Cent50Vz5_pT080 *
		process.QWAcc_Cent50Vz5_pT100 )


process.ana60Vz5 = cms.Path(
		process.pre_ana60Vz5*
		process.QWAcc_Cent60Vz5_pT004 *
		process.QWAcc_Cent60Vz5_pT005 *
		process.QWAcc_Cent60Vz5_pT006 *
		process.QWAcc_Cent60Vz5_pT008 *
		process.QWAcc_Cent60Vz5_pT010 *
		process.QWAcc_Cent60Vz5_pT012 *
		process.QWAcc_Cent60Vz5_pT015 *
		process.QWAcc_Cent60Vz5_pT020 *
		process.QWAcc_Cent60Vz5_pT025 *
		process.QWAcc_Cent60Vz5_pT030 *
		process.QWAcc_Cent60Vz5_pT035 *
		process.QWAcc_Cent60Vz5_pT040 *
		process.QWAcc_Cent60Vz5_pT050 *
		process.QWAcc_Cent60Vz5_pT060 *
		process.QWAcc_Cent60Vz5_pT070 *
		process.QWAcc_Cent60Vz5_pT080 *
		process.QWAcc_Cent60Vz5_pT100 )


process.ana70Vz5 = cms.Path(
		process.pre_ana70Vz5*
		process.QWAcc_Cent70Vz5_pT004 *
		process.QWAcc_Cent70Vz5_pT005 *
		process.QWAcc_Cent70Vz5_pT006 *
		process.QWAcc_Cent70Vz5_pT008 *
		process.QWAcc_Cent70Vz5_pT010 *
		process.QWAcc_Cent70Vz5_pT012 *
		process.QWAcc_Cent70Vz5_pT015 *
		process.QWAcc_Cent70Vz5_pT020 *
		process.QWAcc_Cent70Vz5_pT025 *
		process.QWAcc_Cent70Vz5_pT030 *
		process.QWAcc_Cent70Vz5_pT035 *
		process.QWAcc_Cent70Vz5_pT040 *
		process.QWAcc_Cent70Vz5_pT050 *
		process.QWAcc_Cent70Vz5_pT060 *
		process.QWAcc_Cent70Vz5_pT070 *
		process.QWAcc_Cent70Vz5_pT080 *
		process.QWAcc_Cent70Vz5_pT100 )


process.ana80Vz5 = cms.Path(
		process.pre_ana80Vz5*
		process.QWAcc_Cent80Vz5_pT004 *
		process.QWAcc_Cent80Vz5_pT005 *
		process.QWAcc_Cent80Vz5_pT006 *
		process.QWAcc_Cent80Vz5_pT008 *
		process.QWAcc_Cent80Vz5_pT010 *
		process.QWAcc_Cent80Vz5_pT012 *
		process.QWAcc_Cent80Vz5_pT015 *
		process.QWAcc_Cent80Vz5_pT020 *
		process.QWAcc_Cent80Vz5_pT025 *
		process.QWAcc_Cent80Vz5_pT030 *
		process.QWAcc_Cent80Vz5_pT035 *
		process.QWAcc_Cent80Vz5_pT040 *
		process.QWAcc_Cent80Vz5_pT050 *
		process.QWAcc_Cent80Vz5_pT060 *
		process.QWAcc_Cent80Vz5_pT070 *
		process.QWAcc_Cent80Vz5_pT080 *
		process.QWAcc_Cent80Vz5_pT100 )


process.ana90Vz5 = cms.Path(
		process.pre_ana90Vz5*
		process.QWAcc_Cent90Vz5_pT004 *
		process.QWAcc_Cent90Vz5_pT005 *
		process.QWAcc_Cent90Vz5_pT006 *
		process.QWAcc_Cent90Vz5_pT008 *
		process.QWAcc_Cent90Vz5_pT010 *
		process.QWAcc_Cent90Vz5_pT012 *
		process.QWAcc_Cent90Vz5_pT015 *
		process.QWAcc_Cent90Vz5_pT020 *
		process.QWAcc_Cent90Vz5_pT025 *
		process.QWAcc_Cent90Vz5_pT030 *
		process.QWAcc_Cent90Vz5_pT035 *
		process.QWAcc_Cent90Vz5_pT040 *
		process.QWAcc_Cent90Vz5_pT050 *
		process.QWAcc_Cent90Vz5_pT060 *
		process.QWAcc_Cent90Vz5_pT070 *
		process.QWAcc_Cent90Vz5_pT080 *
		process.QWAcc_Cent90Vz5_pT100 )


process.ana00Vz5 = cms.Path(
		process.pre_ana00Vz5*
		process.QWAcc_Cent00Vz5_pT004 *
		process.QWAcc_Cent00Vz5_pT005 *
		process.QWAcc_Cent00Vz5_pT006 *
		process.QWAcc_Cent00Vz5_pT008 *
		process.QWAcc_Cent00Vz5_pT010 *
		process.QWAcc_Cent00Vz5_pT012 *
		process.QWAcc_Cent00Vz5_pT015 *
		process.QWAcc_Cent00Vz5_pT020 *
		process.QWAcc_Cent00Vz5_pT025 *
		process.QWAcc_Cent00Vz5_pT030 *
		process.QWAcc_Cent00Vz5_pT035 *
		process.QWAcc_Cent00Vz5_pT040 *
		process.QWAcc_Cent00Vz5_pT050 *
		process.QWAcc_Cent00Vz5_pT060 *
		process.QWAcc_Cent00Vz5_pT070 *
		process.QWAcc_Cent00Vz5_pT080 *
		process.QWAcc_Cent00Vz5_pT100 )


## Vz6
process.ana05Vz6 = cms.Path(
		process.pre_ana05Vz6*
		process.QWAcc_Cent05Vz6_pT004 *
		process.QWAcc_Cent05Vz6_pT005 *
		process.QWAcc_Cent05Vz6_pT006 *
		process.QWAcc_Cent05Vz6_pT008 *
		process.QWAcc_Cent05Vz6_pT010 *
		process.QWAcc_Cent05Vz6_pT012 *
		process.QWAcc_Cent05Vz6_pT015 *
		process.QWAcc_Cent05Vz6_pT020 *
		process.QWAcc_Cent05Vz6_pT025 *
		process.QWAcc_Cent05Vz6_pT030 *
		process.QWAcc_Cent05Vz6_pT035 *
		process.QWAcc_Cent05Vz6_pT040 *
		process.QWAcc_Cent05Vz6_pT050 *
		process.QWAcc_Cent05Vz6_pT060 *
		process.QWAcc_Cent05Vz6_pT070 *
		process.QWAcc_Cent05Vz6_pT080 *
		process.QWAcc_Cent05Vz6_pT100 )

process.ana10Vz6 = cms.Path(
		process.pre_ana10Vz6*
		process.QWAcc_Cent10Vz6_pT004 *
		process.QWAcc_Cent10Vz6_pT005 *
		process.QWAcc_Cent10Vz6_pT006 *
		process.QWAcc_Cent10Vz6_pT008 *
		process.QWAcc_Cent10Vz6_pT010 *
		process.QWAcc_Cent10Vz6_pT012 *
		process.QWAcc_Cent10Vz6_pT015 *
		process.QWAcc_Cent10Vz6_pT020 *
		process.QWAcc_Cent10Vz6_pT025 *
		process.QWAcc_Cent10Vz6_pT030 *
		process.QWAcc_Cent10Vz6_pT035 *
		process.QWAcc_Cent10Vz6_pT040 *
		process.QWAcc_Cent10Vz6_pT050 *
		process.QWAcc_Cent10Vz6_pT060 *
		process.QWAcc_Cent10Vz6_pT070 *
		process.QWAcc_Cent10Vz6_pT080 *
		process.QWAcc_Cent10Vz6_pT100 )

process.ana15Vz6 = cms.Path(
		process.pre_ana15Vz6*
		process.QWAcc_Cent15Vz6_pT004 *
		process.QWAcc_Cent15Vz6_pT005 *
		process.QWAcc_Cent15Vz6_pT006 *
		process.QWAcc_Cent15Vz6_pT008 *
		process.QWAcc_Cent15Vz6_pT010 *
		process.QWAcc_Cent15Vz6_pT012 *
		process.QWAcc_Cent15Vz6_pT015 *
		process.QWAcc_Cent15Vz6_pT020 *
		process.QWAcc_Cent15Vz6_pT025 *
		process.QWAcc_Cent15Vz6_pT030 *
		process.QWAcc_Cent15Vz6_pT035 *
		process.QWAcc_Cent15Vz6_pT040 *
		process.QWAcc_Cent15Vz6_pT050 *
		process.QWAcc_Cent15Vz6_pT060 *
		process.QWAcc_Cent15Vz6_pT070 *
		process.QWAcc_Cent15Vz6_pT080 *
		process.QWAcc_Cent15Vz6_pT100 )


process.ana20Vz6 = cms.Path(
		process.pre_ana20Vz6*
		process.QWAcc_Cent20Vz6_pT004 *
		process.QWAcc_Cent20Vz6_pT005 *
		process.QWAcc_Cent20Vz6_pT006 *
		process.QWAcc_Cent20Vz6_pT008 *
		process.QWAcc_Cent20Vz6_pT010 *
		process.QWAcc_Cent20Vz6_pT012 *
		process.QWAcc_Cent20Vz6_pT015 *
		process.QWAcc_Cent20Vz6_pT020 *
		process.QWAcc_Cent20Vz6_pT025 *
		process.QWAcc_Cent20Vz6_pT030 *
		process.QWAcc_Cent20Vz6_pT035 *
		process.QWAcc_Cent20Vz6_pT040 *
		process.QWAcc_Cent20Vz6_pT050 *
		process.QWAcc_Cent20Vz6_pT060 *
		process.QWAcc_Cent20Vz6_pT070 *
		process.QWAcc_Cent20Vz6_pT080 *
		process.QWAcc_Cent20Vz6_pT100 )

process.ana25Vz6 = cms.Path(
		process.pre_ana25Vz6*
		process.QWAcc_Cent25Vz6_pT004 *
		process.QWAcc_Cent25Vz6_pT005 *
		process.QWAcc_Cent25Vz6_pT006 *
		process.QWAcc_Cent25Vz6_pT008 *
		process.QWAcc_Cent25Vz6_pT010 *
		process.QWAcc_Cent25Vz6_pT012 *
		process.QWAcc_Cent25Vz6_pT015 *
		process.QWAcc_Cent25Vz6_pT020 *
		process.QWAcc_Cent25Vz6_pT025 *
		process.QWAcc_Cent25Vz6_pT030 *
		process.QWAcc_Cent25Vz6_pT035 *
		process.QWAcc_Cent25Vz6_pT040 *
		process.QWAcc_Cent25Vz6_pT050 *
		process.QWAcc_Cent25Vz6_pT060 *
		process.QWAcc_Cent25Vz6_pT070 *
		process.QWAcc_Cent25Vz6_pT080 *
		process.QWAcc_Cent25Vz6_pT100 )

process.ana30Vz6 = cms.Path(
		process.pre_ana30Vz6*
		process.QWAcc_Cent30Vz6_pT004 *
		process.QWAcc_Cent30Vz6_pT005 *
		process.QWAcc_Cent30Vz6_pT006 *
		process.QWAcc_Cent30Vz6_pT008 *
		process.QWAcc_Cent30Vz6_pT010 *
		process.QWAcc_Cent30Vz6_pT012 *
		process.QWAcc_Cent30Vz6_pT015 *
		process.QWAcc_Cent30Vz6_pT020 *
		process.QWAcc_Cent30Vz6_pT025 *
		process.QWAcc_Cent30Vz6_pT030 *
		process.QWAcc_Cent30Vz6_pT035 *
		process.QWAcc_Cent30Vz6_pT040 *
		process.QWAcc_Cent30Vz6_pT050 *
		process.QWAcc_Cent30Vz6_pT060 *
		process.QWAcc_Cent30Vz6_pT070 *
		process.QWAcc_Cent30Vz6_pT080 *
		process.QWAcc_Cent30Vz6_pT100 )

process.ana35Vz6 = cms.Path(
		process.pre_ana35Vz6*
		process.QWAcc_Cent35Vz6_pT004 *
		process.QWAcc_Cent35Vz6_pT005 *
		process.QWAcc_Cent35Vz6_pT006 *
		process.QWAcc_Cent35Vz6_pT008 *
		process.QWAcc_Cent35Vz6_pT010 *
		process.QWAcc_Cent35Vz6_pT012 *
		process.QWAcc_Cent35Vz6_pT015 *
		process.QWAcc_Cent35Vz6_pT020 *
		process.QWAcc_Cent35Vz6_pT025 *
		process.QWAcc_Cent35Vz6_pT030 *
		process.QWAcc_Cent35Vz6_pT035 *
		process.QWAcc_Cent35Vz6_pT040 *
		process.QWAcc_Cent35Vz6_pT050 *
		process.QWAcc_Cent35Vz6_pT060 *
		process.QWAcc_Cent35Vz6_pT070 *
		process.QWAcc_Cent35Vz6_pT080 *
		process.QWAcc_Cent35Vz6_pT100 )

process.ana40Vz6 = cms.Path(
		process.pre_ana40Vz6*
		process.QWAcc_Cent40Vz6_pT004 *
		process.QWAcc_Cent40Vz6_pT005 *
		process.QWAcc_Cent40Vz6_pT006 *
		process.QWAcc_Cent40Vz6_pT008 *
		process.QWAcc_Cent40Vz6_pT010 *
		process.QWAcc_Cent40Vz6_pT012 *
		process.QWAcc_Cent40Vz6_pT015 *
		process.QWAcc_Cent40Vz6_pT020 *
		process.QWAcc_Cent40Vz6_pT025 *
		process.QWAcc_Cent40Vz6_pT030 *
		process.QWAcc_Cent40Vz6_pT035 *
		process.QWAcc_Cent40Vz6_pT040 *
		process.QWAcc_Cent40Vz6_pT050 *
		process.QWAcc_Cent40Vz6_pT060 *
		process.QWAcc_Cent40Vz6_pT070 *
		process.QWAcc_Cent40Vz6_pT080 *
		process.QWAcc_Cent40Vz6_pT100 )

process.ana50Vz6 = cms.Path(
		process.pre_ana50Vz6*
		process.QWAcc_Cent50Vz6_pT004 *
		process.QWAcc_Cent50Vz6_pT005 *
		process.QWAcc_Cent50Vz6_pT006 *
		process.QWAcc_Cent50Vz6_pT008 *
		process.QWAcc_Cent50Vz6_pT010 *
		process.QWAcc_Cent50Vz6_pT012 *
		process.QWAcc_Cent50Vz6_pT015 *
		process.QWAcc_Cent50Vz6_pT020 *
		process.QWAcc_Cent50Vz6_pT025 *
		process.QWAcc_Cent50Vz6_pT030 *
		process.QWAcc_Cent50Vz6_pT035 *
		process.QWAcc_Cent50Vz6_pT040 *
		process.QWAcc_Cent50Vz6_pT050 *
		process.QWAcc_Cent50Vz6_pT060 *
		process.QWAcc_Cent50Vz6_pT070 *
		process.QWAcc_Cent50Vz6_pT080 *
		process.QWAcc_Cent50Vz6_pT100 )


process.ana60Vz6 = cms.Path(
		process.pre_ana60Vz6*
		process.QWAcc_Cent60Vz6_pT004 *
		process.QWAcc_Cent60Vz6_pT005 *
		process.QWAcc_Cent60Vz6_pT006 *
		process.QWAcc_Cent60Vz6_pT008 *
		process.QWAcc_Cent60Vz6_pT010 *
		process.QWAcc_Cent60Vz6_pT012 *
		process.QWAcc_Cent60Vz6_pT015 *
		process.QWAcc_Cent60Vz6_pT020 *
		process.QWAcc_Cent60Vz6_pT025 *
		process.QWAcc_Cent60Vz6_pT030 *
		process.QWAcc_Cent60Vz6_pT035 *
		process.QWAcc_Cent60Vz6_pT040 *
		process.QWAcc_Cent60Vz6_pT050 *
		process.QWAcc_Cent60Vz6_pT060 *
		process.QWAcc_Cent60Vz6_pT070 *
		process.QWAcc_Cent60Vz6_pT080 *
		process.QWAcc_Cent60Vz6_pT100 )


process.ana70Vz6 = cms.Path(
		process.pre_ana70Vz6*
		process.QWAcc_Cent70Vz6_pT004 *
		process.QWAcc_Cent70Vz6_pT005 *
		process.QWAcc_Cent70Vz6_pT006 *
		process.QWAcc_Cent70Vz6_pT008 *
		process.QWAcc_Cent70Vz6_pT010 *
		process.QWAcc_Cent70Vz6_pT012 *
		process.QWAcc_Cent70Vz6_pT015 *
		process.QWAcc_Cent70Vz6_pT020 *
		process.QWAcc_Cent70Vz6_pT025 *
		process.QWAcc_Cent70Vz6_pT030 *
		process.QWAcc_Cent70Vz6_pT035 *
		process.QWAcc_Cent70Vz6_pT040 *
		process.QWAcc_Cent70Vz6_pT050 *
		process.QWAcc_Cent70Vz6_pT060 *
		process.QWAcc_Cent70Vz6_pT070 *
		process.QWAcc_Cent70Vz6_pT080 *
		process.QWAcc_Cent70Vz6_pT100 )


process.ana80Vz6 = cms.Path(
		process.pre_ana80Vz6*
		process.QWAcc_Cent80Vz6_pT004 *
		process.QWAcc_Cent80Vz6_pT005 *
		process.QWAcc_Cent80Vz6_pT006 *
		process.QWAcc_Cent80Vz6_pT008 *
		process.QWAcc_Cent80Vz6_pT010 *
		process.QWAcc_Cent80Vz6_pT012 *
		process.QWAcc_Cent80Vz6_pT015 *
		process.QWAcc_Cent80Vz6_pT020 *
		process.QWAcc_Cent80Vz6_pT025 *
		process.QWAcc_Cent80Vz6_pT030 *
		process.QWAcc_Cent80Vz6_pT035 *
		process.QWAcc_Cent80Vz6_pT040 *
		process.QWAcc_Cent80Vz6_pT050 *
		process.QWAcc_Cent80Vz6_pT060 *
		process.QWAcc_Cent80Vz6_pT070 *
		process.QWAcc_Cent80Vz6_pT080 *
		process.QWAcc_Cent80Vz6_pT100 )


process.ana90Vz6 = cms.Path(
		process.pre_ana90Vz6*
		process.QWAcc_Cent90Vz6_pT004 *
		process.QWAcc_Cent90Vz6_pT005 *
		process.QWAcc_Cent90Vz6_pT006 *
		process.QWAcc_Cent90Vz6_pT008 *
		process.QWAcc_Cent90Vz6_pT010 *
		process.QWAcc_Cent90Vz6_pT012 *
		process.QWAcc_Cent90Vz6_pT015 *
		process.QWAcc_Cent90Vz6_pT020 *
		process.QWAcc_Cent90Vz6_pT025 *
		process.QWAcc_Cent90Vz6_pT030 *
		process.QWAcc_Cent90Vz6_pT035 *
		process.QWAcc_Cent90Vz6_pT040 *
		process.QWAcc_Cent90Vz6_pT050 *
		process.QWAcc_Cent90Vz6_pT060 *
		process.QWAcc_Cent90Vz6_pT070 *
		process.QWAcc_Cent90Vz6_pT080 *
		process.QWAcc_Cent90Vz6_pT100 )


process.ana00Vz6 = cms.Path(
		process.pre_ana00Vz6*
		process.QWAcc_Cent00Vz6_pT004 *
		process.QWAcc_Cent00Vz6_pT005 *
		process.QWAcc_Cent00Vz6_pT006 *
		process.QWAcc_Cent00Vz6_pT008 *
		process.QWAcc_Cent00Vz6_pT010 *
		process.QWAcc_Cent00Vz6_pT012 *
		process.QWAcc_Cent00Vz6_pT015 *
		process.QWAcc_Cent00Vz6_pT020 *
		process.QWAcc_Cent00Vz6_pT025 *
		process.QWAcc_Cent00Vz6_pT030 *
		process.QWAcc_Cent00Vz6_pT035 *
		process.QWAcc_Cent00Vz6_pT040 *
		process.QWAcc_Cent00Vz6_pT050 *
		process.QWAcc_Cent00Vz6_pT060 *
		process.QWAcc_Cent00Vz6_pT070 *
		process.QWAcc_Cent00Vz6_pT080 *
		process.QWAcc_Cent00Vz6_pT100 )


## Vz7
process.ana05Vz7 = cms.Path(
		process.pre_ana05Vz7*
		process.QWAcc_Cent05Vz7_pT004 *
		process.QWAcc_Cent05Vz7_pT005 *
		process.QWAcc_Cent05Vz7_pT006 *
		process.QWAcc_Cent05Vz7_pT008 *
		process.QWAcc_Cent05Vz7_pT010 *
		process.QWAcc_Cent05Vz7_pT012 *
		process.QWAcc_Cent05Vz7_pT015 *
		process.QWAcc_Cent05Vz7_pT020 *
		process.QWAcc_Cent05Vz7_pT025 *
		process.QWAcc_Cent05Vz7_pT030 *
		process.QWAcc_Cent05Vz7_pT035 *
		process.QWAcc_Cent05Vz7_pT040 *
		process.QWAcc_Cent05Vz7_pT050 *
		process.QWAcc_Cent05Vz7_pT060 *
		process.QWAcc_Cent05Vz7_pT070 *
		process.QWAcc_Cent05Vz7_pT080 *
		process.QWAcc_Cent05Vz7_pT100 )

process.ana10Vz7 = cms.Path(
		process.pre_ana10Vz7*
		process.QWAcc_Cent10Vz7_pT004 *
		process.QWAcc_Cent10Vz7_pT005 *
		process.QWAcc_Cent10Vz7_pT006 *
		process.QWAcc_Cent10Vz7_pT008 *
		process.QWAcc_Cent10Vz7_pT010 *
		process.QWAcc_Cent10Vz7_pT012 *
		process.QWAcc_Cent10Vz7_pT015 *
		process.QWAcc_Cent10Vz7_pT020 *
		process.QWAcc_Cent10Vz7_pT025 *
		process.QWAcc_Cent10Vz7_pT030 *
		process.QWAcc_Cent10Vz7_pT035 *
		process.QWAcc_Cent10Vz7_pT040 *
		process.QWAcc_Cent10Vz7_pT050 *
		process.QWAcc_Cent10Vz7_pT060 *
		process.QWAcc_Cent10Vz7_pT070 *
		process.QWAcc_Cent10Vz7_pT080 *
		process.QWAcc_Cent10Vz7_pT100 )

process.ana15Vz7 = cms.Path(
		process.pre_ana15Vz7*
		process.QWAcc_Cent15Vz7_pT004 *
		process.QWAcc_Cent15Vz7_pT005 *
		process.QWAcc_Cent15Vz7_pT006 *
		process.QWAcc_Cent15Vz7_pT008 *
		process.QWAcc_Cent15Vz7_pT010 *
		process.QWAcc_Cent15Vz7_pT012 *
		process.QWAcc_Cent15Vz7_pT015 *
		process.QWAcc_Cent15Vz7_pT020 *
		process.QWAcc_Cent15Vz7_pT025 *
		process.QWAcc_Cent15Vz7_pT030 *
		process.QWAcc_Cent15Vz7_pT035 *
		process.QWAcc_Cent15Vz7_pT040 *
		process.QWAcc_Cent15Vz7_pT050 *
		process.QWAcc_Cent15Vz7_pT060 *
		process.QWAcc_Cent15Vz7_pT070 *
		process.QWAcc_Cent15Vz7_pT080 *
		process.QWAcc_Cent15Vz7_pT100 )


process.ana20Vz7 = cms.Path(
		process.pre_ana20Vz7*
		process.QWAcc_Cent20Vz7_pT004 *
		process.QWAcc_Cent20Vz7_pT005 *
		process.QWAcc_Cent20Vz7_pT006 *
		process.QWAcc_Cent20Vz7_pT008 *
		process.QWAcc_Cent20Vz7_pT010 *
		process.QWAcc_Cent20Vz7_pT012 *
		process.QWAcc_Cent20Vz7_pT015 *
		process.QWAcc_Cent20Vz7_pT020 *
		process.QWAcc_Cent20Vz7_pT025 *
		process.QWAcc_Cent20Vz7_pT030 *
		process.QWAcc_Cent20Vz7_pT035 *
		process.QWAcc_Cent20Vz7_pT040 *
		process.QWAcc_Cent20Vz7_pT050 *
		process.QWAcc_Cent20Vz7_pT060 *
		process.QWAcc_Cent20Vz7_pT070 *
		process.QWAcc_Cent20Vz7_pT080 *
		process.QWAcc_Cent20Vz7_pT100 )

process.ana25Vz7 = cms.Path(
		process.pre_ana25Vz7*
		process.QWAcc_Cent25Vz7_pT004 *
		process.QWAcc_Cent25Vz7_pT005 *
		process.QWAcc_Cent25Vz7_pT006 *
		process.QWAcc_Cent25Vz7_pT008 *
		process.QWAcc_Cent25Vz7_pT010 *
		process.QWAcc_Cent25Vz7_pT012 *
		process.QWAcc_Cent25Vz7_pT015 *
		process.QWAcc_Cent25Vz7_pT020 *
		process.QWAcc_Cent25Vz7_pT025 *
		process.QWAcc_Cent25Vz7_pT030 *
		process.QWAcc_Cent25Vz7_pT035 *
		process.QWAcc_Cent25Vz7_pT040 *
		process.QWAcc_Cent25Vz7_pT050 *
		process.QWAcc_Cent25Vz7_pT060 *
		process.QWAcc_Cent25Vz7_pT070 *
		process.QWAcc_Cent25Vz7_pT080 *
		process.QWAcc_Cent25Vz7_pT100 )

process.ana30Vz7 = cms.Path(
		process.pre_ana30Vz7*
		process.QWAcc_Cent30Vz7_pT004 *
		process.QWAcc_Cent30Vz7_pT005 *
		process.QWAcc_Cent30Vz7_pT006 *
		process.QWAcc_Cent30Vz7_pT008 *
		process.QWAcc_Cent30Vz7_pT010 *
		process.QWAcc_Cent30Vz7_pT012 *
		process.QWAcc_Cent30Vz7_pT015 *
		process.QWAcc_Cent30Vz7_pT020 *
		process.QWAcc_Cent30Vz7_pT025 *
		process.QWAcc_Cent30Vz7_pT030 *
		process.QWAcc_Cent30Vz7_pT035 *
		process.QWAcc_Cent30Vz7_pT040 *
		process.QWAcc_Cent30Vz7_pT050 *
		process.QWAcc_Cent30Vz7_pT060 *
		process.QWAcc_Cent30Vz7_pT070 *
		process.QWAcc_Cent30Vz7_pT080 *
		process.QWAcc_Cent30Vz7_pT100 )

process.ana35Vz7 = cms.Path(
		process.pre_ana35Vz7*
		process.QWAcc_Cent35Vz7_pT004 *
		process.QWAcc_Cent35Vz7_pT005 *
		process.QWAcc_Cent35Vz7_pT006 *
		process.QWAcc_Cent35Vz7_pT008 *
		process.QWAcc_Cent35Vz7_pT010 *
		process.QWAcc_Cent35Vz7_pT012 *
		process.QWAcc_Cent35Vz7_pT015 *
		process.QWAcc_Cent35Vz7_pT020 *
		process.QWAcc_Cent35Vz7_pT025 *
		process.QWAcc_Cent35Vz7_pT030 *
		process.QWAcc_Cent35Vz7_pT035 *
		process.QWAcc_Cent35Vz7_pT040 *
		process.QWAcc_Cent35Vz7_pT050 *
		process.QWAcc_Cent35Vz7_pT060 *
		process.QWAcc_Cent35Vz7_pT070 *
		process.QWAcc_Cent35Vz7_pT080 *
		process.QWAcc_Cent35Vz7_pT100 )

process.ana40Vz7 = cms.Path(
		process.pre_ana40Vz7*
		process.QWAcc_Cent40Vz7_pT004 *
		process.QWAcc_Cent40Vz7_pT005 *
		process.QWAcc_Cent40Vz7_pT006 *
		process.QWAcc_Cent40Vz7_pT008 *
		process.QWAcc_Cent40Vz7_pT010 *
		process.QWAcc_Cent40Vz7_pT012 *
		process.QWAcc_Cent40Vz7_pT015 *
		process.QWAcc_Cent40Vz7_pT020 *
		process.QWAcc_Cent40Vz7_pT025 *
		process.QWAcc_Cent40Vz7_pT030 *
		process.QWAcc_Cent40Vz7_pT035 *
		process.QWAcc_Cent40Vz7_pT040 *
		process.QWAcc_Cent40Vz7_pT050 *
		process.QWAcc_Cent40Vz7_pT060 *
		process.QWAcc_Cent40Vz7_pT070 *
		process.QWAcc_Cent40Vz7_pT080 *
		process.QWAcc_Cent40Vz7_pT100 )

process.ana50Vz7 = cms.Path(
		process.pre_ana50Vz7*
		process.QWAcc_Cent50Vz7_pT004 *
		process.QWAcc_Cent50Vz7_pT005 *
		process.QWAcc_Cent50Vz7_pT006 *
		process.QWAcc_Cent50Vz7_pT008 *
		process.QWAcc_Cent50Vz7_pT010 *
		process.QWAcc_Cent50Vz7_pT012 *
		process.QWAcc_Cent50Vz7_pT015 *
		process.QWAcc_Cent50Vz7_pT020 *
		process.QWAcc_Cent50Vz7_pT025 *
		process.QWAcc_Cent50Vz7_pT030 *
		process.QWAcc_Cent50Vz7_pT035 *
		process.QWAcc_Cent50Vz7_pT040 *
		process.QWAcc_Cent50Vz7_pT050 *
		process.QWAcc_Cent50Vz7_pT060 *
		process.QWAcc_Cent50Vz7_pT070 *
		process.QWAcc_Cent50Vz7_pT080 *
		process.QWAcc_Cent50Vz7_pT100 )


process.ana60Vz7 = cms.Path(
		process.pre_ana60Vz7*
		process.QWAcc_Cent60Vz7_pT004 *
		process.QWAcc_Cent60Vz7_pT005 *
		process.QWAcc_Cent60Vz7_pT006 *
		process.QWAcc_Cent60Vz7_pT008 *
		process.QWAcc_Cent60Vz7_pT010 *
		process.QWAcc_Cent60Vz7_pT012 *
		process.QWAcc_Cent60Vz7_pT015 *
		process.QWAcc_Cent60Vz7_pT020 *
		process.QWAcc_Cent60Vz7_pT025 *
		process.QWAcc_Cent60Vz7_pT030 *
		process.QWAcc_Cent60Vz7_pT035 *
		process.QWAcc_Cent60Vz7_pT040 *
		process.QWAcc_Cent60Vz7_pT050 *
		process.QWAcc_Cent60Vz7_pT060 *
		process.QWAcc_Cent60Vz7_pT070 *
		process.QWAcc_Cent60Vz7_pT080 *
		process.QWAcc_Cent60Vz7_pT100 )


process.ana70Vz7 = cms.Path(
		process.pre_ana70Vz7*
		process.QWAcc_Cent70Vz7_pT004 *
		process.QWAcc_Cent70Vz7_pT005 *
		process.QWAcc_Cent70Vz7_pT006 *
		process.QWAcc_Cent70Vz7_pT008 *
		process.QWAcc_Cent70Vz7_pT010 *
		process.QWAcc_Cent70Vz7_pT012 *
		process.QWAcc_Cent70Vz7_pT015 *
		process.QWAcc_Cent70Vz7_pT020 *
		process.QWAcc_Cent70Vz7_pT025 *
		process.QWAcc_Cent70Vz7_pT030 *
		process.QWAcc_Cent70Vz7_pT035 *
		process.QWAcc_Cent70Vz7_pT040 *
		process.QWAcc_Cent70Vz7_pT050 *
		process.QWAcc_Cent70Vz7_pT060 *
		process.QWAcc_Cent70Vz7_pT070 *
		process.QWAcc_Cent70Vz7_pT080 *
		process.QWAcc_Cent70Vz7_pT100 )


process.ana80Vz7 = cms.Path(
		process.pre_ana80Vz7*
		process.QWAcc_Cent80Vz7_pT004 *
		process.QWAcc_Cent80Vz7_pT005 *
		process.QWAcc_Cent80Vz7_pT006 *
		process.QWAcc_Cent80Vz7_pT008 *
		process.QWAcc_Cent80Vz7_pT010 *
		process.QWAcc_Cent80Vz7_pT012 *
		process.QWAcc_Cent80Vz7_pT015 *
		process.QWAcc_Cent80Vz7_pT020 *
		process.QWAcc_Cent80Vz7_pT025 *
		process.QWAcc_Cent80Vz7_pT030 *
		process.QWAcc_Cent80Vz7_pT035 *
		process.QWAcc_Cent80Vz7_pT040 *
		process.QWAcc_Cent80Vz7_pT050 *
		process.QWAcc_Cent80Vz7_pT060 *
		process.QWAcc_Cent80Vz7_pT070 *
		process.QWAcc_Cent80Vz7_pT080 *
		process.QWAcc_Cent80Vz7_pT100 )


process.ana90Vz7 = cms.Path(
		process.pre_ana90Vz7*
		process.QWAcc_Cent90Vz7_pT004 *
		process.QWAcc_Cent90Vz7_pT005 *
		process.QWAcc_Cent90Vz7_pT006 *
		process.QWAcc_Cent90Vz7_pT008 *
		process.QWAcc_Cent90Vz7_pT010 *
		process.QWAcc_Cent90Vz7_pT012 *
		process.QWAcc_Cent90Vz7_pT015 *
		process.QWAcc_Cent90Vz7_pT020 *
		process.QWAcc_Cent90Vz7_pT025 *
		process.QWAcc_Cent90Vz7_pT030 *
		process.QWAcc_Cent90Vz7_pT035 *
		process.QWAcc_Cent90Vz7_pT040 *
		process.QWAcc_Cent90Vz7_pT050 *
		process.QWAcc_Cent90Vz7_pT060 *
		process.QWAcc_Cent90Vz7_pT070 *
		process.QWAcc_Cent90Vz7_pT080 *
		process.QWAcc_Cent90Vz7_pT100 )


process.ana00Vz7 = cms.Path(
		process.pre_ana00Vz7*
		process.QWAcc_Cent00Vz7_pT004 *
		process.QWAcc_Cent00Vz7_pT005 *
		process.QWAcc_Cent00Vz7_pT006 *
		process.QWAcc_Cent00Vz7_pT008 *
		process.QWAcc_Cent00Vz7_pT010 *
		process.QWAcc_Cent00Vz7_pT012 *
		process.QWAcc_Cent00Vz7_pT015 *
		process.QWAcc_Cent00Vz7_pT020 *
		process.QWAcc_Cent00Vz7_pT025 *
		process.QWAcc_Cent00Vz7_pT030 *
		process.QWAcc_Cent00Vz7_pT035 *
		process.QWAcc_Cent00Vz7_pT040 *
		process.QWAcc_Cent00Vz7_pT050 *
		process.QWAcc_Cent00Vz7_pT060 *
		process.QWAcc_Cent00Vz7_pT070 *
		process.QWAcc_Cent00Vz7_pT080 *
		process.QWAcc_Cent00Vz7_pT100 )


## Vz8
process.ana05Vz8 = cms.Path(
		process.pre_ana05Vz8*
		process.QWAcc_Cent05Vz8_pT004 *
		process.QWAcc_Cent05Vz8_pT005 *
		process.QWAcc_Cent05Vz8_pT006 *
		process.QWAcc_Cent05Vz8_pT008 *
		process.QWAcc_Cent05Vz8_pT010 *
		process.QWAcc_Cent05Vz8_pT012 *
		process.QWAcc_Cent05Vz8_pT015 *
		process.QWAcc_Cent05Vz8_pT020 *
		process.QWAcc_Cent05Vz8_pT025 *
		process.QWAcc_Cent05Vz8_pT030 *
		process.QWAcc_Cent05Vz8_pT035 *
		process.QWAcc_Cent05Vz8_pT040 *
		process.QWAcc_Cent05Vz8_pT050 *
		process.QWAcc_Cent05Vz8_pT060 *
		process.QWAcc_Cent05Vz8_pT070 *
		process.QWAcc_Cent05Vz8_pT080 *
		process.QWAcc_Cent05Vz8_pT100 )

process.ana10Vz8 = cms.Path(
		process.pre_ana10Vz8*
		process.QWAcc_Cent10Vz8_pT004 *
		process.QWAcc_Cent10Vz8_pT005 *
		process.QWAcc_Cent10Vz8_pT006 *
		process.QWAcc_Cent10Vz8_pT008 *
		process.QWAcc_Cent10Vz8_pT010 *
		process.QWAcc_Cent10Vz8_pT012 *
		process.QWAcc_Cent10Vz8_pT015 *
		process.QWAcc_Cent10Vz8_pT020 *
		process.QWAcc_Cent10Vz8_pT025 *
		process.QWAcc_Cent10Vz8_pT030 *
		process.QWAcc_Cent10Vz8_pT035 *
		process.QWAcc_Cent10Vz8_pT040 *
		process.QWAcc_Cent10Vz8_pT050 *
		process.QWAcc_Cent10Vz8_pT060 *
		process.QWAcc_Cent10Vz8_pT070 *
		process.QWAcc_Cent10Vz8_pT080 *
		process.QWAcc_Cent10Vz8_pT100 )

process.ana15Vz8 = cms.Path(
		process.pre_ana15Vz8*
		process.QWAcc_Cent15Vz8_pT004 *
		process.QWAcc_Cent15Vz8_pT005 *
		process.QWAcc_Cent15Vz8_pT006 *
		process.QWAcc_Cent15Vz8_pT008 *
		process.QWAcc_Cent15Vz8_pT010 *
		process.QWAcc_Cent15Vz8_pT012 *
		process.QWAcc_Cent15Vz8_pT015 *
		process.QWAcc_Cent15Vz8_pT020 *
		process.QWAcc_Cent15Vz8_pT025 *
		process.QWAcc_Cent15Vz8_pT030 *
		process.QWAcc_Cent15Vz8_pT035 *
		process.QWAcc_Cent15Vz8_pT040 *
		process.QWAcc_Cent15Vz8_pT050 *
		process.QWAcc_Cent15Vz8_pT060 *
		process.QWAcc_Cent15Vz8_pT070 *
		process.QWAcc_Cent15Vz8_pT080 *
		process.QWAcc_Cent15Vz8_pT100 )


process.ana20Vz8 = cms.Path(
		process.pre_ana20Vz8*
		process.QWAcc_Cent20Vz8_pT004 *
		process.QWAcc_Cent20Vz8_pT005 *
		process.QWAcc_Cent20Vz8_pT006 *
		process.QWAcc_Cent20Vz8_pT008 *
		process.QWAcc_Cent20Vz8_pT010 *
		process.QWAcc_Cent20Vz8_pT012 *
		process.QWAcc_Cent20Vz8_pT015 *
		process.QWAcc_Cent20Vz8_pT020 *
		process.QWAcc_Cent20Vz8_pT025 *
		process.QWAcc_Cent20Vz8_pT030 *
		process.QWAcc_Cent20Vz8_pT035 *
		process.QWAcc_Cent20Vz8_pT040 *
		process.QWAcc_Cent20Vz8_pT050 *
		process.QWAcc_Cent20Vz8_pT060 *
		process.QWAcc_Cent20Vz8_pT070 *
		process.QWAcc_Cent20Vz8_pT080 *
		process.QWAcc_Cent20Vz8_pT100 )

process.ana25Vz8 = cms.Path(
		process.pre_ana25Vz8*
		process.QWAcc_Cent25Vz8_pT004 *
		process.QWAcc_Cent25Vz8_pT005 *
		process.QWAcc_Cent25Vz8_pT006 *
		process.QWAcc_Cent25Vz8_pT008 *
		process.QWAcc_Cent25Vz8_pT010 *
		process.QWAcc_Cent25Vz8_pT012 *
		process.QWAcc_Cent25Vz8_pT015 *
		process.QWAcc_Cent25Vz8_pT020 *
		process.QWAcc_Cent25Vz8_pT025 *
		process.QWAcc_Cent25Vz8_pT030 *
		process.QWAcc_Cent25Vz8_pT035 *
		process.QWAcc_Cent25Vz8_pT040 *
		process.QWAcc_Cent25Vz8_pT050 *
		process.QWAcc_Cent25Vz8_pT060 *
		process.QWAcc_Cent25Vz8_pT070 *
		process.QWAcc_Cent25Vz8_pT080 *
		process.QWAcc_Cent25Vz8_pT100 )

process.ana30Vz8 = cms.Path(
		process.pre_ana30Vz8*
		process.QWAcc_Cent30Vz8_pT004 *
		process.QWAcc_Cent30Vz8_pT005 *
		process.QWAcc_Cent30Vz8_pT006 *
		process.QWAcc_Cent30Vz8_pT008 *
		process.QWAcc_Cent30Vz8_pT010 *
		process.QWAcc_Cent30Vz8_pT012 *
		process.QWAcc_Cent30Vz8_pT015 *
		process.QWAcc_Cent30Vz8_pT020 *
		process.QWAcc_Cent30Vz8_pT025 *
		process.QWAcc_Cent30Vz8_pT030 *
		process.QWAcc_Cent30Vz8_pT035 *
		process.QWAcc_Cent30Vz8_pT040 *
		process.QWAcc_Cent30Vz8_pT050 *
		process.QWAcc_Cent30Vz8_pT060 *
		process.QWAcc_Cent30Vz8_pT070 *
		process.QWAcc_Cent30Vz8_pT080 *
		process.QWAcc_Cent30Vz8_pT100 )

process.ana35Vz8 = cms.Path(
		process.pre_ana35Vz8*
		process.QWAcc_Cent35Vz8_pT004 *
		process.QWAcc_Cent35Vz8_pT005 *
		process.QWAcc_Cent35Vz8_pT006 *
		process.QWAcc_Cent35Vz8_pT008 *
		process.QWAcc_Cent35Vz8_pT010 *
		process.QWAcc_Cent35Vz8_pT012 *
		process.QWAcc_Cent35Vz8_pT015 *
		process.QWAcc_Cent35Vz8_pT020 *
		process.QWAcc_Cent35Vz8_pT025 *
		process.QWAcc_Cent35Vz8_pT030 *
		process.QWAcc_Cent35Vz8_pT035 *
		process.QWAcc_Cent35Vz8_pT040 *
		process.QWAcc_Cent35Vz8_pT050 *
		process.QWAcc_Cent35Vz8_pT060 *
		process.QWAcc_Cent35Vz8_pT070 *
		process.QWAcc_Cent35Vz8_pT080 *
		process.QWAcc_Cent35Vz8_pT100 )

process.ana40Vz8 = cms.Path(
		process.pre_ana40Vz8*
		process.QWAcc_Cent40Vz8_pT004 *
		process.QWAcc_Cent40Vz8_pT005 *
		process.QWAcc_Cent40Vz8_pT006 *
		process.QWAcc_Cent40Vz8_pT008 *
		process.QWAcc_Cent40Vz8_pT010 *
		process.QWAcc_Cent40Vz8_pT012 *
		process.QWAcc_Cent40Vz8_pT015 *
		process.QWAcc_Cent40Vz8_pT020 *
		process.QWAcc_Cent40Vz8_pT025 *
		process.QWAcc_Cent40Vz8_pT030 *
		process.QWAcc_Cent40Vz8_pT035 *
		process.QWAcc_Cent40Vz8_pT040 *
		process.QWAcc_Cent40Vz8_pT050 *
		process.QWAcc_Cent40Vz8_pT060 *
		process.QWAcc_Cent40Vz8_pT070 *
		process.QWAcc_Cent40Vz8_pT080 *
		process.QWAcc_Cent40Vz8_pT100 )

process.ana50Vz8 = cms.Path(
		process.pre_ana50Vz8*
		process.QWAcc_Cent50Vz8_pT004 *
		process.QWAcc_Cent50Vz8_pT005 *
		process.QWAcc_Cent50Vz8_pT006 *
		process.QWAcc_Cent50Vz8_pT008 *
		process.QWAcc_Cent50Vz8_pT010 *
		process.QWAcc_Cent50Vz8_pT012 *
		process.QWAcc_Cent50Vz8_pT015 *
		process.QWAcc_Cent50Vz8_pT020 *
		process.QWAcc_Cent50Vz8_pT025 *
		process.QWAcc_Cent50Vz8_pT030 *
		process.QWAcc_Cent50Vz8_pT035 *
		process.QWAcc_Cent50Vz8_pT040 *
		process.QWAcc_Cent50Vz8_pT050 *
		process.QWAcc_Cent50Vz8_pT060 *
		process.QWAcc_Cent50Vz8_pT070 *
		process.QWAcc_Cent50Vz8_pT080 *
		process.QWAcc_Cent50Vz8_pT100 )


process.ana60Vz8 = cms.Path(
		process.pre_ana60Vz8*
		process.QWAcc_Cent60Vz8_pT004 *
		process.QWAcc_Cent60Vz8_pT005 *
		process.QWAcc_Cent60Vz8_pT006 *
		process.QWAcc_Cent60Vz8_pT008 *
		process.QWAcc_Cent60Vz8_pT010 *
		process.QWAcc_Cent60Vz8_pT012 *
		process.QWAcc_Cent60Vz8_pT015 *
		process.QWAcc_Cent60Vz8_pT020 *
		process.QWAcc_Cent60Vz8_pT025 *
		process.QWAcc_Cent60Vz8_pT030 *
		process.QWAcc_Cent60Vz8_pT035 *
		process.QWAcc_Cent60Vz8_pT040 *
		process.QWAcc_Cent60Vz8_pT050 *
		process.QWAcc_Cent60Vz8_pT060 *
		process.QWAcc_Cent60Vz8_pT070 *
		process.QWAcc_Cent60Vz8_pT080 *
		process.QWAcc_Cent60Vz8_pT100 )


process.ana70Vz8 = cms.Path(
		process.pre_ana70Vz8*
		process.QWAcc_Cent70Vz8_pT004 *
		process.QWAcc_Cent70Vz8_pT005 *
		process.QWAcc_Cent70Vz8_pT006 *
		process.QWAcc_Cent70Vz8_pT008 *
		process.QWAcc_Cent70Vz8_pT010 *
		process.QWAcc_Cent70Vz8_pT012 *
		process.QWAcc_Cent70Vz8_pT015 *
		process.QWAcc_Cent70Vz8_pT020 *
		process.QWAcc_Cent70Vz8_pT025 *
		process.QWAcc_Cent70Vz8_pT030 *
		process.QWAcc_Cent70Vz8_pT035 *
		process.QWAcc_Cent70Vz8_pT040 *
		process.QWAcc_Cent70Vz8_pT050 *
		process.QWAcc_Cent70Vz8_pT060 *
		process.QWAcc_Cent70Vz8_pT070 *
		process.QWAcc_Cent70Vz8_pT080 *
		process.QWAcc_Cent70Vz8_pT100 )


process.ana80Vz8 = cms.Path(
		process.pre_ana80Vz8*
		process.QWAcc_Cent80Vz8_pT004 *
		process.QWAcc_Cent80Vz8_pT005 *
		process.QWAcc_Cent80Vz8_pT006 *
		process.QWAcc_Cent80Vz8_pT008 *
		process.QWAcc_Cent80Vz8_pT010 *
		process.QWAcc_Cent80Vz8_pT012 *
		process.QWAcc_Cent80Vz8_pT015 *
		process.QWAcc_Cent80Vz8_pT020 *
		process.QWAcc_Cent80Vz8_pT025 *
		process.QWAcc_Cent80Vz8_pT030 *
		process.QWAcc_Cent80Vz8_pT035 *
		process.QWAcc_Cent80Vz8_pT040 *
		process.QWAcc_Cent80Vz8_pT050 *
		process.QWAcc_Cent80Vz8_pT060 *
		process.QWAcc_Cent80Vz8_pT070 *
		process.QWAcc_Cent80Vz8_pT080 *
		process.QWAcc_Cent80Vz8_pT100 )


process.ana90Vz8 = cms.Path(
		process.pre_ana90Vz8*
		process.QWAcc_Cent90Vz8_pT004 *
		process.QWAcc_Cent90Vz8_pT005 *
		process.QWAcc_Cent90Vz8_pT006 *
		process.QWAcc_Cent90Vz8_pT008 *
		process.QWAcc_Cent90Vz8_pT010 *
		process.QWAcc_Cent90Vz8_pT012 *
		process.QWAcc_Cent90Vz8_pT015 *
		process.QWAcc_Cent90Vz8_pT020 *
		process.QWAcc_Cent90Vz8_pT025 *
		process.QWAcc_Cent90Vz8_pT030 *
		process.QWAcc_Cent90Vz8_pT035 *
		process.QWAcc_Cent90Vz8_pT040 *
		process.QWAcc_Cent90Vz8_pT050 *
		process.QWAcc_Cent90Vz8_pT060 *
		process.QWAcc_Cent90Vz8_pT070 *
		process.QWAcc_Cent90Vz8_pT080 *
		process.QWAcc_Cent90Vz8_pT100 )


process.ana00Vz8 = cms.Path(
		process.pre_ana00Vz8*
		process.QWAcc_Cent00Vz8_pT004 *
		process.QWAcc_Cent00Vz8_pT005 *
		process.QWAcc_Cent00Vz8_pT006 *
		process.QWAcc_Cent00Vz8_pT008 *
		process.QWAcc_Cent00Vz8_pT010 *
		process.QWAcc_Cent00Vz8_pT012 *
		process.QWAcc_Cent00Vz8_pT015 *
		process.QWAcc_Cent00Vz8_pT020 *
		process.QWAcc_Cent00Vz8_pT025 *
		process.QWAcc_Cent00Vz8_pT030 *
		process.QWAcc_Cent00Vz8_pT035 *
		process.QWAcc_Cent00Vz8_pT040 *
		process.QWAcc_Cent00Vz8_pT050 *
		process.QWAcc_Cent00Vz8_pT060 *
		process.QWAcc_Cent00Vz8_pT070 *
		process.QWAcc_Cent00Vz8_pT080 *
		process.QWAcc_Cent00Vz8_pT100 )


## Vz9
process.ana05Vz9 = cms.Path(
		process.pre_ana05Vz9*
		process.QWAcc_Cent05Vz9_pT004 *
		process.QWAcc_Cent05Vz9_pT005 *
		process.QWAcc_Cent05Vz9_pT006 *
		process.QWAcc_Cent05Vz9_pT008 *
		process.QWAcc_Cent05Vz9_pT010 *
		process.QWAcc_Cent05Vz9_pT012 *
		process.QWAcc_Cent05Vz9_pT015 *
		process.QWAcc_Cent05Vz9_pT020 *
		process.QWAcc_Cent05Vz9_pT025 *
		process.QWAcc_Cent05Vz9_pT030 *
		process.QWAcc_Cent05Vz9_pT035 *
		process.QWAcc_Cent05Vz9_pT040 *
		process.QWAcc_Cent05Vz9_pT050 *
		process.QWAcc_Cent05Vz9_pT060 *
		process.QWAcc_Cent05Vz9_pT070 *
		process.QWAcc_Cent05Vz9_pT080 *
		process.QWAcc_Cent05Vz9_pT100 )

process.ana10Vz9 = cms.Path(
		process.pre_ana10Vz9*
		process.QWAcc_Cent10Vz9_pT004 *
		process.QWAcc_Cent10Vz9_pT005 *
		process.QWAcc_Cent10Vz9_pT006 *
		process.QWAcc_Cent10Vz9_pT008 *
		process.QWAcc_Cent10Vz9_pT010 *
		process.QWAcc_Cent10Vz9_pT012 *
		process.QWAcc_Cent10Vz9_pT015 *
		process.QWAcc_Cent10Vz9_pT020 *
		process.QWAcc_Cent10Vz9_pT025 *
		process.QWAcc_Cent10Vz9_pT030 *
		process.QWAcc_Cent10Vz9_pT035 *
		process.QWAcc_Cent10Vz9_pT040 *
		process.QWAcc_Cent10Vz9_pT050 *
		process.QWAcc_Cent10Vz9_pT060 *
		process.QWAcc_Cent10Vz9_pT070 *
		process.QWAcc_Cent10Vz9_pT080 *
		process.QWAcc_Cent10Vz9_pT100 )

process.ana15Vz9 = cms.Path(
		process.pre_ana15Vz9*
		process.QWAcc_Cent15Vz9_pT004 *
		process.QWAcc_Cent15Vz9_pT005 *
		process.QWAcc_Cent15Vz9_pT006 *
		process.QWAcc_Cent15Vz9_pT008 *
		process.QWAcc_Cent15Vz9_pT010 *
		process.QWAcc_Cent15Vz9_pT012 *
		process.QWAcc_Cent15Vz9_pT015 *
		process.QWAcc_Cent15Vz9_pT020 *
		process.QWAcc_Cent15Vz9_pT025 *
		process.QWAcc_Cent15Vz9_pT030 *
		process.QWAcc_Cent15Vz9_pT035 *
		process.QWAcc_Cent15Vz9_pT040 *
		process.QWAcc_Cent15Vz9_pT050 *
		process.QWAcc_Cent15Vz9_pT060 *
		process.QWAcc_Cent15Vz9_pT070 *
		process.QWAcc_Cent15Vz9_pT080 *
		process.QWAcc_Cent15Vz9_pT100 )


process.ana20Vz9 = cms.Path(
		process.pre_ana20Vz9*
		process.QWAcc_Cent20Vz9_pT004 *
		process.QWAcc_Cent20Vz9_pT005 *
		process.QWAcc_Cent20Vz9_pT006 *
		process.QWAcc_Cent20Vz9_pT008 *
		process.QWAcc_Cent20Vz9_pT010 *
		process.QWAcc_Cent20Vz9_pT012 *
		process.QWAcc_Cent20Vz9_pT015 *
		process.QWAcc_Cent20Vz9_pT020 *
		process.QWAcc_Cent20Vz9_pT025 *
		process.QWAcc_Cent20Vz9_pT030 *
		process.QWAcc_Cent20Vz9_pT035 *
		process.QWAcc_Cent20Vz9_pT040 *
		process.QWAcc_Cent20Vz9_pT050 *
		process.QWAcc_Cent20Vz9_pT060 *
		process.QWAcc_Cent20Vz9_pT070 *
		process.QWAcc_Cent20Vz9_pT080 *
		process.QWAcc_Cent20Vz9_pT100 )

process.ana25Vz9 = cms.Path(
		process.pre_ana25Vz9*
		process.QWAcc_Cent25Vz9_pT004 *
		process.QWAcc_Cent25Vz9_pT005 *
		process.QWAcc_Cent25Vz9_pT006 *
		process.QWAcc_Cent25Vz9_pT008 *
		process.QWAcc_Cent25Vz9_pT010 *
		process.QWAcc_Cent25Vz9_pT012 *
		process.QWAcc_Cent25Vz9_pT015 *
		process.QWAcc_Cent25Vz9_pT020 *
		process.QWAcc_Cent25Vz9_pT025 *
		process.QWAcc_Cent25Vz9_pT030 *
		process.QWAcc_Cent25Vz9_pT035 *
		process.QWAcc_Cent25Vz9_pT040 *
		process.QWAcc_Cent25Vz9_pT050 *
		process.QWAcc_Cent25Vz9_pT060 *
		process.QWAcc_Cent25Vz9_pT070 *
		process.QWAcc_Cent25Vz9_pT080 *
		process.QWAcc_Cent25Vz9_pT100 )

process.ana30Vz9 = cms.Path(
		process.pre_ana30Vz9*
		process.QWAcc_Cent30Vz9_pT004 *
		process.QWAcc_Cent30Vz9_pT005 *
		process.QWAcc_Cent30Vz9_pT006 *
		process.QWAcc_Cent30Vz9_pT008 *
		process.QWAcc_Cent30Vz9_pT010 *
		process.QWAcc_Cent30Vz9_pT012 *
		process.QWAcc_Cent30Vz9_pT015 *
		process.QWAcc_Cent30Vz9_pT020 *
		process.QWAcc_Cent30Vz9_pT025 *
		process.QWAcc_Cent30Vz9_pT030 *
		process.QWAcc_Cent30Vz9_pT035 *
		process.QWAcc_Cent30Vz9_pT040 *
		process.QWAcc_Cent30Vz9_pT050 *
		process.QWAcc_Cent30Vz9_pT060 *
		process.QWAcc_Cent30Vz9_pT070 *
		process.QWAcc_Cent30Vz9_pT080 *
		process.QWAcc_Cent30Vz9_pT100 )

process.ana35Vz9 = cms.Path(
		process.pre_ana35Vz9*
		process.QWAcc_Cent35Vz9_pT004 *
		process.QWAcc_Cent35Vz9_pT005 *
		process.QWAcc_Cent35Vz9_pT006 *
		process.QWAcc_Cent35Vz9_pT008 *
		process.QWAcc_Cent35Vz9_pT010 *
		process.QWAcc_Cent35Vz9_pT012 *
		process.QWAcc_Cent35Vz9_pT015 *
		process.QWAcc_Cent35Vz9_pT020 *
		process.QWAcc_Cent35Vz9_pT025 *
		process.QWAcc_Cent35Vz9_pT030 *
		process.QWAcc_Cent35Vz9_pT035 *
		process.QWAcc_Cent35Vz9_pT040 *
		process.QWAcc_Cent35Vz9_pT050 *
		process.QWAcc_Cent35Vz9_pT060 *
		process.QWAcc_Cent35Vz9_pT070 *
		process.QWAcc_Cent35Vz9_pT080 *
		process.QWAcc_Cent35Vz9_pT100 )

process.ana40Vz9 = cms.Path(
		process.pre_ana40Vz9*
		process.QWAcc_Cent40Vz9_pT004 *
		process.QWAcc_Cent40Vz9_pT005 *
		process.QWAcc_Cent40Vz9_pT006 *
		process.QWAcc_Cent40Vz9_pT008 *
		process.QWAcc_Cent40Vz9_pT010 *
		process.QWAcc_Cent40Vz9_pT012 *
		process.QWAcc_Cent40Vz9_pT015 *
		process.QWAcc_Cent40Vz9_pT020 *
		process.QWAcc_Cent40Vz9_pT025 *
		process.QWAcc_Cent40Vz9_pT030 *
		process.QWAcc_Cent40Vz9_pT035 *
		process.QWAcc_Cent40Vz9_pT040 *
		process.QWAcc_Cent40Vz9_pT050 *
		process.QWAcc_Cent40Vz9_pT060 *
		process.QWAcc_Cent40Vz9_pT070 *
		process.QWAcc_Cent40Vz9_pT080 *
		process.QWAcc_Cent40Vz9_pT100 )

process.ana50Vz9 = cms.Path(
		process.pre_ana50Vz9*
		process.QWAcc_Cent50Vz9_pT004 *
		process.QWAcc_Cent50Vz9_pT005 *
		process.QWAcc_Cent50Vz9_pT006 *
		process.QWAcc_Cent50Vz9_pT008 *
		process.QWAcc_Cent50Vz9_pT010 *
		process.QWAcc_Cent50Vz9_pT012 *
		process.QWAcc_Cent50Vz9_pT015 *
		process.QWAcc_Cent50Vz9_pT020 *
		process.QWAcc_Cent50Vz9_pT025 *
		process.QWAcc_Cent50Vz9_pT030 *
		process.QWAcc_Cent50Vz9_pT035 *
		process.QWAcc_Cent50Vz9_pT040 *
		process.QWAcc_Cent50Vz9_pT050 *
		process.QWAcc_Cent50Vz9_pT060 *
		process.QWAcc_Cent50Vz9_pT070 *
		process.QWAcc_Cent50Vz9_pT080 *
		process.QWAcc_Cent50Vz9_pT100 )


process.ana60Vz9 = cms.Path(
		process.pre_ana60Vz9*
		process.QWAcc_Cent60Vz9_pT004 *
		process.QWAcc_Cent60Vz9_pT005 *
		process.QWAcc_Cent60Vz9_pT006 *
		process.QWAcc_Cent60Vz9_pT008 *
		process.QWAcc_Cent60Vz9_pT010 *
		process.QWAcc_Cent60Vz9_pT012 *
		process.QWAcc_Cent60Vz9_pT015 *
		process.QWAcc_Cent60Vz9_pT020 *
		process.QWAcc_Cent60Vz9_pT025 *
		process.QWAcc_Cent60Vz9_pT030 *
		process.QWAcc_Cent60Vz9_pT035 *
		process.QWAcc_Cent60Vz9_pT040 *
		process.QWAcc_Cent60Vz9_pT050 *
		process.QWAcc_Cent60Vz9_pT060 *
		process.QWAcc_Cent60Vz9_pT070 *
		process.QWAcc_Cent60Vz9_pT080 *
		process.QWAcc_Cent60Vz9_pT100 )


process.ana70Vz9 = cms.Path(
		process.pre_ana70Vz9*
		process.QWAcc_Cent70Vz9_pT004 *
		process.QWAcc_Cent70Vz9_pT005 *
		process.QWAcc_Cent70Vz9_pT006 *
		process.QWAcc_Cent70Vz9_pT008 *
		process.QWAcc_Cent70Vz9_pT010 *
		process.QWAcc_Cent70Vz9_pT012 *
		process.QWAcc_Cent70Vz9_pT015 *
		process.QWAcc_Cent70Vz9_pT020 *
		process.QWAcc_Cent70Vz9_pT025 *
		process.QWAcc_Cent70Vz9_pT030 *
		process.QWAcc_Cent70Vz9_pT035 *
		process.QWAcc_Cent70Vz9_pT040 *
		process.QWAcc_Cent70Vz9_pT050 *
		process.QWAcc_Cent70Vz9_pT060 *
		process.QWAcc_Cent70Vz9_pT070 *
		process.QWAcc_Cent70Vz9_pT080 *
		process.QWAcc_Cent70Vz9_pT100 )


process.ana80Vz9 = cms.Path(
		process.pre_ana80Vz9*
		process.QWAcc_Cent80Vz9_pT004 *
		process.QWAcc_Cent80Vz9_pT005 *
		process.QWAcc_Cent80Vz9_pT006 *
		process.QWAcc_Cent80Vz9_pT008 *
		process.QWAcc_Cent80Vz9_pT010 *
		process.QWAcc_Cent80Vz9_pT012 *
		process.QWAcc_Cent80Vz9_pT015 *
		process.QWAcc_Cent80Vz9_pT020 *
		process.QWAcc_Cent80Vz9_pT025 *
		process.QWAcc_Cent80Vz9_pT030 *
		process.QWAcc_Cent80Vz9_pT035 *
		process.QWAcc_Cent80Vz9_pT040 *
		process.QWAcc_Cent80Vz9_pT050 *
		process.QWAcc_Cent80Vz9_pT060 *
		process.QWAcc_Cent80Vz9_pT070 *
		process.QWAcc_Cent80Vz9_pT080 *
		process.QWAcc_Cent80Vz9_pT100 )


process.ana90Vz9 = cms.Path(
		process.pre_ana90Vz9*
		process.QWAcc_Cent90Vz9_pT004 *
		process.QWAcc_Cent90Vz9_pT005 *
		process.QWAcc_Cent90Vz9_pT006 *
		process.QWAcc_Cent90Vz9_pT008 *
		process.QWAcc_Cent90Vz9_pT010 *
		process.QWAcc_Cent90Vz9_pT012 *
		process.QWAcc_Cent90Vz9_pT015 *
		process.QWAcc_Cent90Vz9_pT020 *
		process.QWAcc_Cent90Vz9_pT025 *
		process.QWAcc_Cent90Vz9_pT030 *
		process.QWAcc_Cent90Vz9_pT035 *
		process.QWAcc_Cent90Vz9_pT040 *
		process.QWAcc_Cent90Vz9_pT050 *
		process.QWAcc_Cent90Vz9_pT060 *
		process.QWAcc_Cent90Vz9_pT070 *
		process.QWAcc_Cent90Vz9_pT080 *
		process.QWAcc_Cent90Vz9_pT100 )


process.ana00Vz9 = cms.Path(
		process.pre_ana00Vz9*
		process.QWAcc_Cent00Vz9_pT004 *
		process.QWAcc_Cent00Vz9_pT005 *
		process.QWAcc_Cent00Vz9_pT006 *
		process.QWAcc_Cent00Vz9_pT008 *
		process.QWAcc_Cent00Vz9_pT010 *
		process.QWAcc_Cent00Vz9_pT012 *
		process.QWAcc_Cent00Vz9_pT015 *
		process.QWAcc_Cent00Vz9_pT020 *
		process.QWAcc_Cent00Vz9_pT025 *
		process.QWAcc_Cent00Vz9_pT030 *
		process.QWAcc_Cent00Vz9_pT035 *
		process.QWAcc_Cent00Vz9_pT040 *
		process.QWAcc_Cent00Vz9_pT050 *
		process.QWAcc_Cent00Vz9_pT060 *
		process.QWAcc_Cent00Vz9_pT070 *
		process.QWAcc_Cent00Vz9_pT080 *
		process.QWAcc_Cent00Vz9_pT100 )


process.ana = cms.Path(process.pre_ana*process.cumugap )

process.schedule = cms.Schedule(
#	process.ana,

	process.ana05Vz0,
	process.ana10Vz0,
	process.ana15Vz0,
	process.ana20Vz0,
	process.ana25Vz0,
	process.ana30Vz0,
	process.ana35Vz0,
	process.ana40Vz0,
	process.ana50Vz0,
	process.ana60Vz0,
	process.ana70Vz0,
	process.ana80Vz0,
	process.ana90Vz0,
	process.ana00Vz0,

	process.ana05Vz1,
	process.ana10Vz1,
	process.ana15Vz1,
	process.ana20Vz1,
	process.ana25Vz1,
	process.ana30Vz1,
	process.ana35Vz1,
	process.ana40Vz1,
	process.ana50Vz1,
	process.ana60Vz1,
	process.ana70Vz1,
	process.ana80Vz1,
	process.ana90Vz1,
	process.ana00Vz1,

	process.ana05Vz2,
	process.ana10Vz2,
	process.ana15Vz2,
	process.ana20Vz2,
	process.ana25Vz2,
	process.ana30Vz2,
	process.ana35Vz2,
	process.ana40Vz2,
	process.ana50Vz2,
	process.ana60Vz2,
	process.ana70Vz2,
	process.ana80Vz2,
	process.ana90Vz2,
	process.ana00Vz2,

	process.ana05Vz3,
	process.ana10Vz3,
	process.ana15Vz3,
	process.ana20Vz3,
	process.ana25Vz3,
	process.ana30Vz3,
	process.ana35Vz3,
	process.ana40Vz3,
	process.ana50Vz3,
	process.ana60Vz3,
	process.ana70Vz3,
	process.ana80Vz3,
	process.ana90Vz3,
	process.ana00Vz3,

	process.ana05Vz4,
	process.ana10Vz4,
	process.ana15Vz4,
	process.ana20Vz4,
	process.ana25Vz4,
	process.ana30Vz4,
	process.ana35Vz4,
	process.ana40Vz4,
	process.ana50Vz4,
	process.ana60Vz4,
	process.ana70Vz4,
	process.ana80Vz4,
	process.ana90Vz4,
	process.ana00Vz4,

	process.ana05Vz5,
	process.ana10Vz5,
	process.ana15Vz5,
	process.ana20Vz5,
	process.ana25Vz5,
	process.ana30Vz5,
	process.ana35Vz5,
	process.ana40Vz5,
	process.ana50Vz5,
	process.ana60Vz5,
	process.ana70Vz5,
	process.ana80Vz5,
	process.ana90Vz5,
	process.ana00Vz5,

	process.ana05Vz6,
	process.ana10Vz6,
	process.ana15Vz6,
	process.ana20Vz6,
	process.ana25Vz6,
	process.ana30Vz6,
	process.ana35Vz6,
	process.ana40Vz6,
	process.ana50Vz6,
	process.ana60Vz6,
	process.ana70Vz6,
	process.ana80Vz6,
	process.ana90Vz6,
	process.ana00Vz6,

	process.ana05Vz7,
	process.ana10Vz7,
	process.ana15Vz7,
	process.ana20Vz7,
	process.ana25Vz7,
	process.ana30Vz7,
	process.ana35Vz7,
	process.ana40Vz7,
	process.ana50Vz7,
	process.ana60Vz7,
	process.ana70Vz7,
	process.ana80Vz7,
	process.ana90Vz7,
	process.ana00Vz7,

	process.ana05Vz8,
	process.ana10Vz8,
	process.ana15Vz8,
	process.ana20Vz8,
	process.ana25Vz8,
	process.ana30Vz8,
	process.ana35Vz8,
	process.ana40Vz8,
	process.ana50Vz8,
	process.ana60Vz8,
	process.ana70Vz8,
	process.ana80Vz8,
	process.ana90Vz8,
	process.ana00Vz8,

	process.ana05Vz9,
	process.ana10Vz9,
	process.ana15Vz9,
	process.ana20Vz9,
	process.ana25Vz9,
	process.ana30Vz9,
	process.ana35Vz9,
	process.ana40Vz9,
	process.ana50Vz9,
	process.ana60Vz9,
	process.ana70Vz9,
	process.ana80Vz9,
	process.ana90Vz9,
	process.ana00Vz9,

)
