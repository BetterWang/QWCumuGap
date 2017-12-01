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


process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')

process.primaryVertexFilter.src = cms.InputTag("offlinePrimaryVertices")

process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
process.ppRecoCentFilter = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(60, 180)
		),
	BinLabel = cms.InputTag("centralityBins")
	)

process.NoScraping = cms.EDFilter("FilterOutScraping",
 applyfilter = cms.untracked.bool(True),
 debugOn = cms.untracked.bool(False),
 numtrack = cms.untracked.uint32(10),
 thresh = cms.untracked.double(0.25)
)

process.eventSelection = cms.Sequence(
        process.hfCoincFilter3
        + process.primaryVertexFilter
	+ process.NoScraping
#        + process.clusterCompatibilityFilter
)

process.load('PbPb_HIMB5_ppReco_eff')
process.QWEvent.fweight = cms.untracked.InputTag('Hydjet_ppReco_v5_loose.root')
process.QWEvent.dzdzerror = cms.untracked.double(5.0)
process.QWEvent.d0d0error = cms.untracked.double(5.0)
process.QWEvent.pterrorpt = cms.untracked.double(0.1)

process.dbNoff = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('Noff'),
		)

process.cutHF = cms.EDFilter('QWHFNoffFilter',
		srcHF = cms.untracked.InputTag('centralityBins', 'etHFtowerSum'),
		srcNoff = cms.untracked.InputTag('dbNoff'),
		curve = cms.untracked.InputTag('0.001 * x * x')
		)

process.monHFsumEtVsNoff = cms.EDAnalyzer('QWCorrAnalyzer',
                srcX = cms.untracked.InputTag('centralityBins', "etHFtowerSum"),
                NbinsX = cms.untracked.int32(2500),
                hstartX = cms.untracked.double(0.),
                hendX = cms.untracked.double(2500.),
                srcY = cms.untracked.InputTag('dbNoff'),
                NbinsY = cms.untracked.int32(1000),
                hstartY = cms.untracked.double(0.),
                hendY = cms.untracked.double(1000.),
                )

process.ana = cms.Path( process.eventSelection * process.makeEvent * process.dbNoff * process.cutHF * process.cumugap * process.monHFsumEtVsNoff * process.vectMonW )

process.schedule = cms.Schedule(
	process.ana,
)
