import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuGap")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
#process.MessageLogger.cerr.FwkReport.reportEvery = 100

#from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/XeXe_MB_AOD.root")
)


import HLTrigger.HLTfilters.hltHighLevel_cfi

process.hltMB = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltMB.HLTPaths = [
	"HLT_HIL1MinimumBiasHF_OR_SinglePixelTrack_part*"
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

process.eventSelection = cms.Sequence(
        process.hfCoincFilter3
        + process.primaryVertexFilter
#        + process.clusterCompatibilityFilter
)

process.QWEvent = cms.EDProducer("QWEventProducer"
		, vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices', "")
		, trackSrc = cms.untracked.InputTag('generalTracks')
		, fweight = cms.untracked.InputTag('Hydjet_eff_mult_v1.root')
                , centralitySrc = cms.untracked.InputTag("Noff")
		, dzdzerror = cms.untracked.double(3.0)
		, d0d0error = cms.untracked.double(3.0)
		, pterrorpt = cms.untracked.double(0.1)
		, ptMin = cms.untracked.double(0.3)
		, ptMax= cms.untracked.double(3.0)
		, Etamin = cms.untracked.double(-2.4)
		, Etamax = cms.untracked.double(2.4)
                )

process.QWEvent.fweight = cms.untracked.InputTag('NA')


process.Noff = cms.EDProducer("QWNtrkOfflineProducer",
		vertexSrc = cms.untracked.InputTag("offlinePrimaryVertices"),
		trackSrc  = cms.untracked.InputTag("generalTracks")
		)

# monitoring
process.histNoff = cms.EDAnalyzer('QWHistAnalyzer',
		src = cms.untracked.InputTag("Noff"),
		Nbins = cms.untracked.int32(5000),
		start = cms.untracked.double(0),
		end = cms.untracked.double(5000),
		)


process.vectPhi = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag("QWEvent", "phi"),
		hNbins = cms.untracked.int32(5000),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(5000),
		cNbins = cms.untracked.int32(1000),
		cstart = cms.untracked.double(-3.14159265358979323846),
		cend = cms.untracked.double(3.14159265358979323846),
		)

process.vectPt = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag("QWEvent", "pt"),
		hNbins = cms.untracked.int32(5000),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(5000),
		cNbins = cms.untracked.int32(1000),
		cstart = cms.untracked.double(0),
		cend = cms.untracked.double(5),
		)

process.vectEta = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag("QWEvent", "eta"),
		hNbins = cms.untracked.int32(5000),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(5000),
		cNbins = cms.untracked.int32(1000),
		cstart = cms.untracked.double(-2.5),
		cend = cms.untracked.double(2.5),
		)

process.corr2D = cms.EDAnalyzer('QWVCorrAnalyzer',
		srcX = cms.untracked.InputTag('QWEvent', 'eta'),
		NbinsX = cms.untracked.int32(48),
		hstartX = cms.untracked.double(-2.4),
		hendX = cms.untracked.double(2.4),
		srcY = cms.untracked.InputTag('QWEvent', 'phi'),
		NbinsY = cms.untracked.int32(48),
		hstartY = cms.untracked.double(-3.14159265358979323846),
		hendY = cms.untracked.double(3.14159265358979323846),
		)

process.vectMon = cms.Sequence(process.histNoff * process.vectPhi * process.vectPt * process.vectEta * process.corr2D)
#process.vectMon = cms.Sequence(process.histNoff * process.vectPhi * process.vectPt * process.vectEta )

process.ana = cms.Path(process.eventSelection*process.Noff*process.QWEvent*process.cumugap * process.vectMon )

process.RECO = cms.OutputModule("PoolOutputModule",
		outputCommands = cms.untracked.vstring('keep *'),
		SelectEvents = cms.untracked.PSet(
			SelectEvents = cms.vstring('ana')
			),
		fileName = cms.untracked.string('reco.root')
		)

process.out = cms.EndPath(process.RECO)

process.schedule = cms.Schedule(
	process.ana,
)
