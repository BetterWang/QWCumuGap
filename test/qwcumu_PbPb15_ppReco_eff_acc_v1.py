import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuGap")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

#from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/ppReco.root")
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
	, centrality = cms.untracked.InputTag('Noff')
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

process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')

process.primaryVertexFilter.src = cms.InputTag("offlinePrimaryVertices")

process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
process.ppRecoCentFilter = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(60, 180)
		),
	BinLabel = cms.InputTag("centralityBins")
	)


process.NoffFilter120 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(0, 120)
		),
	BinLabel = cms.InputTag("Noff")
	)



process.NoffFilter260 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(120, 260)
		),
	BinLabel = cms.InputTag("Noff")
	)



process.NoffFilter400 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(260, 400)
		),
	BinLabel = cms.InputTag("Noff")
	)


process.NoffFilter800 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(400, 800)
		),
	BinLabel = cms.InputTag("Noff")
	)



process.NoffFilter1200 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(800, 1200)
		),
	BinLabel = cms.InputTag("Noff")
	)


process.NoffFilter2000 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(1200, 2000)
		),
	BinLabel = cms.InputTag("Noff")
	)

process.eventSelection = cms.Sequence(
        process.hfCoincFilter3
        + process.primaryVertexFilter
#        + process.clusterCompatibilityFilter
)



process.QWAcc_Noff120Vz0_pT004 = cms.EDAnalyzer("QWEventAccAnalyzer",
		srcPhi = cms.untracked.InputTag("QWEvent", "phi"),
		srcEta = cms.untracked.InputTag("QWEvent", "eta"),
		srcPt = cms.untracked.InputTag("QWEvent", "pt"),
		srcWeight = cms.untracked.InputTag("QWEvent", "weight"),
		minPt = cms.untracked.double(0.3),
		maxPt = cms.untracked.double(0.4)
		)

process.QWAcc_Noff120Vz0_pT005 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(0.4),
		maxPt = cms.untracked.double(0.5)
		)


process.QWAcc_Noff120Vz0_pT006 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(0.5),
		maxPt = cms.untracked.double(0.6)
		)

process.QWAcc_Noff120Vz0_pT008 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(0.6),
		maxPt = cms.untracked.double(0.8)
		)

process.QWAcc_Noff120Vz0_pT010 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(0.8),
		maxPt = cms.untracked.double(1.0)
		)

process.QWAcc_Noff120Vz0_pT012 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(1.0),
		maxPt = cms.untracked.double(1.25)
		)

process.QWAcc_Noff120Vz0_pT015 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(1.25),
		maxPt = cms.untracked.double(1.5)
		)

process.QWAcc_Noff120Vz0_pT020 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(1.5),
		maxPt = cms.untracked.double(2.0)
		)

process.QWAcc_Noff120Vz0_pT025 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(2.0),
		maxPt = cms.untracked.double(2.5)
		)


process.QWAcc_Noff120Vz0_pT030 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(2.5),
		maxPt = cms.untracked.double(3.0)
		)

process.QWAcc_Noff120Vz0_pT035 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(3.0),
		maxPt = cms.untracked.double(3.5)
		)

process.QWAcc_Noff120Vz0_pT040 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(3.5),
		maxPt = cms.untracked.double(4.0)
		)

process.QWAcc_Noff120Vz0_pT050 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(4.0),
		maxPt = cms.untracked.double(5.0)
		)

process.QWAcc_Noff120Vz0_pT060 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(5.0),
		maxPt = cms.untracked.double(6.0)
		)

process.QWAcc_Noff120Vz0_pT070 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(6.0),
		maxPt = cms.untracked.double(7.0)
		)

process.QWAcc_Noff120Vz0_pT080 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(7.0),
		maxPt = cms.untracked.double(8.0)
		)

process.QWAcc_Noff120Vz0_pT100 = process.QWAcc_Noff120Vz0_pT004.clone(
		minPt = cms.untracked.double(8.0),
		maxPt = cms.untracked.double(10.0)
		)

# Vz0
process.QWAcc_Noff260Vz0_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff400Vz0_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff800Vz0_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff12XVz0_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff20XVz0_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()

process.QWAcc_Noff260Vz0_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff400Vz0_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff800Vz0_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff12XVz0_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff20XVz0_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()

process.QWAcc_Noff260Vz0_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff400Vz0_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff800Vz0_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff12XVz0_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff20XVz0_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()

process.QWAcc_Noff260Vz0_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff400Vz0_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff800Vz0_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff12XVz0_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff20XVz0_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()

process.QWAcc_Noff260Vz0_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff400Vz0_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff800Vz0_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff12XVz0_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff20XVz0_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()

process.QWAcc_Noff260Vz0_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff400Vz0_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff800Vz0_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff12XVz0_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff20XVz0_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()

process.QWAcc_Noff260Vz0_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff400Vz0_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff800Vz0_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff12XVz0_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff20XVz0_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()

process.QWAcc_Noff260Vz0_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff400Vz0_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff800Vz0_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff12XVz0_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff20XVz0_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()

process.QWAcc_Noff260Vz0_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff400Vz0_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff800Vz0_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff12XVz0_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff20XVz0_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()

process.QWAcc_Noff260Vz0_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff400Vz0_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff800Vz0_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff12XVz0_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff20XVz0_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()

process.QWAcc_Noff260Vz0_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff400Vz0_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff800Vz0_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff12XVz0_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff20XVz0_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()

process.QWAcc_Noff260Vz0_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff400Vz0_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff800Vz0_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff12XVz0_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff20XVz0_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()

process.QWAcc_Noff260Vz0_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff400Vz0_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff800Vz0_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff12XVz0_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff20XVz0_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()

process.QWAcc_Noff260Vz0_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff400Vz0_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff800Vz0_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff12XVz0_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff20XVz0_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()

process.QWAcc_Noff260Vz0_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff400Vz0_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff800Vz0_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff12XVz0_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff20XVz0_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()

process.QWAcc_Noff260Vz0_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff400Vz0_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff800Vz0_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff12XVz0_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff20XVz0_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()

process.QWAcc_Noff260Vz0_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff400Vz0_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff800Vz0_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff12XVz0_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff20XVz0_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()

# Vz1
process.QWAcc_Noff120Vz1_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff260Vz1_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff400Vz1_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff800Vz1_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff12XVz1_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff20XVz1_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()

process.QWAcc_Noff120Vz1_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff260Vz1_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff400Vz1_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff800Vz1_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff12XVz1_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff20XVz1_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()

process.QWAcc_Noff120Vz1_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff260Vz1_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff400Vz1_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff800Vz1_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff12XVz1_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff20XVz1_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()

process.QWAcc_Noff120Vz1_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff260Vz1_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff400Vz1_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff800Vz1_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff12XVz1_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff20XVz1_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()

process.QWAcc_Noff120Vz1_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff260Vz1_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff400Vz1_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff800Vz1_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff12XVz1_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff20XVz1_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()

process.QWAcc_Noff120Vz1_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff260Vz1_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff400Vz1_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff800Vz1_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff12XVz1_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff20XVz1_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()

process.QWAcc_Noff120Vz1_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff260Vz1_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff400Vz1_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff800Vz1_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff12XVz1_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff20XVz1_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()

process.QWAcc_Noff120Vz1_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff260Vz1_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff400Vz1_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff800Vz1_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff12XVz1_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff20XVz1_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()

process.QWAcc_Noff120Vz1_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff260Vz1_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff400Vz1_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff800Vz1_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff12XVz1_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff20XVz1_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()

process.QWAcc_Noff120Vz1_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff260Vz1_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff400Vz1_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff800Vz1_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff12XVz1_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff20XVz1_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()

process.QWAcc_Noff120Vz1_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff260Vz1_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff400Vz1_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff800Vz1_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff12XVz1_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff20XVz1_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()

process.QWAcc_Noff120Vz1_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff260Vz1_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff400Vz1_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff800Vz1_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff12XVz1_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff20XVz1_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()

process.QWAcc_Noff120Vz1_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff260Vz1_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff400Vz1_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff800Vz1_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff12XVz1_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff20XVz1_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()

process.QWAcc_Noff120Vz1_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff260Vz1_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff400Vz1_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff800Vz1_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff12XVz1_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff20XVz1_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()

process.QWAcc_Noff120Vz1_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff260Vz1_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff400Vz1_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff800Vz1_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff12XVz1_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff20XVz1_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()

process.QWAcc_Noff120Vz1_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff260Vz1_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff400Vz1_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff800Vz1_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff12XVz1_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff20XVz1_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()

process.QWAcc_Noff120Vz1_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff260Vz1_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff400Vz1_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff800Vz1_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff12XVz1_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff20XVz1_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()


# Vz2
process.QWAcc_Noff120Vz2_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff260Vz2_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff400Vz2_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff800Vz2_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff12XVz2_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff20XVz2_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()

process.QWAcc_Noff120Vz2_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff260Vz2_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff400Vz2_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff800Vz2_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff12XVz2_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff20XVz2_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()

process.QWAcc_Noff120Vz2_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff260Vz2_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff400Vz2_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff800Vz2_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff12XVz2_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff20XVz2_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()

process.QWAcc_Noff120Vz2_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff260Vz2_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff400Vz2_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff800Vz2_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff12XVz2_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff20XVz2_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()

process.QWAcc_Noff120Vz2_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff260Vz2_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff400Vz2_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff800Vz2_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff12XVz2_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff20XVz2_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()

process.QWAcc_Noff120Vz2_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff260Vz2_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff400Vz2_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff800Vz2_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff12XVz2_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff20XVz2_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()

process.QWAcc_Noff120Vz2_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff260Vz2_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff400Vz2_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff800Vz2_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff12XVz2_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff20XVz2_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()

process.QWAcc_Noff120Vz2_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff260Vz2_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff400Vz2_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff800Vz2_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff12XVz2_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff20XVz2_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()

process.QWAcc_Noff120Vz2_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff260Vz2_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff400Vz2_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff800Vz2_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff12XVz2_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff20XVz2_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()

process.QWAcc_Noff120Vz2_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff260Vz2_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff400Vz2_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff800Vz2_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff12XVz2_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff20XVz2_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()

process.QWAcc_Noff120Vz2_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff260Vz2_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff400Vz2_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff800Vz2_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff12XVz2_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff20XVz2_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()

process.QWAcc_Noff120Vz2_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff260Vz2_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff400Vz2_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff800Vz2_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff12XVz2_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff20XVz2_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()

process.QWAcc_Noff120Vz2_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff260Vz2_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff400Vz2_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff800Vz2_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff12XVz2_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff20XVz2_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()

process.QWAcc_Noff120Vz2_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff260Vz2_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff400Vz2_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff800Vz2_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff12XVz2_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff20XVz2_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()

process.QWAcc_Noff120Vz2_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff260Vz2_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff400Vz2_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff800Vz2_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff12XVz2_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff20XVz2_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()

process.QWAcc_Noff120Vz2_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff260Vz2_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff400Vz2_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff800Vz2_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff12XVz2_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff20XVz2_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()

process.QWAcc_Noff120Vz2_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff260Vz2_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff400Vz2_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff800Vz2_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff12XVz2_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff20XVz2_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()


# Vz3
process.QWAcc_Noff120Vz3_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff260Vz3_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff400Vz3_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff800Vz3_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff12XVz3_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff20XVz3_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()

process.QWAcc_Noff120Vz3_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff260Vz3_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff400Vz3_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff800Vz3_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff12XVz3_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff20XVz3_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()

process.QWAcc_Noff120Vz3_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff260Vz3_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff400Vz3_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff800Vz3_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff12XVz3_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff20XVz3_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()

process.QWAcc_Noff120Vz3_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff260Vz3_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff400Vz3_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff800Vz3_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff12XVz3_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff20XVz3_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()

process.QWAcc_Noff120Vz3_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff260Vz3_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff400Vz3_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff800Vz3_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff12XVz3_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff20XVz3_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()

process.QWAcc_Noff120Vz3_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff260Vz3_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff400Vz3_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff800Vz3_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff12XVz3_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff20XVz3_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()

process.QWAcc_Noff120Vz3_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff260Vz3_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff400Vz3_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff800Vz3_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff12XVz3_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff20XVz3_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()

process.QWAcc_Noff120Vz3_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff260Vz3_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff400Vz3_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff800Vz3_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff12XVz3_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff20XVz3_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()

process.QWAcc_Noff120Vz3_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff260Vz3_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff400Vz3_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff800Vz3_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff12XVz3_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff20XVz3_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()

process.QWAcc_Noff120Vz3_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff260Vz3_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff400Vz3_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff800Vz3_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff12XVz3_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff20XVz3_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()

process.QWAcc_Noff120Vz3_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff260Vz3_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff400Vz3_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff800Vz3_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff12XVz3_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff20XVz3_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()

process.QWAcc_Noff120Vz3_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff260Vz3_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff400Vz3_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff800Vz3_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff12XVz3_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff20XVz3_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()

process.QWAcc_Noff120Vz3_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff260Vz3_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff400Vz3_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff800Vz3_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff12XVz3_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff20XVz3_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()

process.QWAcc_Noff120Vz3_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff260Vz3_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff400Vz3_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff800Vz3_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff12XVz3_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff20XVz3_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()

process.QWAcc_Noff120Vz3_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff260Vz3_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff400Vz3_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff800Vz3_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff12XVz3_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff20XVz3_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()

process.QWAcc_Noff120Vz3_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff260Vz3_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff400Vz3_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff800Vz3_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff12XVz3_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff20XVz3_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()

process.QWAcc_Noff120Vz3_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff260Vz3_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff400Vz3_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff800Vz3_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff12XVz3_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff20XVz3_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()


# Vz4
process.QWAcc_Noff120Vz4_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff260Vz4_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff400Vz4_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff800Vz4_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff12XVz4_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff20XVz4_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()

process.QWAcc_Noff120Vz4_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff260Vz4_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff400Vz4_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff800Vz4_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff12XVz4_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff20XVz4_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()

process.QWAcc_Noff120Vz4_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff260Vz4_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff400Vz4_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff800Vz4_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff12XVz4_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff20XVz4_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()

process.QWAcc_Noff120Vz4_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff260Vz4_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff400Vz4_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff800Vz4_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff12XVz4_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff20XVz4_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()

process.QWAcc_Noff120Vz4_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff260Vz4_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff400Vz4_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff800Vz4_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff12XVz4_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff20XVz4_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()

process.QWAcc_Noff120Vz4_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff260Vz4_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff400Vz4_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff800Vz4_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff12XVz4_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff20XVz4_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()

process.QWAcc_Noff120Vz4_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff260Vz4_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff400Vz4_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff800Vz4_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff12XVz4_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff20XVz4_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()

process.QWAcc_Noff120Vz4_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff260Vz4_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff400Vz4_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff800Vz4_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff12XVz4_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff20XVz4_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()

process.QWAcc_Noff120Vz4_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff260Vz4_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff400Vz4_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff800Vz4_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff12XVz4_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff20XVz4_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()

process.QWAcc_Noff120Vz4_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff260Vz4_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff400Vz4_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff800Vz4_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff12XVz4_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff20XVz4_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()

process.QWAcc_Noff120Vz4_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff260Vz4_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff400Vz4_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff800Vz4_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff12XVz4_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff20XVz4_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()

process.QWAcc_Noff120Vz4_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff260Vz4_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff400Vz4_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff800Vz4_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff12XVz4_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff20XVz4_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()

process.QWAcc_Noff120Vz4_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff260Vz4_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff400Vz4_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff800Vz4_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff12XVz4_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff20XVz4_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()

process.QWAcc_Noff120Vz4_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff260Vz4_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff400Vz4_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff800Vz4_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff12XVz4_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff20XVz4_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()

process.QWAcc_Noff120Vz4_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff260Vz4_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff400Vz4_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff800Vz4_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff12XVz4_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff20XVz4_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()

process.QWAcc_Noff120Vz4_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff260Vz4_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff400Vz4_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff800Vz4_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff12XVz4_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff20XVz4_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()

process.QWAcc_Noff120Vz4_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff260Vz4_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff400Vz4_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff800Vz4_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff12XVz4_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff20XVz4_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()


# Vz5
process.QWAcc_Noff120Vz5_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff260Vz5_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff400Vz5_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff800Vz5_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff12XVz5_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff20XVz5_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()

process.QWAcc_Noff120Vz5_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff260Vz5_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff400Vz5_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff800Vz5_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff12XVz5_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff20XVz5_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()

process.QWAcc_Noff120Vz5_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff260Vz5_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff400Vz5_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff800Vz5_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff12XVz5_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff20XVz5_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()

process.QWAcc_Noff120Vz5_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff260Vz5_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff400Vz5_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff800Vz5_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff12XVz5_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff20XVz5_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()

process.QWAcc_Noff120Vz5_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff260Vz5_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff400Vz5_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff800Vz5_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff12XVz5_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff20XVz5_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()

process.QWAcc_Noff120Vz5_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff260Vz5_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff400Vz5_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff800Vz5_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff12XVz5_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff20XVz5_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()

process.QWAcc_Noff120Vz5_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff260Vz5_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff400Vz5_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff800Vz5_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff12XVz5_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff20XVz5_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()

process.QWAcc_Noff120Vz5_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff260Vz5_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff400Vz5_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff800Vz5_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff12XVz5_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff20XVz5_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()

process.QWAcc_Noff120Vz5_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff260Vz5_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff400Vz5_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff800Vz5_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff12XVz5_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff20XVz5_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()

process.QWAcc_Noff120Vz5_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff260Vz5_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff400Vz5_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff800Vz5_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff12XVz5_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff20XVz5_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()

process.QWAcc_Noff120Vz5_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff260Vz5_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff400Vz5_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff800Vz5_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff12XVz5_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff20XVz5_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()

process.QWAcc_Noff120Vz5_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff260Vz5_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff400Vz5_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff800Vz5_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff12XVz5_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff20XVz5_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()

process.QWAcc_Noff120Vz5_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff260Vz5_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff400Vz5_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff800Vz5_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff12XVz5_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff20XVz5_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()

process.QWAcc_Noff120Vz5_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff260Vz5_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff400Vz5_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff800Vz5_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff12XVz5_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff20XVz5_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()

process.QWAcc_Noff120Vz5_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff260Vz5_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff400Vz5_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff800Vz5_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff12XVz5_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff20XVz5_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()

process.QWAcc_Noff120Vz5_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff260Vz5_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff400Vz5_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff800Vz5_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff12XVz5_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff20XVz5_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()

process.QWAcc_Noff120Vz5_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff260Vz5_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff400Vz5_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff800Vz5_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff12XVz5_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff20XVz5_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()


# Vz6
process.QWAcc_Noff120Vz6_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff260Vz6_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff400Vz6_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff800Vz6_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff12XVz6_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff20XVz6_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()

process.QWAcc_Noff120Vz6_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff260Vz6_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff400Vz6_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff800Vz6_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff12XVz6_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff20XVz6_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()

process.QWAcc_Noff120Vz6_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff260Vz6_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff400Vz6_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff800Vz6_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff12XVz6_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff20XVz6_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()

process.QWAcc_Noff120Vz6_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff260Vz6_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff400Vz6_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff800Vz6_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff12XVz6_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff20XVz6_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()

process.QWAcc_Noff120Vz6_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff260Vz6_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff400Vz6_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff800Vz6_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff12XVz6_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff20XVz6_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()

process.QWAcc_Noff120Vz6_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff260Vz6_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff400Vz6_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff800Vz6_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff12XVz6_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff20XVz6_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()

process.QWAcc_Noff120Vz6_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff260Vz6_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff400Vz6_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff800Vz6_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff12XVz6_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff20XVz6_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()

process.QWAcc_Noff120Vz6_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff260Vz6_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff400Vz6_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff800Vz6_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff12XVz6_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff20XVz6_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()

process.QWAcc_Noff120Vz6_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff260Vz6_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff400Vz6_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff800Vz6_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff12XVz6_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff20XVz6_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()

process.QWAcc_Noff120Vz6_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff260Vz6_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff400Vz6_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff800Vz6_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff12XVz6_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff20XVz6_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()

process.QWAcc_Noff120Vz6_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff260Vz6_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff400Vz6_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff800Vz6_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff12XVz6_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff20XVz6_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()

process.QWAcc_Noff120Vz6_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff260Vz6_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff400Vz6_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff800Vz6_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff12XVz6_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff20XVz6_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()

process.QWAcc_Noff120Vz6_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff260Vz6_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff400Vz6_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff800Vz6_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff12XVz6_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff20XVz6_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()

process.QWAcc_Noff120Vz6_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff260Vz6_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff400Vz6_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff800Vz6_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff12XVz6_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff20XVz6_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()

process.QWAcc_Noff120Vz6_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff260Vz6_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff400Vz6_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff800Vz6_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff12XVz6_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff20XVz6_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()

process.QWAcc_Noff120Vz6_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff260Vz6_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff400Vz6_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff800Vz6_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff12XVz6_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff20XVz6_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()

process.QWAcc_Noff120Vz6_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff260Vz6_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff400Vz6_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff800Vz6_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff12XVz6_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff20XVz6_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()


# Vz7
process.QWAcc_Noff120Vz7_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff260Vz7_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff400Vz7_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff800Vz7_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff12XVz7_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff20XVz7_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()

process.QWAcc_Noff120Vz7_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff260Vz7_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff400Vz7_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff800Vz7_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff12XVz7_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff20XVz7_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()

process.QWAcc_Noff120Vz7_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff260Vz7_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff400Vz7_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff800Vz7_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff12XVz7_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff20XVz7_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()

process.QWAcc_Noff120Vz7_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff260Vz7_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff400Vz7_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff800Vz7_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff12XVz7_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff20XVz7_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()

process.QWAcc_Noff120Vz7_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff260Vz7_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff400Vz7_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff800Vz7_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff12XVz7_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff20XVz7_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()

process.QWAcc_Noff120Vz7_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff260Vz7_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff400Vz7_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff800Vz7_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff12XVz7_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff20XVz7_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()

process.QWAcc_Noff120Vz7_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff260Vz7_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff400Vz7_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff800Vz7_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff12XVz7_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff20XVz7_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()

process.QWAcc_Noff120Vz7_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff260Vz7_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff400Vz7_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff800Vz7_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff12XVz7_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff20XVz7_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()

process.QWAcc_Noff120Vz7_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff260Vz7_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff400Vz7_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff800Vz7_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff12XVz7_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff20XVz7_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()

process.QWAcc_Noff120Vz7_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff260Vz7_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff400Vz7_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff800Vz7_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff12XVz7_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff20XVz7_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()

process.QWAcc_Noff120Vz7_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff260Vz7_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff400Vz7_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff800Vz7_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff12XVz7_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff20XVz7_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()

process.QWAcc_Noff120Vz7_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff260Vz7_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff400Vz7_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff800Vz7_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff12XVz7_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff20XVz7_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()

process.QWAcc_Noff120Vz7_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff260Vz7_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff400Vz7_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff800Vz7_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff12XVz7_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff20XVz7_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()

process.QWAcc_Noff120Vz7_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff260Vz7_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff400Vz7_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff800Vz7_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff12XVz7_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff20XVz7_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()

process.QWAcc_Noff120Vz7_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff260Vz7_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff400Vz7_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff800Vz7_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff12XVz7_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff20XVz7_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()

process.QWAcc_Noff120Vz7_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff260Vz7_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff400Vz7_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff800Vz7_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff12XVz7_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff20XVz7_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()

process.QWAcc_Noff120Vz7_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff260Vz7_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff400Vz7_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff800Vz7_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff12XVz7_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff20XVz7_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()


# Vz8
process.QWAcc_Noff120Vz8_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff260Vz8_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff400Vz8_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff800Vz8_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff12XVz8_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff20XVz8_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()

process.QWAcc_Noff120Vz8_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff260Vz8_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff400Vz8_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff800Vz8_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff12XVz8_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff20XVz8_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()

process.QWAcc_Noff120Vz8_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff260Vz8_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff400Vz8_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff800Vz8_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff12XVz8_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff20XVz8_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()

process.QWAcc_Noff120Vz8_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff260Vz8_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff400Vz8_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff800Vz8_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff12XVz8_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff20XVz8_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()

process.QWAcc_Noff120Vz8_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff260Vz8_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff400Vz8_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff800Vz8_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff12XVz8_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff20XVz8_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()

process.QWAcc_Noff120Vz8_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff260Vz8_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff400Vz8_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff800Vz8_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff12XVz8_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff20XVz8_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()

process.QWAcc_Noff120Vz8_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff260Vz8_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff400Vz8_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff800Vz8_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff12XVz8_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff20XVz8_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()

process.QWAcc_Noff120Vz8_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff260Vz8_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff400Vz8_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff800Vz8_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff12XVz8_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff20XVz8_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()

process.QWAcc_Noff120Vz8_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff260Vz8_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff400Vz8_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff800Vz8_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff12XVz8_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff20XVz8_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()

process.QWAcc_Noff120Vz8_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff260Vz8_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff400Vz8_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff800Vz8_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff12XVz8_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff20XVz8_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()

process.QWAcc_Noff120Vz8_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff260Vz8_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff400Vz8_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff800Vz8_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff12XVz8_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff20XVz8_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()

process.QWAcc_Noff120Vz8_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff260Vz8_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff400Vz8_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff800Vz8_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff12XVz8_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff20XVz8_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()

process.QWAcc_Noff120Vz8_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff260Vz8_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff400Vz8_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff800Vz8_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff12XVz8_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff20XVz8_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()

process.QWAcc_Noff120Vz8_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff260Vz8_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff400Vz8_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff800Vz8_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff12XVz8_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff20XVz8_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()

process.QWAcc_Noff120Vz8_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff260Vz8_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff400Vz8_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff800Vz8_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff12XVz8_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff20XVz8_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()

process.QWAcc_Noff120Vz8_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff260Vz8_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff400Vz8_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff800Vz8_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff12XVz8_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff20XVz8_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()

process.QWAcc_Noff120Vz8_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff260Vz8_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff400Vz8_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff800Vz8_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff12XVz8_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff20XVz8_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()


# Vz9
process.QWAcc_Noff120Vz9_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff260Vz9_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff400Vz9_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff800Vz9_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff12XVz9_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()
process.QWAcc_Noff20XVz9_pT004 = process.QWAcc_Noff120Vz0_pT004.clone()

process.QWAcc_Noff120Vz9_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff260Vz9_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff400Vz9_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff800Vz9_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff12XVz9_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()
process.QWAcc_Noff20XVz9_pT005 = process.QWAcc_Noff120Vz0_pT005.clone()

process.QWAcc_Noff120Vz9_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff260Vz9_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff400Vz9_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff800Vz9_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff12XVz9_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()
process.QWAcc_Noff20XVz9_pT006 = process.QWAcc_Noff120Vz0_pT006.clone()

process.QWAcc_Noff120Vz9_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff260Vz9_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff400Vz9_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff800Vz9_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff12XVz9_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()
process.QWAcc_Noff20XVz9_pT008 = process.QWAcc_Noff120Vz0_pT008.clone()

process.QWAcc_Noff120Vz9_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff260Vz9_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff400Vz9_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff800Vz9_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff12XVz9_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()
process.QWAcc_Noff20XVz9_pT010 = process.QWAcc_Noff120Vz0_pT010.clone()

process.QWAcc_Noff120Vz9_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff260Vz9_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff400Vz9_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff800Vz9_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff12XVz9_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()
process.QWAcc_Noff20XVz9_pT012 = process.QWAcc_Noff120Vz0_pT012.clone()

process.QWAcc_Noff120Vz9_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff260Vz9_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff400Vz9_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff800Vz9_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff12XVz9_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()
process.QWAcc_Noff20XVz9_pT015 = process.QWAcc_Noff120Vz0_pT015.clone()

process.QWAcc_Noff120Vz9_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff260Vz9_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff400Vz9_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff800Vz9_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff12XVz9_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()
process.QWAcc_Noff20XVz9_pT020 = process.QWAcc_Noff120Vz0_pT020.clone()

process.QWAcc_Noff120Vz9_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff260Vz9_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff400Vz9_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff800Vz9_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff12XVz9_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()
process.QWAcc_Noff20XVz9_pT025 = process.QWAcc_Noff120Vz0_pT025.clone()

process.QWAcc_Noff120Vz9_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff260Vz9_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff400Vz9_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff800Vz9_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff12XVz9_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()
process.QWAcc_Noff20XVz9_pT030 = process.QWAcc_Noff120Vz0_pT030.clone()

process.QWAcc_Noff120Vz9_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff260Vz9_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff400Vz9_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff800Vz9_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff12XVz9_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()
process.QWAcc_Noff20XVz9_pT035 = process.QWAcc_Noff120Vz0_pT035.clone()

process.QWAcc_Noff120Vz9_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff260Vz9_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff400Vz9_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff800Vz9_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff12XVz9_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()
process.QWAcc_Noff20XVz9_pT040 = process.QWAcc_Noff120Vz0_pT040.clone()

process.QWAcc_Noff120Vz9_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff260Vz9_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff400Vz9_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff800Vz9_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff12XVz9_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()
process.QWAcc_Noff20XVz9_pT050 = process.QWAcc_Noff120Vz0_pT050.clone()

process.QWAcc_Noff120Vz9_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff260Vz9_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff400Vz9_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff800Vz9_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff12XVz9_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()
process.QWAcc_Noff20XVz9_pT060 = process.QWAcc_Noff120Vz0_pT060.clone()

process.QWAcc_Noff120Vz9_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff260Vz9_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff400Vz9_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff800Vz9_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff12XVz9_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()
process.QWAcc_Noff20XVz9_pT070 = process.QWAcc_Noff120Vz0_pT070.clone()

process.QWAcc_Noff120Vz9_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff260Vz9_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff400Vz9_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff800Vz9_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff12XVz9_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()
process.QWAcc_Noff20XVz9_pT080 = process.QWAcc_Noff120Vz0_pT080.clone()

process.QWAcc_Noff120Vz9_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff260Vz9_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff400Vz9_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff800Vz9_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff12XVz9_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()
process.QWAcc_Noff20XVz9_pT100 = process.QWAcc_Noff120Vz0_pT100.clone()






process.load('PbPb_HIMB5_ppReco_eff')
process.QWEvent.fweight = cms.untracked.InputTag('Hydjet_PbPb_eff_v1.root')


process.pre_ana = cms.Sequence(process.eventSelection * process.makeEvent * process.ppRecoCentFilter * process.PrimaryVz)

# Vz0
process.pre_ana120Vz0 = cms.Sequence(process.pre_ana * process.NoffFilter120 * process.VzFilter0)
process.pre_ana260Vz0 = cms.Sequence(process.pre_ana * process.NoffFilter260 * process.VzFilter0)
process.pre_ana400Vz0 = cms.Sequence(process.pre_ana * process.NoffFilter400 * process.VzFilter0)
process.pre_ana800Vz0 = cms.Sequence(process.pre_ana * process.NoffFilter800 * process.VzFilter0)
process.pre_ana12XVz0 = cms.Sequence(process.pre_ana * process.NoffFilter1200* process.VzFilter0)
process.pre_ana20XVz0 = cms.Sequence(process.pre_ana * process.NoffFilter2000* process.VzFilter0)

# Vz1
process.pre_ana120Vz1 = cms.Sequence(process.pre_ana * process.NoffFilter120 * process.VzFilter1)
process.pre_ana260Vz1 = cms.Sequence(process.pre_ana * process.NoffFilter260 * process.VzFilter1)
process.pre_ana400Vz1 = cms.Sequence(process.pre_ana * process.NoffFilter400 * process.VzFilter1)
process.pre_ana800Vz1 = cms.Sequence(process.pre_ana * process.NoffFilter800 * process.VzFilter1)
process.pre_ana12XVz1 = cms.Sequence(process.pre_ana * process.NoffFilter1200* process.VzFilter1)
process.pre_ana20XVz1 = cms.Sequence(process.pre_ana * process.NoffFilter2000* process.VzFilter1)

# Vz2
process.pre_ana120Vz2 = cms.Sequence(process.pre_ana * process.NoffFilter120 * process.VzFilter2)
process.pre_ana260Vz2 = cms.Sequence(process.pre_ana * process.NoffFilter260 * process.VzFilter2)
process.pre_ana400Vz2 = cms.Sequence(process.pre_ana * process.NoffFilter400 * process.VzFilter2)
process.pre_ana800Vz2 = cms.Sequence(process.pre_ana * process.NoffFilter800 * process.VzFilter2)
process.pre_ana12XVz2 = cms.Sequence(process.pre_ana * process.NoffFilter1200* process.VzFilter2)
process.pre_ana20XVz2 = cms.Sequence(process.pre_ana * process.NoffFilter2000* process.VzFilter2)


# Vz3
process.pre_ana120Vz3 = cms.Sequence(process.pre_ana * process.NoffFilter120 * process.VzFilter3)
process.pre_ana260Vz3 = cms.Sequence(process.pre_ana * process.NoffFilter260 * process.VzFilter3)
process.pre_ana400Vz3 = cms.Sequence(process.pre_ana * process.NoffFilter400 * process.VzFilter3)
process.pre_ana800Vz3 = cms.Sequence(process.pre_ana * process.NoffFilter800 * process.VzFilter3)
process.pre_ana12XVz3 = cms.Sequence(process.pre_ana * process.NoffFilter1200* process.VzFilter3)
process.pre_ana20XVz3 = cms.Sequence(process.pre_ana * process.NoffFilter2000* process.VzFilter3)


# Vz4
process.pre_ana120Vz4 = cms.Sequence(process.pre_ana * process.NoffFilter120 * process.VzFilter4)
process.pre_ana260Vz4 = cms.Sequence(process.pre_ana * process.NoffFilter260 * process.VzFilter4)
process.pre_ana400Vz4 = cms.Sequence(process.pre_ana * process.NoffFilter400 * process.VzFilter4)
process.pre_ana800Vz4 = cms.Sequence(process.pre_ana * process.NoffFilter800 * process.VzFilter4)
process.pre_ana12XVz4 = cms.Sequence(process.pre_ana * process.NoffFilter1200* process.VzFilter4)
process.pre_ana20XVz4 = cms.Sequence(process.pre_ana * process.NoffFilter2000* process.VzFilter4)


# Vz5
process.pre_ana120Vz5 = cms.Sequence(process.pre_ana * process.NoffFilter120 * process.VzFilter5)
process.pre_ana260Vz5 = cms.Sequence(process.pre_ana * process.NoffFilter260 * process.VzFilter5)
process.pre_ana400Vz5 = cms.Sequence(process.pre_ana * process.NoffFilter400 * process.VzFilter5)
process.pre_ana800Vz5 = cms.Sequence(process.pre_ana * process.NoffFilter800 * process.VzFilter5)
process.pre_ana12XVz5 = cms.Sequence(process.pre_ana * process.NoffFilter1200* process.VzFilter5)
process.pre_ana20XVz5 = cms.Sequence(process.pre_ana * process.NoffFilter2000* process.VzFilter5)

# Vz6
process.pre_ana120Vz6 = cms.Sequence(process.pre_ana * process.NoffFilter120 * process.VzFilter6)
process.pre_ana260Vz6 = cms.Sequence(process.pre_ana * process.NoffFilter260 * process.VzFilter6)
process.pre_ana400Vz6 = cms.Sequence(process.pre_ana * process.NoffFilter400 * process.VzFilter6)
process.pre_ana800Vz6 = cms.Sequence(process.pre_ana * process.NoffFilter800 * process.VzFilter6)
process.pre_ana12XVz6 = cms.Sequence(process.pre_ana * process.NoffFilter1200* process.VzFilter6)
process.pre_ana20XVz6 = cms.Sequence(process.pre_ana * process.NoffFilter2000* process.VzFilter6)


# Vz7
process.pre_ana120Vz7 = cms.Sequence(process.pre_ana * process.NoffFilter120 * process.VzFilter7)
process.pre_ana260Vz7 = cms.Sequence(process.pre_ana * process.NoffFilter260 * process.VzFilter7)
process.pre_ana400Vz7 = cms.Sequence(process.pre_ana * process.NoffFilter400 * process.VzFilter7)
process.pre_ana800Vz7 = cms.Sequence(process.pre_ana * process.NoffFilter800 * process.VzFilter7)
process.pre_ana12XVz7 = cms.Sequence(process.pre_ana * process.NoffFilter1200* process.VzFilter7)
process.pre_ana20XVz7 = cms.Sequence(process.pre_ana * process.NoffFilter2000* process.VzFilter7)

# Vz8
process.pre_ana120Vz8 = cms.Sequence(process.pre_ana * process.NoffFilter120 * process.VzFilter8)
process.pre_ana260Vz8 = cms.Sequence(process.pre_ana * process.NoffFilter260 * process.VzFilter8)
process.pre_ana400Vz8 = cms.Sequence(process.pre_ana * process.NoffFilter400 * process.VzFilter8)
process.pre_ana800Vz8 = cms.Sequence(process.pre_ana * process.NoffFilter800 * process.VzFilter8)
process.pre_ana12XVz8 = cms.Sequence(process.pre_ana * process.NoffFilter1200* process.VzFilter8)
process.pre_ana20XVz8 = cms.Sequence(process.pre_ana * process.NoffFilter2000* process.VzFilter8)


# Vz9
process.pre_ana120Vz9 = cms.Sequence(process.pre_ana * process.NoffFilter120 * process.VzFilter9)
process.pre_ana260Vz9 = cms.Sequence(process.pre_ana * process.NoffFilter260 * process.VzFilter9)
process.pre_ana400Vz9 = cms.Sequence(process.pre_ana * process.NoffFilter400 * process.VzFilter9)
process.pre_ana800Vz9 = cms.Sequence(process.pre_ana * process.NoffFilter800 * process.VzFilter9)
process.pre_ana12XVz9 = cms.Sequence(process.pre_ana * process.NoffFilter1200* process.VzFilter9)
process.pre_ana20XVz9 = cms.Sequence(process.pre_ana * process.NoffFilter2000* process.VzFilter9)


## Vz0
process.ana120Vz0 = cms.Path(
		process.pre_ana120Vz0 *
		process.QWAcc_Noff120Vz0_pT004 *
		process.QWAcc_Noff120Vz0_pT005 *
		process.QWAcc_Noff120Vz0_pT006 *
		process.QWAcc_Noff120Vz0_pT008 *
		process.QWAcc_Noff120Vz0_pT010 *
		process.QWAcc_Noff120Vz0_pT012 *
		process.QWAcc_Noff120Vz0_pT015 *
		process.QWAcc_Noff120Vz0_pT020 *
		process.QWAcc_Noff120Vz0_pT025 *
		process.QWAcc_Noff120Vz0_pT030 *
		process.QWAcc_Noff120Vz0_pT035 *
		process.QWAcc_Noff120Vz0_pT040 *
		process.QWAcc_Noff120Vz0_pT050 *
		process.QWAcc_Noff120Vz0_pT060 *
		process.QWAcc_Noff120Vz0_pT070 *
		process.QWAcc_Noff120Vz0_pT080 *
		process.QWAcc_Noff120Vz0_pT100
		)

process.ana260Vz0 = cms.Path(
		process.pre_ana260Vz0 *
		process.QWAcc_Noff260Vz0_pT004 *
		process.QWAcc_Noff260Vz0_pT005 *
		process.QWAcc_Noff260Vz0_pT006 *
		process.QWAcc_Noff260Vz0_pT008 *
		process.QWAcc_Noff260Vz0_pT010 *
		process.QWAcc_Noff260Vz0_pT012 *
		process.QWAcc_Noff260Vz0_pT015 *
		process.QWAcc_Noff260Vz0_pT020 *
		process.QWAcc_Noff260Vz0_pT025 *
		process.QWAcc_Noff260Vz0_pT030 *
		process.QWAcc_Noff260Vz0_pT035 *
		process.QWAcc_Noff260Vz0_pT040 *
		process.QWAcc_Noff260Vz0_pT050 *
		process.QWAcc_Noff260Vz0_pT060 *
		process.QWAcc_Noff260Vz0_pT070 *
		process.QWAcc_Noff260Vz0_pT080 *
		process.QWAcc_Noff260Vz0_pT100
		)

process.ana400Vz0 = cms.Path(
		process.pre_ana400Vz0 *
		process.QWAcc_Noff400Vz0_pT004 *
		process.QWAcc_Noff400Vz0_pT005 *
		process.QWAcc_Noff400Vz0_pT006 *
		process.QWAcc_Noff400Vz0_pT008 *
		process.QWAcc_Noff400Vz0_pT010 *
		process.QWAcc_Noff400Vz0_pT012 *
		process.QWAcc_Noff400Vz0_pT015 *
		process.QWAcc_Noff400Vz0_pT020 *
		process.QWAcc_Noff400Vz0_pT025 *
		process.QWAcc_Noff400Vz0_pT030 *
		process.QWAcc_Noff400Vz0_pT035 *
		process.QWAcc_Noff400Vz0_pT040 *
		process.QWAcc_Noff400Vz0_pT050 *
		process.QWAcc_Noff400Vz0_pT060 *
		process.QWAcc_Noff400Vz0_pT070 *
		process.QWAcc_Noff400Vz0_pT080 *
		process.QWAcc_Noff400Vz0_pT100
		)

process.ana800Vz0 = cms.Path(
		process.pre_ana800Vz0 *
		process.QWAcc_Noff800Vz0_pT004 *
		process.QWAcc_Noff800Vz0_pT005 *
		process.QWAcc_Noff800Vz0_pT006 *
		process.QWAcc_Noff800Vz0_pT008 *
		process.QWAcc_Noff800Vz0_pT010 *
		process.QWAcc_Noff800Vz0_pT012 *
		process.QWAcc_Noff800Vz0_pT015 *
		process.QWAcc_Noff800Vz0_pT020 *
		process.QWAcc_Noff800Vz0_pT025 *
		process.QWAcc_Noff800Vz0_pT030 *
		process.QWAcc_Noff800Vz0_pT035 *
		process.QWAcc_Noff800Vz0_pT040 *
		process.QWAcc_Noff800Vz0_pT050 *
		process.QWAcc_Noff800Vz0_pT060 *
		process.QWAcc_Noff800Vz0_pT070 *
		process.QWAcc_Noff800Vz0_pT080 *
		process.QWAcc_Noff800Vz0_pT100
		)

process.ana12XVz0 = cms.Path(
		process.pre_ana12XVz0 *
		process.QWAcc_Noff12XVz0_pT004 *
		process.QWAcc_Noff12XVz0_pT005 *
		process.QWAcc_Noff12XVz0_pT006 *
		process.QWAcc_Noff12XVz0_pT008 *
		process.QWAcc_Noff12XVz0_pT010 *
		process.QWAcc_Noff12XVz0_pT012 *
		process.QWAcc_Noff12XVz0_pT015 *
		process.QWAcc_Noff12XVz0_pT020 *
		process.QWAcc_Noff12XVz0_pT025 *
		process.QWAcc_Noff12XVz0_pT030 *
		process.QWAcc_Noff12XVz0_pT035 *
		process.QWAcc_Noff12XVz0_pT040 *
		process.QWAcc_Noff12XVz0_pT050 *
		process.QWAcc_Noff12XVz0_pT060 *
		process.QWAcc_Noff12XVz0_pT070 *
		process.QWAcc_Noff12XVz0_pT080 *
		process.QWAcc_Noff12XVz0_pT100
		)

process.ana20XVz0 = cms.Path(
		process.pre_ana20XVz0 *
		process.QWAcc_Noff20XVz0_pT004 *
		process.QWAcc_Noff20XVz0_pT005 *
		process.QWAcc_Noff20XVz0_pT006 *
		process.QWAcc_Noff20XVz0_pT008 *
		process.QWAcc_Noff20XVz0_pT010 *
		process.QWAcc_Noff20XVz0_pT012 *
		process.QWAcc_Noff20XVz0_pT015 *
		process.QWAcc_Noff20XVz0_pT020 *
		process.QWAcc_Noff20XVz0_pT025 *
		process.QWAcc_Noff20XVz0_pT030 *
		process.QWAcc_Noff20XVz0_pT035 *
		process.QWAcc_Noff20XVz0_pT040 *
		process.QWAcc_Noff20XVz0_pT050 *
		process.QWAcc_Noff20XVz0_pT060 *
		process.QWAcc_Noff20XVz0_pT070 *
		process.QWAcc_Noff20XVz0_pT080 *
		process.QWAcc_Noff20XVz0_pT100
		)


## Vz1
process.ana120Vz1 = cms.Path(
		process.pre_ana120Vz1 *
		process.QWAcc_Noff120Vz1_pT004 *
		process.QWAcc_Noff120Vz1_pT005 *
		process.QWAcc_Noff120Vz1_pT006 *
		process.QWAcc_Noff120Vz1_pT008 *
		process.QWAcc_Noff120Vz1_pT010 *
		process.QWAcc_Noff120Vz1_pT012 *
		process.QWAcc_Noff120Vz1_pT015 *
		process.QWAcc_Noff120Vz1_pT020 *
		process.QWAcc_Noff120Vz1_pT025 *
		process.QWAcc_Noff120Vz1_pT030 *
		process.QWAcc_Noff120Vz1_pT035 *
		process.QWAcc_Noff120Vz1_pT040 *
		process.QWAcc_Noff120Vz1_pT050 *
		process.QWAcc_Noff120Vz1_pT060 *
		process.QWAcc_Noff120Vz1_pT070 *
		process.QWAcc_Noff120Vz1_pT080 *
		process.QWAcc_Noff120Vz1_pT100
		)

process.ana260Vz1 = cms.Path(
		process.pre_ana260Vz1 *
		process.QWAcc_Noff260Vz1_pT004 *
		process.QWAcc_Noff260Vz1_pT005 *
		process.QWAcc_Noff260Vz1_pT006 *
		process.QWAcc_Noff260Vz1_pT008 *
		process.QWAcc_Noff260Vz1_pT010 *
		process.QWAcc_Noff260Vz1_pT012 *
		process.QWAcc_Noff260Vz1_pT015 *
		process.QWAcc_Noff260Vz1_pT020 *
		process.QWAcc_Noff260Vz1_pT025 *
		process.QWAcc_Noff260Vz1_pT030 *
		process.QWAcc_Noff260Vz1_pT035 *
		process.QWAcc_Noff260Vz1_pT040 *
		process.QWAcc_Noff260Vz1_pT050 *
		process.QWAcc_Noff260Vz1_pT060 *
		process.QWAcc_Noff260Vz1_pT070 *
		process.QWAcc_Noff260Vz1_pT080 *
		process.QWAcc_Noff260Vz1_pT100
		)

process.ana400Vz1 = cms.Path(
		process.pre_ana400Vz1 *
		process.QWAcc_Noff400Vz1_pT004 *
		process.QWAcc_Noff400Vz1_pT005 *
		process.QWAcc_Noff400Vz1_pT006 *
		process.QWAcc_Noff400Vz1_pT008 *
		process.QWAcc_Noff400Vz1_pT010 *
		process.QWAcc_Noff400Vz1_pT012 *
		process.QWAcc_Noff400Vz1_pT015 *
		process.QWAcc_Noff400Vz1_pT020 *
		process.QWAcc_Noff400Vz1_pT025 *
		process.QWAcc_Noff400Vz1_pT030 *
		process.QWAcc_Noff400Vz1_pT035 *
		process.QWAcc_Noff400Vz1_pT040 *
		process.QWAcc_Noff400Vz1_pT050 *
		process.QWAcc_Noff400Vz1_pT060 *
		process.QWAcc_Noff400Vz1_pT070 *
		process.QWAcc_Noff400Vz1_pT080 *
		process.QWAcc_Noff400Vz1_pT100
		)

process.ana800Vz1 = cms.Path(
		process.pre_ana800Vz1 *
		process.QWAcc_Noff800Vz1_pT004 *
		process.QWAcc_Noff800Vz1_pT005 *
		process.QWAcc_Noff800Vz1_pT006 *
		process.QWAcc_Noff800Vz1_pT008 *
		process.QWAcc_Noff800Vz1_pT010 *
		process.QWAcc_Noff800Vz1_pT012 *
		process.QWAcc_Noff800Vz1_pT015 *
		process.QWAcc_Noff800Vz1_pT020 *
		process.QWAcc_Noff800Vz1_pT025 *
		process.QWAcc_Noff800Vz1_pT030 *
		process.QWAcc_Noff800Vz1_pT035 *
		process.QWAcc_Noff800Vz1_pT040 *
		process.QWAcc_Noff800Vz1_pT050 *
		process.QWAcc_Noff800Vz1_pT060 *
		process.QWAcc_Noff800Vz1_pT070 *
		process.QWAcc_Noff800Vz1_pT080 *
		process.QWAcc_Noff800Vz1_pT100
		)

process.ana12XVz1 = cms.Path(
		process.pre_ana12XVz1 *
		process.QWAcc_Noff12XVz1_pT004 *
		process.QWAcc_Noff12XVz1_pT005 *
		process.QWAcc_Noff12XVz1_pT006 *
		process.QWAcc_Noff12XVz1_pT008 *
		process.QWAcc_Noff12XVz1_pT010 *
		process.QWAcc_Noff12XVz1_pT012 *
		process.QWAcc_Noff12XVz1_pT015 *
		process.QWAcc_Noff12XVz1_pT020 *
		process.QWAcc_Noff12XVz1_pT025 *
		process.QWAcc_Noff12XVz1_pT030 *
		process.QWAcc_Noff12XVz1_pT035 *
		process.QWAcc_Noff12XVz1_pT040 *
		process.QWAcc_Noff12XVz1_pT050 *
		process.QWAcc_Noff12XVz1_pT060 *
		process.QWAcc_Noff12XVz1_pT070 *
		process.QWAcc_Noff12XVz1_pT080 *
		process.QWAcc_Noff12XVz1_pT100
		)

process.ana20XVz1 = cms.Path(
		process.pre_ana20XVz1 *
		process.QWAcc_Noff20XVz1_pT004 *
		process.QWAcc_Noff20XVz1_pT005 *
		process.QWAcc_Noff20XVz1_pT006 *
		process.QWAcc_Noff20XVz1_pT008 *
		process.QWAcc_Noff20XVz1_pT010 *
		process.QWAcc_Noff20XVz1_pT012 *
		process.QWAcc_Noff20XVz1_pT015 *
		process.QWAcc_Noff20XVz1_pT020 *
		process.QWAcc_Noff20XVz1_pT025 *
		process.QWAcc_Noff20XVz1_pT030 *
		process.QWAcc_Noff20XVz1_pT035 *
		process.QWAcc_Noff20XVz1_pT040 *
		process.QWAcc_Noff20XVz1_pT050 *
		process.QWAcc_Noff20XVz1_pT060 *
		process.QWAcc_Noff20XVz1_pT070 *
		process.QWAcc_Noff20XVz1_pT080 *
		process.QWAcc_Noff20XVz1_pT100
		)


## Vz2
process.ana120Vz2 = cms.Path(
		process.pre_ana120Vz2 *
		process.QWAcc_Noff120Vz2_pT004 *
		process.QWAcc_Noff120Vz2_pT005 *
		process.QWAcc_Noff120Vz2_pT006 *
		process.QWAcc_Noff120Vz2_pT008 *
		process.QWAcc_Noff120Vz2_pT010 *
		process.QWAcc_Noff120Vz2_pT012 *
		process.QWAcc_Noff120Vz2_pT015 *
		process.QWAcc_Noff120Vz2_pT020 *
		process.QWAcc_Noff120Vz2_pT025 *
		process.QWAcc_Noff120Vz2_pT030 *
		process.QWAcc_Noff120Vz2_pT035 *
		process.QWAcc_Noff120Vz2_pT040 *
		process.QWAcc_Noff120Vz2_pT050 *
		process.QWAcc_Noff120Vz2_pT060 *
		process.QWAcc_Noff120Vz2_pT070 *
		process.QWAcc_Noff120Vz2_pT080 *
		process.QWAcc_Noff120Vz2_pT100
		)

process.ana260Vz2 = cms.Path(
		process.pre_ana260Vz2 *
		process.QWAcc_Noff260Vz2_pT004 *
		process.QWAcc_Noff260Vz2_pT005 *
		process.QWAcc_Noff260Vz2_pT006 *
		process.QWAcc_Noff260Vz2_pT008 *
		process.QWAcc_Noff260Vz2_pT010 *
		process.QWAcc_Noff260Vz2_pT012 *
		process.QWAcc_Noff260Vz2_pT015 *
		process.QWAcc_Noff260Vz2_pT020 *
		process.QWAcc_Noff260Vz2_pT025 *
		process.QWAcc_Noff260Vz2_pT030 *
		process.QWAcc_Noff260Vz2_pT035 *
		process.QWAcc_Noff260Vz2_pT040 *
		process.QWAcc_Noff260Vz2_pT050 *
		process.QWAcc_Noff260Vz2_pT060 *
		process.QWAcc_Noff260Vz2_pT070 *
		process.QWAcc_Noff260Vz2_pT080 *
		process.QWAcc_Noff260Vz2_pT100
		)

process.ana400Vz2 = cms.Path(
		process.pre_ana400Vz2 *
		process.QWAcc_Noff400Vz2_pT004 *
		process.QWAcc_Noff400Vz2_pT005 *
		process.QWAcc_Noff400Vz2_pT006 *
		process.QWAcc_Noff400Vz2_pT008 *
		process.QWAcc_Noff400Vz2_pT010 *
		process.QWAcc_Noff400Vz2_pT012 *
		process.QWAcc_Noff400Vz2_pT015 *
		process.QWAcc_Noff400Vz2_pT020 *
		process.QWAcc_Noff400Vz2_pT025 *
		process.QWAcc_Noff400Vz2_pT030 *
		process.QWAcc_Noff400Vz2_pT035 *
		process.QWAcc_Noff400Vz2_pT040 *
		process.QWAcc_Noff400Vz2_pT050 *
		process.QWAcc_Noff400Vz2_pT060 *
		process.QWAcc_Noff400Vz2_pT070 *
		process.QWAcc_Noff400Vz2_pT080 *
		process.QWAcc_Noff400Vz2_pT100
		)

process.ana800Vz2 = cms.Path(
		process.pre_ana800Vz2 *
		process.QWAcc_Noff800Vz2_pT004 *
		process.QWAcc_Noff800Vz2_pT005 *
		process.QWAcc_Noff800Vz2_pT006 *
		process.QWAcc_Noff800Vz2_pT008 *
		process.QWAcc_Noff800Vz2_pT010 *
		process.QWAcc_Noff800Vz2_pT012 *
		process.QWAcc_Noff800Vz2_pT015 *
		process.QWAcc_Noff800Vz2_pT020 *
		process.QWAcc_Noff800Vz2_pT025 *
		process.QWAcc_Noff800Vz2_pT030 *
		process.QWAcc_Noff800Vz2_pT035 *
		process.QWAcc_Noff800Vz2_pT040 *
		process.QWAcc_Noff800Vz2_pT050 *
		process.QWAcc_Noff800Vz2_pT060 *
		process.QWAcc_Noff800Vz2_pT070 *
		process.QWAcc_Noff800Vz2_pT080 *
		process.QWAcc_Noff800Vz2_pT100
		)

process.ana12XVz2 = cms.Path(
		process.pre_ana12XVz2 *
		process.QWAcc_Noff12XVz2_pT004 *
		process.QWAcc_Noff12XVz2_pT005 *
		process.QWAcc_Noff12XVz2_pT006 *
		process.QWAcc_Noff12XVz2_pT008 *
		process.QWAcc_Noff12XVz2_pT010 *
		process.QWAcc_Noff12XVz2_pT012 *
		process.QWAcc_Noff12XVz2_pT015 *
		process.QWAcc_Noff12XVz2_pT020 *
		process.QWAcc_Noff12XVz2_pT025 *
		process.QWAcc_Noff12XVz2_pT030 *
		process.QWAcc_Noff12XVz2_pT035 *
		process.QWAcc_Noff12XVz2_pT040 *
		process.QWAcc_Noff12XVz2_pT050 *
		process.QWAcc_Noff12XVz2_pT060 *
		process.QWAcc_Noff12XVz2_pT070 *
		process.QWAcc_Noff12XVz2_pT080 *
		process.QWAcc_Noff12XVz2_pT100
		)

process.ana20XVz2 = cms.Path(
		process.pre_ana20XVz2 *
		process.QWAcc_Noff20XVz2_pT004 *
		process.QWAcc_Noff20XVz2_pT005 *
		process.QWAcc_Noff20XVz2_pT006 *
		process.QWAcc_Noff20XVz2_pT008 *
		process.QWAcc_Noff20XVz2_pT010 *
		process.QWAcc_Noff20XVz2_pT012 *
		process.QWAcc_Noff20XVz2_pT015 *
		process.QWAcc_Noff20XVz2_pT020 *
		process.QWAcc_Noff20XVz2_pT025 *
		process.QWAcc_Noff20XVz2_pT030 *
		process.QWAcc_Noff20XVz2_pT035 *
		process.QWAcc_Noff20XVz2_pT040 *
		process.QWAcc_Noff20XVz2_pT050 *
		process.QWAcc_Noff20XVz2_pT060 *
		process.QWAcc_Noff20XVz2_pT070 *
		process.QWAcc_Noff20XVz2_pT080 *
		process.QWAcc_Noff20XVz2_pT100
		)


## Vz3
process.ana120Vz3 = cms.Path(
		process.pre_ana120Vz3 *
		process.QWAcc_Noff120Vz3_pT004 *
		process.QWAcc_Noff120Vz3_pT005 *
		process.QWAcc_Noff120Vz3_pT006 *
		process.QWAcc_Noff120Vz3_pT008 *
		process.QWAcc_Noff120Vz3_pT010 *
		process.QWAcc_Noff120Vz3_pT012 *
		process.QWAcc_Noff120Vz3_pT015 *
		process.QWAcc_Noff120Vz3_pT020 *
		process.QWAcc_Noff120Vz3_pT025 *
		process.QWAcc_Noff120Vz3_pT030 *
		process.QWAcc_Noff120Vz3_pT035 *
		process.QWAcc_Noff120Vz3_pT040 *
		process.QWAcc_Noff120Vz3_pT050 *
		process.QWAcc_Noff120Vz3_pT060 *
		process.QWAcc_Noff120Vz3_pT070 *
		process.QWAcc_Noff120Vz3_pT080 *
		process.QWAcc_Noff120Vz3_pT100
		)

process.ana260Vz3 = cms.Path(
		process.pre_ana260Vz3 *
		process.QWAcc_Noff260Vz3_pT004 *
		process.QWAcc_Noff260Vz3_pT005 *
		process.QWAcc_Noff260Vz3_pT006 *
		process.QWAcc_Noff260Vz3_pT008 *
		process.QWAcc_Noff260Vz3_pT010 *
		process.QWAcc_Noff260Vz3_pT012 *
		process.QWAcc_Noff260Vz3_pT015 *
		process.QWAcc_Noff260Vz3_pT020 *
		process.QWAcc_Noff260Vz3_pT025 *
		process.QWAcc_Noff260Vz3_pT030 *
		process.QWAcc_Noff260Vz3_pT035 *
		process.QWAcc_Noff260Vz3_pT040 *
		process.QWAcc_Noff260Vz3_pT050 *
		process.QWAcc_Noff260Vz3_pT060 *
		process.QWAcc_Noff260Vz3_pT070 *
		process.QWAcc_Noff260Vz3_pT080 *
		process.QWAcc_Noff260Vz3_pT100
		)

process.ana400Vz3 = cms.Path(
		process.pre_ana400Vz3 *
		process.QWAcc_Noff400Vz3_pT004 *
		process.QWAcc_Noff400Vz3_pT005 *
		process.QWAcc_Noff400Vz3_pT006 *
		process.QWAcc_Noff400Vz3_pT008 *
		process.QWAcc_Noff400Vz3_pT010 *
		process.QWAcc_Noff400Vz3_pT012 *
		process.QWAcc_Noff400Vz3_pT015 *
		process.QWAcc_Noff400Vz3_pT020 *
		process.QWAcc_Noff400Vz3_pT025 *
		process.QWAcc_Noff400Vz3_pT030 *
		process.QWAcc_Noff400Vz3_pT035 *
		process.QWAcc_Noff400Vz3_pT040 *
		process.QWAcc_Noff400Vz3_pT050 *
		process.QWAcc_Noff400Vz3_pT060 *
		process.QWAcc_Noff400Vz3_pT070 *
		process.QWAcc_Noff400Vz3_pT080 *
		process.QWAcc_Noff400Vz3_pT100
		)

process.ana800Vz3 = cms.Path(
		process.pre_ana800Vz3 *
		process.QWAcc_Noff800Vz3_pT004 *
		process.QWAcc_Noff800Vz3_pT005 *
		process.QWAcc_Noff800Vz3_pT006 *
		process.QWAcc_Noff800Vz3_pT008 *
		process.QWAcc_Noff800Vz3_pT010 *
		process.QWAcc_Noff800Vz3_pT012 *
		process.QWAcc_Noff800Vz3_pT015 *
		process.QWAcc_Noff800Vz3_pT020 *
		process.QWAcc_Noff800Vz3_pT025 *
		process.QWAcc_Noff800Vz3_pT030 *
		process.QWAcc_Noff800Vz3_pT035 *
		process.QWAcc_Noff800Vz3_pT040 *
		process.QWAcc_Noff800Vz3_pT050 *
		process.QWAcc_Noff800Vz3_pT060 *
		process.QWAcc_Noff800Vz3_pT070 *
		process.QWAcc_Noff800Vz3_pT080 *
		process.QWAcc_Noff800Vz3_pT100
		)

process.ana12XVz3 = cms.Path(
		process.pre_ana12XVz3 *
		process.QWAcc_Noff12XVz3_pT004 *
		process.QWAcc_Noff12XVz3_pT005 *
		process.QWAcc_Noff12XVz3_pT006 *
		process.QWAcc_Noff12XVz3_pT008 *
		process.QWAcc_Noff12XVz3_pT010 *
		process.QWAcc_Noff12XVz3_pT012 *
		process.QWAcc_Noff12XVz3_pT015 *
		process.QWAcc_Noff12XVz3_pT020 *
		process.QWAcc_Noff12XVz3_pT025 *
		process.QWAcc_Noff12XVz3_pT030 *
		process.QWAcc_Noff12XVz3_pT035 *
		process.QWAcc_Noff12XVz3_pT040 *
		process.QWAcc_Noff12XVz3_pT050 *
		process.QWAcc_Noff12XVz3_pT060 *
		process.QWAcc_Noff12XVz3_pT070 *
		process.QWAcc_Noff12XVz3_pT080 *
		process.QWAcc_Noff12XVz3_pT100
		)

process.ana20XVz3 = cms.Path(
		process.pre_ana20XVz3 *
		process.QWAcc_Noff20XVz3_pT004 *
		process.QWAcc_Noff20XVz3_pT005 *
		process.QWAcc_Noff20XVz3_pT006 *
		process.QWAcc_Noff20XVz3_pT008 *
		process.QWAcc_Noff20XVz3_pT010 *
		process.QWAcc_Noff20XVz3_pT012 *
		process.QWAcc_Noff20XVz3_pT015 *
		process.QWAcc_Noff20XVz3_pT020 *
		process.QWAcc_Noff20XVz3_pT025 *
		process.QWAcc_Noff20XVz3_pT030 *
		process.QWAcc_Noff20XVz3_pT035 *
		process.QWAcc_Noff20XVz3_pT040 *
		process.QWAcc_Noff20XVz3_pT050 *
		process.QWAcc_Noff20XVz3_pT060 *
		process.QWAcc_Noff20XVz3_pT070 *
		process.QWAcc_Noff20XVz3_pT080 *
		process.QWAcc_Noff20XVz3_pT100
		)


## Vz4
process.ana120Vz4 = cms.Path(
		process.pre_ana120Vz4 *
		process.QWAcc_Noff120Vz4_pT004 *
		process.QWAcc_Noff120Vz4_pT005 *
		process.QWAcc_Noff120Vz4_pT006 *
		process.QWAcc_Noff120Vz4_pT008 *
		process.QWAcc_Noff120Vz4_pT010 *
		process.QWAcc_Noff120Vz4_pT012 *
		process.QWAcc_Noff120Vz4_pT015 *
		process.QWAcc_Noff120Vz4_pT020 *
		process.QWAcc_Noff120Vz4_pT025 *
		process.QWAcc_Noff120Vz4_pT030 *
		process.QWAcc_Noff120Vz4_pT035 *
		process.QWAcc_Noff120Vz4_pT040 *
		process.QWAcc_Noff120Vz4_pT050 *
		process.QWAcc_Noff120Vz4_pT060 *
		process.QWAcc_Noff120Vz4_pT070 *
		process.QWAcc_Noff120Vz4_pT080 *
		process.QWAcc_Noff120Vz4_pT100
		)

process.ana260Vz4 = cms.Path(
		process.pre_ana260Vz4 *
		process.QWAcc_Noff260Vz4_pT004 *
		process.QWAcc_Noff260Vz4_pT005 *
		process.QWAcc_Noff260Vz4_pT006 *
		process.QWAcc_Noff260Vz4_pT008 *
		process.QWAcc_Noff260Vz4_pT010 *
		process.QWAcc_Noff260Vz4_pT012 *
		process.QWAcc_Noff260Vz4_pT015 *
		process.QWAcc_Noff260Vz4_pT020 *
		process.QWAcc_Noff260Vz4_pT025 *
		process.QWAcc_Noff260Vz4_pT030 *
		process.QWAcc_Noff260Vz4_pT035 *
		process.QWAcc_Noff260Vz4_pT040 *
		process.QWAcc_Noff260Vz4_pT050 *
		process.QWAcc_Noff260Vz4_pT060 *
		process.QWAcc_Noff260Vz4_pT070 *
		process.QWAcc_Noff260Vz4_pT080 *
		process.QWAcc_Noff260Vz4_pT100
		)

process.ana400Vz4 = cms.Path(
		process.pre_ana400Vz4 *
		process.QWAcc_Noff400Vz4_pT004 *
		process.QWAcc_Noff400Vz4_pT005 *
		process.QWAcc_Noff400Vz4_pT006 *
		process.QWAcc_Noff400Vz4_pT008 *
		process.QWAcc_Noff400Vz4_pT010 *
		process.QWAcc_Noff400Vz4_pT012 *
		process.QWAcc_Noff400Vz4_pT015 *
		process.QWAcc_Noff400Vz4_pT020 *
		process.QWAcc_Noff400Vz4_pT025 *
		process.QWAcc_Noff400Vz4_pT030 *
		process.QWAcc_Noff400Vz4_pT035 *
		process.QWAcc_Noff400Vz4_pT040 *
		process.QWAcc_Noff400Vz4_pT050 *
		process.QWAcc_Noff400Vz4_pT060 *
		process.QWAcc_Noff400Vz4_pT070 *
		process.QWAcc_Noff400Vz4_pT080 *
		process.QWAcc_Noff400Vz4_pT100
		)

process.ana800Vz4 = cms.Path(
		process.pre_ana800Vz4 *
		process.QWAcc_Noff800Vz4_pT004 *
		process.QWAcc_Noff800Vz4_pT005 *
		process.QWAcc_Noff800Vz4_pT006 *
		process.QWAcc_Noff800Vz4_pT008 *
		process.QWAcc_Noff800Vz4_pT010 *
		process.QWAcc_Noff800Vz4_pT012 *
		process.QWAcc_Noff800Vz4_pT015 *
		process.QWAcc_Noff800Vz4_pT020 *
		process.QWAcc_Noff800Vz4_pT025 *
		process.QWAcc_Noff800Vz4_pT030 *
		process.QWAcc_Noff800Vz4_pT035 *
		process.QWAcc_Noff800Vz4_pT040 *
		process.QWAcc_Noff800Vz4_pT050 *
		process.QWAcc_Noff800Vz4_pT060 *
		process.QWAcc_Noff800Vz4_pT070 *
		process.QWAcc_Noff800Vz4_pT080 *
		process.QWAcc_Noff800Vz4_pT100
		)

process.ana12XVz4 = cms.Path(
		process.pre_ana12XVz4 *
		process.QWAcc_Noff12XVz4_pT004 *
		process.QWAcc_Noff12XVz4_pT005 *
		process.QWAcc_Noff12XVz4_pT006 *
		process.QWAcc_Noff12XVz4_pT008 *
		process.QWAcc_Noff12XVz4_pT010 *
		process.QWAcc_Noff12XVz4_pT012 *
		process.QWAcc_Noff12XVz4_pT015 *
		process.QWAcc_Noff12XVz4_pT020 *
		process.QWAcc_Noff12XVz4_pT025 *
		process.QWAcc_Noff12XVz4_pT030 *
		process.QWAcc_Noff12XVz4_pT035 *
		process.QWAcc_Noff12XVz4_pT040 *
		process.QWAcc_Noff12XVz4_pT050 *
		process.QWAcc_Noff12XVz4_pT060 *
		process.QWAcc_Noff12XVz4_pT070 *
		process.QWAcc_Noff12XVz4_pT080 *
		process.QWAcc_Noff12XVz4_pT100
		)

process.ana20XVz4 = cms.Path(
		process.pre_ana20XVz4 *
		process.QWAcc_Noff20XVz4_pT004 *
		process.QWAcc_Noff20XVz4_pT005 *
		process.QWAcc_Noff20XVz4_pT006 *
		process.QWAcc_Noff20XVz4_pT008 *
		process.QWAcc_Noff20XVz4_pT010 *
		process.QWAcc_Noff20XVz4_pT012 *
		process.QWAcc_Noff20XVz4_pT015 *
		process.QWAcc_Noff20XVz4_pT020 *
		process.QWAcc_Noff20XVz4_pT025 *
		process.QWAcc_Noff20XVz4_pT030 *
		process.QWAcc_Noff20XVz4_pT035 *
		process.QWAcc_Noff20XVz4_pT040 *
		process.QWAcc_Noff20XVz4_pT050 *
		process.QWAcc_Noff20XVz4_pT060 *
		process.QWAcc_Noff20XVz4_pT070 *
		process.QWAcc_Noff20XVz4_pT080 *
		process.QWAcc_Noff20XVz4_pT100
		)


## Vz5
process.ana120Vz5 = cms.Path(
		process.pre_ana120Vz5 *
		process.QWAcc_Noff120Vz5_pT004 *
		process.QWAcc_Noff120Vz5_pT005 *
		process.QWAcc_Noff120Vz5_pT006 *
		process.QWAcc_Noff120Vz5_pT008 *
		process.QWAcc_Noff120Vz5_pT010 *
		process.QWAcc_Noff120Vz5_pT012 *
		process.QWAcc_Noff120Vz5_pT015 *
		process.QWAcc_Noff120Vz5_pT020 *
		process.QWAcc_Noff120Vz5_pT025 *
		process.QWAcc_Noff120Vz5_pT030 *
		process.QWAcc_Noff120Vz5_pT035 *
		process.QWAcc_Noff120Vz5_pT040 *
		process.QWAcc_Noff120Vz5_pT050 *
		process.QWAcc_Noff120Vz5_pT060 *
		process.QWAcc_Noff120Vz5_pT070 *
		process.QWAcc_Noff120Vz5_pT080 *
		process.QWAcc_Noff120Vz5_pT100
		)

process.ana260Vz5 = cms.Path(
		process.pre_ana260Vz5 *
		process.QWAcc_Noff260Vz5_pT004 *
		process.QWAcc_Noff260Vz5_pT005 *
		process.QWAcc_Noff260Vz5_pT006 *
		process.QWAcc_Noff260Vz5_pT008 *
		process.QWAcc_Noff260Vz5_pT010 *
		process.QWAcc_Noff260Vz5_pT012 *
		process.QWAcc_Noff260Vz5_pT015 *
		process.QWAcc_Noff260Vz5_pT020 *
		process.QWAcc_Noff260Vz5_pT025 *
		process.QWAcc_Noff260Vz5_pT030 *
		process.QWAcc_Noff260Vz5_pT035 *
		process.QWAcc_Noff260Vz5_pT040 *
		process.QWAcc_Noff260Vz5_pT050 *
		process.QWAcc_Noff260Vz5_pT060 *
		process.QWAcc_Noff260Vz5_pT070 *
		process.QWAcc_Noff260Vz5_pT080 *
		process.QWAcc_Noff260Vz5_pT100
		)

process.ana400Vz5 = cms.Path(
		process.pre_ana400Vz5 *
		process.QWAcc_Noff400Vz5_pT004 *
		process.QWAcc_Noff400Vz5_pT005 *
		process.QWAcc_Noff400Vz5_pT006 *
		process.QWAcc_Noff400Vz5_pT008 *
		process.QWAcc_Noff400Vz5_pT010 *
		process.QWAcc_Noff400Vz5_pT012 *
		process.QWAcc_Noff400Vz5_pT015 *
		process.QWAcc_Noff400Vz5_pT020 *
		process.QWAcc_Noff400Vz5_pT025 *
		process.QWAcc_Noff400Vz5_pT030 *
		process.QWAcc_Noff400Vz5_pT035 *
		process.QWAcc_Noff400Vz5_pT040 *
		process.QWAcc_Noff400Vz5_pT050 *
		process.QWAcc_Noff400Vz5_pT060 *
		process.QWAcc_Noff400Vz5_pT070 *
		process.QWAcc_Noff400Vz5_pT080 *
		process.QWAcc_Noff400Vz5_pT100
		)

process.ana800Vz5 = cms.Path(
		process.pre_ana800Vz5 *
		process.QWAcc_Noff800Vz5_pT004 *
		process.QWAcc_Noff800Vz5_pT005 *
		process.QWAcc_Noff800Vz5_pT006 *
		process.QWAcc_Noff800Vz5_pT008 *
		process.QWAcc_Noff800Vz5_pT010 *
		process.QWAcc_Noff800Vz5_pT012 *
		process.QWAcc_Noff800Vz5_pT015 *
		process.QWAcc_Noff800Vz5_pT020 *
		process.QWAcc_Noff800Vz5_pT025 *
		process.QWAcc_Noff800Vz5_pT030 *
		process.QWAcc_Noff800Vz5_pT035 *
		process.QWAcc_Noff800Vz5_pT040 *
		process.QWAcc_Noff800Vz5_pT050 *
		process.QWAcc_Noff800Vz5_pT060 *
		process.QWAcc_Noff800Vz5_pT070 *
		process.QWAcc_Noff800Vz5_pT080 *
		process.QWAcc_Noff800Vz5_pT100
		)

process.ana12XVz5 = cms.Path(
		process.pre_ana12XVz5 *
		process.QWAcc_Noff12XVz5_pT004 *
		process.QWAcc_Noff12XVz5_pT005 *
		process.QWAcc_Noff12XVz5_pT006 *
		process.QWAcc_Noff12XVz5_pT008 *
		process.QWAcc_Noff12XVz5_pT010 *
		process.QWAcc_Noff12XVz5_pT012 *
		process.QWAcc_Noff12XVz5_pT015 *
		process.QWAcc_Noff12XVz5_pT020 *
		process.QWAcc_Noff12XVz5_pT025 *
		process.QWAcc_Noff12XVz5_pT030 *
		process.QWAcc_Noff12XVz5_pT035 *
		process.QWAcc_Noff12XVz5_pT040 *
		process.QWAcc_Noff12XVz5_pT050 *
		process.QWAcc_Noff12XVz5_pT060 *
		process.QWAcc_Noff12XVz5_pT070 *
		process.QWAcc_Noff12XVz5_pT080 *
		process.QWAcc_Noff12XVz5_pT100
		)

process.ana20XVz5 = cms.Path(
		process.pre_ana20XVz5 *
		process.QWAcc_Noff20XVz5_pT004 *
		process.QWAcc_Noff20XVz5_pT005 *
		process.QWAcc_Noff20XVz5_pT006 *
		process.QWAcc_Noff20XVz5_pT008 *
		process.QWAcc_Noff20XVz5_pT010 *
		process.QWAcc_Noff20XVz5_pT012 *
		process.QWAcc_Noff20XVz5_pT015 *
		process.QWAcc_Noff20XVz5_pT020 *
		process.QWAcc_Noff20XVz5_pT025 *
		process.QWAcc_Noff20XVz5_pT030 *
		process.QWAcc_Noff20XVz5_pT035 *
		process.QWAcc_Noff20XVz5_pT040 *
		process.QWAcc_Noff20XVz5_pT050 *
		process.QWAcc_Noff20XVz5_pT060 *
		process.QWAcc_Noff20XVz5_pT070 *
		process.QWAcc_Noff20XVz5_pT080 *
		process.QWAcc_Noff20XVz5_pT100
		)


## Vz6
process.ana120Vz6 = cms.Path(
		process.pre_ana120Vz6 *
		process.QWAcc_Noff120Vz6_pT004 *
		process.QWAcc_Noff120Vz6_pT005 *
		process.QWAcc_Noff120Vz6_pT006 *
		process.QWAcc_Noff120Vz6_pT008 *
		process.QWAcc_Noff120Vz6_pT010 *
		process.QWAcc_Noff120Vz6_pT012 *
		process.QWAcc_Noff120Vz6_pT015 *
		process.QWAcc_Noff120Vz6_pT020 *
		process.QWAcc_Noff120Vz6_pT025 *
		process.QWAcc_Noff120Vz6_pT030 *
		process.QWAcc_Noff120Vz6_pT035 *
		process.QWAcc_Noff120Vz6_pT040 *
		process.QWAcc_Noff120Vz6_pT050 *
		process.QWAcc_Noff120Vz6_pT060 *
		process.QWAcc_Noff120Vz6_pT070 *
		process.QWAcc_Noff120Vz6_pT080 *
		process.QWAcc_Noff120Vz6_pT100
		)

process.ana260Vz6 = cms.Path(
		process.pre_ana260Vz6 *
		process.QWAcc_Noff260Vz6_pT004 *
		process.QWAcc_Noff260Vz6_pT005 *
		process.QWAcc_Noff260Vz6_pT006 *
		process.QWAcc_Noff260Vz6_pT008 *
		process.QWAcc_Noff260Vz6_pT010 *
		process.QWAcc_Noff260Vz6_pT012 *
		process.QWAcc_Noff260Vz6_pT015 *
		process.QWAcc_Noff260Vz6_pT020 *
		process.QWAcc_Noff260Vz6_pT025 *
		process.QWAcc_Noff260Vz6_pT030 *
		process.QWAcc_Noff260Vz6_pT035 *
		process.QWAcc_Noff260Vz6_pT040 *
		process.QWAcc_Noff260Vz6_pT050 *
		process.QWAcc_Noff260Vz6_pT060 *
		process.QWAcc_Noff260Vz6_pT070 *
		process.QWAcc_Noff260Vz6_pT080 *
		process.QWAcc_Noff260Vz6_pT100
		)

process.ana400Vz6 = cms.Path(
		process.pre_ana400Vz6 *
		process.QWAcc_Noff400Vz6_pT004 *
		process.QWAcc_Noff400Vz6_pT005 *
		process.QWAcc_Noff400Vz6_pT006 *
		process.QWAcc_Noff400Vz6_pT008 *
		process.QWAcc_Noff400Vz6_pT010 *
		process.QWAcc_Noff400Vz6_pT012 *
		process.QWAcc_Noff400Vz6_pT015 *
		process.QWAcc_Noff400Vz6_pT020 *
		process.QWAcc_Noff400Vz6_pT025 *
		process.QWAcc_Noff400Vz6_pT030 *
		process.QWAcc_Noff400Vz6_pT035 *
		process.QWAcc_Noff400Vz6_pT040 *
		process.QWAcc_Noff400Vz6_pT050 *
		process.QWAcc_Noff400Vz6_pT060 *
		process.QWAcc_Noff400Vz6_pT070 *
		process.QWAcc_Noff400Vz6_pT080 *
		process.QWAcc_Noff400Vz6_pT100
		)

process.ana800Vz6 = cms.Path(
		process.pre_ana800Vz6 *
		process.QWAcc_Noff800Vz6_pT004 *
		process.QWAcc_Noff800Vz6_pT005 *
		process.QWAcc_Noff800Vz6_pT006 *
		process.QWAcc_Noff800Vz6_pT008 *
		process.QWAcc_Noff800Vz6_pT010 *
		process.QWAcc_Noff800Vz6_pT012 *
		process.QWAcc_Noff800Vz6_pT015 *
		process.QWAcc_Noff800Vz6_pT020 *
		process.QWAcc_Noff800Vz6_pT025 *
		process.QWAcc_Noff800Vz6_pT030 *
		process.QWAcc_Noff800Vz6_pT035 *
		process.QWAcc_Noff800Vz6_pT040 *
		process.QWAcc_Noff800Vz6_pT050 *
		process.QWAcc_Noff800Vz6_pT060 *
		process.QWAcc_Noff800Vz6_pT070 *
		process.QWAcc_Noff800Vz6_pT080 *
		process.QWAcc_Noff800Vz6_pT100
		)

process.ana12XVz6 = cms.Path(
		process.pre_ana12XVz6 *
		process.QWAcc_Noff12XVz6_pT004 *
		process.QWAcc_Noff12XVz6_pT005 *
		process.QWAcc_Noff12XVz6_pT006 *
		process.QWAcc_Noff12XVz6_pT008 *
		process.QWAcc_Noff12XVz6_pT010 *
		process.QWAcc_Noff12XVz6_pT012 *
		process.QWAcc_Noff12XVz6_pT015 *
		process.QWAcc_Noff12XVz6_pT020 *
		process.QWAcc_Noff12XVz6_pT025 *
		process.QWAcc_Noff12XVz6_pT030 *
		process.QWAcc_Noff12XVz6_pT035 *
		process.QWAcc_Noff12XVz6_pT040 *
		process.QWAcc_Noff12XVz6_pT050 *
		process.QWAcc_Noff12XVz6_pT060 *
		process.QWAcc_Noff12XVz6_pT070 *
		process.QWAcc_Noff12XVz6_pT080 *
		process.QWAcc_Noff12XVz6_pT100
		)

process.ana20XVz6 = cms.Path(
		process.pre_ana20XVz6 *
		process.QWAcc_Noff20XVz6_pT004 *
		process.QWAcc_Noff20XVz6_pT005 *
		process.QWAcc_Noff20XVz6_pT006 *
		process.QWAcc_Noff20XVz6_pT008 *
		process.QWAcc_Noff20XVz6_pT010 *
		process.QWAcc_Noff20XVz6_pT012 *
		process.QWAcc_Noff20XVz6_pT015 *
		process.QWAcc_Noff20XVz6_pT020 *
		process.QWAcc_Noff20XVz6_pT025 *
		process.QWAcc_Noff20XVz6_pT030 *
		process.QWAcc_Noff20XVz6_pT035 *
		process.QWAcc_Noff20XVz6_pT040 *
		process.QWAcc_Noff20XVz6_pT050 *
		process.QWAcc_Noff20XVz6_pT060 *
		process.QWAcc_Noff20XVz6_pT070 *
		process.QWAcc_Noff20XVz6_pT080 *
		process.QWAcc_Noff20XVz6_pT100
		)


## Vz7
process.ana120Vz7 = cms.Path(
		process.pre_ana120Vz7 *
		process.QWAcc_Noff120Vz7_pT004 *
		process.QWAcc_Noff120Vz7_pT005 *
		process.QWAcc_Noff120Vz7_pT006 *
		process.QWAcc_Noff120Vz7_pT008 *
		process.QWAcc_Noff120Vz7_pT010 *
		process.QWAcc_Noff120Vz7_pT012 *
		process.QWAcc_Noff120Vz7_pT015 *
		process.QWAcc_Noff120Vz7_pT020 *
		process.QWAcc_Noff120Vz7_pT025 *
		process.QWAcc_Noff120Vz7_pT030 *
		process.QWAcc_Noff120Vz7_pT035 *
		process.QWAcc_Noff120Vz7_pT040 *
		process.QWAcc_Noff120Vz7_pT050 *
		process.QWAcc_Noff120Vz7_pT060 *
		process.QWAcc_Noff120Vz7_pT070 *
		process.QWAcc_Noff120Vz7_pT080 *
		process.QWAcc_Noff120Vz7_pT100
		)

process.ana260Vz7 = cms.Path(
		process.pre_ana260Vz7 *
		process.QWAcc_Noff260Vz7_pT004 *
		process.QWAcc_Noff260Vz7_pT005 *
		process.QWAcc_Noff260Vz7_pT006 *
		process.QWAcc_Noff260Vz7_pT008 *
		process.QWAcc_Noff260Vz7_pT010 *
		process.QWAcc_Noff260Vz7_pT012 *
		process.QWAcc_Noff260Vz7_pT015 *
		process.QWAcc_Noff260Vz7_pT020 *
		process.QWAcc_Noff260Vz7_pT025 *
		process.QWAcc_Noff260Vz7_pT030 *
		process.QWAcc_Noff260Vz7_pT035 *
		process.QWAcc_Noff260Vz7_pT040 *
		process.QWAcc_Noff260Vz7_pT050 *
		process.QWAcc_Noff260Vz7_pT060 *
		process.QWAcc_Noff260Vz7_pT070 *
		process.QWAcc_Noff260Vz7_pT080 *
		process.QWAcc_Noff260Vz7_pT100
		)

process.ana400Vz7 = cms.Path(
		process.pre_ana400Vz7 *
		process.QWAcc_Noff400Vz7_pT004 *
		process.QWAcc_Noff400Vz7_pT005 *
		process.QWAcc_Noff400Vz7_pT006 *
		process.QWAcc_Noff400Vz7_pT008 *
		process.QWAcc_Noff400Vz7_pT010 *
		process.QWAcc_Noff400Vz7_pT012 *
		process.QWAcc_Noff400Vz7_pT015 *
		process.QWAcc_Noff400Vz7_pT020 *
		process.QWAcc_Noff400Vz7_pT025 *
		process.QWAcc_Noff400Vz7_pT030 *
		process.QWAcc_Noff400Vz7_pT035 *
		process.QWAcc_Noff400Vz7_pT040 *
		process.QWAcc_Noff400Vz7_pT050 *
		process.QWAcc_Noff400Vz7_pT060 *
		process.QWAcc_Noff400Vz7_pT070 *
		process.QWAcc_Noff400Vz7_pT080 *
		process.QWAcc_Noff400Vz7_pT100
		)

process.ana800Vz7 = cms.Path(
		process.pre_ana800Vz7 *
		process.QWAcc_Noff800Vz7_pT004 *
		process.QWAcc_Noff800Vz7_pT005 *
		process.QWAcc_Noff800Vz7_pT006 *
		process.QWAcc_Noff800Vz7_pT008 *
		process.QWAcc_Noff800Vz7_pT010 *
		process.QWAcc_Noff800Vz7_pT012 *
		process.QWAcc_Noff800Vz7_pT015 *
		process.QWAcc_Noff800Vz7_pT020 *
		process.QWAcc_Noff800Vz7_pT025 *
		process.QWAcc_Noff800Vz7_pT030 *
		process.QWAcc_Noff800Vz7_pT035 *
		process.QWAcc_Noff800Vz7_pT040 *
		process.QWAcc_Noff800Vz7_pT050 *
		process.QWAcc_Noff800Vz7_pT060 *
		process.QWAcc_Noff800Vz7_pT070 *
		process.QWAcc_Noff800Vz7_pT080 *
		process.QWAcc_Noff800Vz7_pT100
		)

process.ana12XVz7 = cms.Path(
		process.pre_ana12XVz7 *
		process.QWAcc_Noff12XVz7_pT004 *
		process.QWAcc_Noff12XVz7_pT005 *
		process.QWAcc_Noff12XVz7_pT006 *
		process.QWAcc_Noff12XVz7_pT008 *
		process.QWAcc_Noff12XVz7_pT010 *
		process.QWAcc_Noff12XVz7_pT012 *
		process.QWAcc_Noff12XVz7_pT015 *
		process.QWAcc_Noff12XVz7_pT020 *
		process.QWAcc_Noff12XVz7_pT025 *
		process.QWAcc_Noff12XVz7_pT030 *
		process.QWAcc_Noff12XVz7_pT035 *
		process.QWAcc_Noff12XVz7_pT040 *
		process.QWAcc_Noff12XVz7_pT050 *
		process.QWAcc_Noff12XVz7_pT060 *
		process.QWAcc_Noff12XVz7_pT070 *
		process.QWAcc_Noff12XVz7_pT080 *
		process.QWAcc_Noff12XVz7_pT100
		)

process.ana20XVz7 = cms.Path(
		process.pre_ana20XVz7 *
		process.QWAcc_Noff20XVz7_pT004 *
		process.QWAcc_Noff20XVz7_pT005 *
		process.QWAcc_Noff20XVz7_pT006 *
		process.QWAcc_Noff20XVz7_pT008 *
		process.QWAcc_Noff20XVz7_pT010 *
		process.QWAcc_Noff20XVz7_pT012 *
		process.QWAcc_Noff20XVz7_pT015 *
		process.QWAcc_Noff20XVz7_pT020 *
		process.QWAcc_Noff20XVz7_pT025 *
		process.QWAcc_Noff20XVz7_pT030 *
		process.QWAcc_Noff20XVz7_pT035 *
		process.QWAcc_Noff20XVz7_pT040 *
		process.QWAcc_Noff20XVz7_pT050 *
		process.QWAcc_Noff20XVz7_pT060 *
		process.QWAcc_Noff20XVz7_pT070 *
		process.QWAcc_Noff20XVz7_pT080 *
		process.QWAcc_Noff20XVz7_pT100
		)


## Vz8
process.ana120Vz8 = cms.Path(
		process.pre_ana120Vz8 *
		process.QWAcc_Noff120Vz8_pT004 *
		process.QWAcc_Noff120Vz8_pT005 *
		process.QWAcc_Noff120Vz8_pT006 *
		process.QWAcc_Noff120Vz8_pT008 *
		process.QWAcc_Noff120Vz8_pT010 *
		process.QWAcc_Noff120Vz8_pT012 *
		process.QWAcc_Noff120Vz8_pT015 *
		process.QWAcc_Noff120Vz8_pT020 *
		process.QWAcc_Noff120Vz8_pT025 *
		process.QWAcc_Noff120Vz8_pT030 *
		process.QWAcc_Noff120Vz8_pT035 *
		process.QWAcc_Noff120Vz8_pT040 *
		process.QWAcc_Noff120Vz8_pT050 *
		process.QWAcc_Noff120Vz8_pT060 *
		process.QWAcc_Noff120Vz8_pT070 *
		process.QWAcc_Noff120Vz8_pT080 *
		process.QWAcc_Noff120Vz8_pT100
		)

process.ana260Vz8 = cms.Path(
		process.pre_ana260Vz8 *
		process.QWAcc_Noff260Vz8_pT004 *
		process.QWAcc_Noff260Vz8_pT005 *
		process.QWAcc_Noff260Vz8_pT006 *
		process.QWAcc_Noff260Vz8_pT008 *
		process.QWAcc_Noff260Vz8_pT010 *
		process.QWAcc_Noff260Vz8_pT012 *
		process.QWAcc_Noff260Vz8_pT015 *
		process.QWAcc_Noff260Vz8_pT020 *
		process.QWAcc_Noff260Vz8_pT025 *
		process.QWAcc_Noff260Vz8_pT030 *
		process.QWAcc_Noff260Vz8_pT035 *
		process.QWAcc_Noff260Vz8_pT040 *
		process.QWAcc_Noff260Vz8_pT050 *
		process.QWAcc_Noff260Vz8_pT060 *
		process.QWAcc_Noff260Vz8_pT070 *
		process.QWAcc_Noff260Vz8_pT080 *
		process.QWAcc_Noff260Vz8_pT100
		)

process.ana400Vz8 = cms.Path(
		process.pre_ana400Vz8 *
		process.QWAcc_Noff400Vz8_pT004 *
		process.QWAcc_Noff400Vz8_pT005 *
		process.QWAcc_Noff400Vz8_pT006 *
		process.QWAcc_Noff400Vz8_pT008 *
		process.QWAcc_Noff400Vz8_pT010 *
		process.QWAcc_Noff400Vz8_pT012 *
		process.QWAcc_Noff400Vz8_pT015 *
		process.QWAcc_Noff400Vz8_pT020 *
		process.QWAcc_Noff400Vz8_pT025 *
		process.QWAcc_Noff400Vz8_pT030 *
		process.QWAcc_Noff400Vz8_pT035 *
		process.QWAcc_Noff400Vz8_pT040 *
		process.QWAcc_Noff400Vz8_pT050 *
		process.QWAcc_Noff400Vz8_pT060 *
		process.QWAcc_Noff400Vz8_pT070 *
		process.QWAcc_Noff400Vz8_pT080 *
		process.QWAcc_Noff400Vz8_pT100
		)

process.ana800Vz8 = cms.Path(
		process.pre_ana800Vz8 *
		process.QWAcc_Noff800Vz8_pT004 *
		process.QWAcc_Noff800Vz8_pT005 *
		process.QWAcc_Noff800Vz8_pT006 *
		process.QWAcc_Noff800Vz8_pT008 *
		process.QWAcc_Noff800Vz8_pT010 *
		process.QWAcc_Noff800Vz8_pT012 *
		process.QWAcc_Noff800Vz8_pT015 *
		process.QWAcc_Noff800Vz8_pT020 *
		process.QWAcc_Noff800Vz8_pT025 *
		process.QWAcc_Noff800Vz8_pT030 *
		process.QWAcc_Noff800Vz8_pT035 *
		process.QWAcc_Noff800Vz8_pT040 *
		process.QWAcc_Noff800Vz8_pT050 *
		process.QWAcc_Noff800Vz8_pT060 *
		process.QWAcc_Noff800Vz8_pT070 *
		process.QWAcc_Noff800Vz8_pT080 *
		process.QWAcc_Noff800Vz8_pT100
		)

process.ana12XVz8 = cms.Path(
		process.pre_ana12XVz8 *
		process.QWAcc_Noff12XVz8_pT004 *
		process.QWAcc_Noff12XVz8_pT005 *
		process.QWAcc_Noff12XVz8_pT006 *
		process.QWAcc_Noff12XVz8_pT008 *
		process.QWAcc_Noff12XVz8_pT010 *
		process.QWAcc_Noff12XVz8_pT012 *
		process.QWAcc_Noff12XVz8_pT015 *
		process.QWAcc_Noff12XVz8_pT020 *
		process.QWAcc_Noff12XVz8_pT025 *
		process.QWAcc_Noff12XVz8_pT030 *
		process.QWAcc_Noff12XVz8_pT035 *
		process.QWAcc_Noff12XVz8_pT040 *
		process.QWAcc_Noff12XVz8_pT050 *
		process.QWAcc_Noff12XVz8_pT060 *
		process.QWAcc_Noff12XVz8_pT070 *
		process.QWAcc_Noff12XVz8_pT080 *
		process.QWAcc_Noff12XVz8_pT100
		)

process.ana20XVz8 = cms.Path(
		process.pre_ana20XVz8 *
		process.QWAcc_Noff20XVz8_pT004 *
		process.QWAcc_Noff20XVz8_pT005 *
		process.QWAcc_Noff20XVz8_pT006 *
		process.QWAcc_Noff20XVz8_pT008 *
		process.QWAcc_Noff20XVz8_pT010 *
		process.QWAcc_Noff20XVz8_pT012 *
		process.QWAcc_Noff20XVz8_pT015 *
		process.QWAcc_Noff20XVz8_pT020 *
		process.QWAcc_Noff20XVz8_pT025 *
		process.QWAcc_Noff20XVz8_pT030 *
		process.QWAcc_Noff20XVz8_pT035 *
		process.QWAcc_Noff20XVz8_pT040 *
		process.QWAcc_Noff20XVz8_pT050 *
		process.QWAcc_Noff20XVz8_pT060 *
		process.QWAcc_Noff20XVz8_pT070 *
		process.QWAcc_Noff20XVz8_pT080 *
		process.QWAcc_Noff20XVz8_pT100
		)


## Vz9
process.ana120Vz9 = cms.Path(
		process.pre_ana120Vz9 *
		process.QWAcc_Noff120Vz9_pT004 *
		process.QWAcc_Noff120Vz9_pT005 *
		process.QWAcc_Noff120Vz9_pT006 *
		process.QWAcc_Noff120Vz9_pT008 *
		process.QWAcc_Noff120Vz9_pT010 *
		process.QWAcc_Noff120Vz9_pT012 *
		process.QWAcc_Noff120Vz9_pT015 *
		process.QWAcc_Noff120Vz9_pT020 *
		process.QWAcc_Noff120Vz9_pT025 *
		process.QWAcc_Noff120Vz9_pT030 *
		process.QWAcc_Noff120Vz9_pT035 *
		process.QWAcc_Noff120Vz9_pT040 *
		process.QWAcc_Noff120Vz9_pT050 *
		process.QWAcc_Noff120Vz9_pT060 *
		process.QWAcc_Noff120Vz9_pT070 *
		process.QWAcc_Noff120Vz9_pT080 *
		process.QWAcc_Noff120Vz9_pT100
		)

process.ana260Vz9 = cms.Path(
		process.pre_ana260Vz9 *
		process.QWAcc_Noff260Vz9_pT004 *
		process.QWAcc_Noff260Vz9_pT005 *
		process.QWAcc_Noff260Vz9_pT006 *
		process.QWAcc_Noff260Vz9_pT008 *
		process.QWAcc_Noff260Vz9_pT010 *
		process.QWAcc_Noff260Vz9_pT012 *
		process.QWAcc_Noff260Vz9_pT015 *
		process.QWAcc_Noff260Vz9_pT020 *
		process.QWAcc_Noff260Vz9_pT025 *
		process.QWAcc_Noff260Vz9_pT030 *
		process.QWAcc_Noff260Vz9_pT035 *
		process.QWAcc_Noff260Vz9_pT040 *
		process.QWAcc_Noff260Vz9_pT050 *
		process.QWAcc_Noff260Vz9_pT060 *
		process.QWAcc_Noff260Vz9_pT070 *
		process.QWAcc_Noff260Vz9_pT080 *
		process.QWAcc_Noff260Vz9_pT100
		)

process.ana400Vz9 = cms.Path(
		process.pre_ana400Vz9 *
		process.QWAcc_Noff400Vz9_pT004 *
		process.QWAcc_Noff400Vz9_pT005 *
		process.QWAcc_Noff400Vz9_pT006 *
		process.QWAcc_Noff400Vz9_pT008 *
		process.QWAcc_Noff400Vz9_pT010 *
		process.QWAcc_Noff400Vz9_pT012 *
		process.QWAcc_Noff400Vz9_pT015 *
		process.QWAcc_Noff400Vz9_pT020 *
		process.QWAcc_Noff400Vz9_pT025 *
		process.QWAcc_Noff400Vz9_pT030 *
		process.QWAcc_Noff400Vz9_pT035 *
		process.QWAcc_Noff400Vz9_pT040 *
		process.QWAcc_Noff400Vz9_pT050 *
		process.QWAcc_Noff400Vz9_pT060 *
		process.QWAcc_Noff400Vz9_pT070 *
		process.QWAcc_Noff400Vz9_pT080 *
		process.QWAcc_Noff400Vz9_pT100
		)

process.ana800Vz9 = cms.Path(
		process.pre_ana800Vz9 *
		process.QWAcc_Noff800Vz9_pT004 *
		process.QWAcc_Noff800Vz9_pT005 *
		process.QWAcc_Noff800Vz9_pT006 *
		process.QWAcc_Noff800Vz9_pT008 *
		process.QWAcc_Noff800Vz9_pT010 *
		process.QWAcc_Noff800Vz9_pT012 *
		process.QWAcc_Noff800Vz9_pT015 *
		process.QWAcc_Noff800Vz9_pT020 *
		process.QWAcc_Noff800Vz9_pT025 *
		process.QWAcc_Noff800Vz9_pT030 *
		process.QWAcc_Noff800Vz9_pT035 *
		process.QWAcc_Noff800Vz9_pT040 *
		process.QWAcc_Noff800Vz9_pT050 *
		process.QWAcc_Noff800Vz9_pT060 *
		process.QWAcc_Noff800Vz9_pT070 *
		process.QWAcc_Noff800Vz9_pT080 *
		process.QWAcc_Noff800Vz9_pT100
		)

process.ana12XVz9 = cms.Path(
		process.pre_ana12XVz9 *
		process.QWAcc_Noff12XVz9_pT004 *
		process.QWAcc_Noff12XVz9_pT005 *
		process.QWAcc_Noff12XVz9_pT006 *
		process.QWAcc_Noff12XVz9_pT008 *
		process.QWAcc_Noff12XVz9_pT010 *
		process.QWAcc_Noff12XVz9_pT012 *
		process.QWAcc_Noff12XVz9_pT015 *
		process.QWAcc_Noff12XVz9_pT020 *
		process.QWAcc_Noff12XVz9_pT025 *
		process.QWAcc_Noff12XVz9_pT030 *
		process.QWAcc_Noff12XVz9_pT035 *
		process.QWAcc_Noff12XVz9_pT040 *
		process.QWAcc_Noff12XVz9_pT050 *
		process.QWAcc_Noff12XVz9_pT060 *
		process.QWAcc_Noff12XVz9_pT070 *
		process.QWAcc_Noff12XVz9_pT080 *
		process.QWAcc_Noff12XVz9_pT100
		)

process.ana20XVz9 = cms.Path(
		process.pre_ana20XVz9 *
		process.QWAcc_Noff20XVz9_pT004 *
		process.QWAcc_Noff20XVz9_pT005 *
		process.QWAcc_Noff20XVz9_pT006 *
		process.QWAcc_Noff20XVz9_pT008 *
		process.QWAcc_Noff20XVz9_pT010 *
		process.QWAcc_Noff20XVz9_pT012 *
		process.QWAcc_Noff20XVz9_pT015 *
		process.QWAcc_Noff20XVz9_pT020 *
		process.QWAcc_Noff20XVz9_pT025 *
		process.QWAcc_Noff20XVz9_pT030 *
		process.QWAcc_Noff20XVz9_pT035 *
		process.QWAcc_Noff20XVz9_pT040 *
		process.QWAcc_Noff20XVz9_pT050 *
		process.QWAcc_Noff20XVz9_pT060 *
		process.QWAcc_Noff20XVz9_pT070 *
		process.QWAcc_Noff20XVz9_pT080 *
		process.QWAcc_Noff20XVz9_pT100
		)


#process.ana = cms.Path(process.eventSelection*process.makeEvent*process.ppRecoCentFilter*process.cumugap * process.vectMonW )

process.schedule = cms.Schedule(
#	process.ana,
	process.ana120Vz0,
	process.ana260Vz0,
	process.ana400Vz0,
	process.ana800Vz0,
	process.ana12XVz0,
	process.ana20XVz0,

	process.ana120Vz1,
	process.ana260Vz1,
	process.ana400Vz1,
	process.ana800Vz1,
	process.ana12XVz1,
	process.ana20XVz1,

	process.ana120Vz2,
	process.ana260Vz2,
	process.ana400Vz2,
	process.ana800Vz2,
	process.ana12XVz2,
	process.ana20XVz2,

	process.ana120Vz3,
	process.ana260Vz3,
	process.ana400Vz3,
	process.ana800Vz3,
	process.ana12XVz3,
	process.ana20XVz3,

	process.ana120Vz4,
	process.ana260Vz4,
	process.ana400Vz4,
	process.ana800Vz4,
	process.ana12XVz4,
	process.ana20XVz4,

	process.ana120Vz5,
	process.ana260Vz5,
	process.ana400Vz5,
	process.ana800Vz5,
	process.ana12XVz5,
	process.ana20XVz5,

	process.ana120Vz6,
	process.ana260Vz6,
	process.ana400Vz6,
	process.ana800Vz6,
	process.ana12XVz6,
	process.ana20XVz6,

	process.ana120Vz7,
	process.ana260Vz7,
	process.ana400Vz7,
	process.ana800Vz7,
	process.ana12XVz7,
	process.ana20XVz7,

	process.ana120Vz8,
	process.ana260Vz8,
	process.ana400Vz8,
	process.ana800Vz8,
	process.ana12XVz8,
	process.ana20XVz8,

	process.ana120Vz9,
	process.ana260Vz9,
	process.ana400Vz9,
	process.ana800Vz9,
	process.ana12XVz9,
	process.ana20XVz9,

)
