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
process.MessageLogger.suppressWarning = cms.untracked.vstring('GMOVertex')

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '75X_dataRun2_PromptHI_v3', '')

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
	, trackEta = cms.untracked.InputTag('QWGMOEvent', "eta")
	, trackPhi = cms.untracked.InputTag('QWGMOEvent', "phi")
	, trackPt = cms.untracked.InputTag('QWGMOEvent', "pt")
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

#process.primaryVertexFilter.src = cms.InputTag("offlinePrimaryVertices")
process.primaryVertexFilter.src = cms.InputTag("GMOVertex")

process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
process.ppRecoCentFilter = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(60, 180)
		),
	BinLabel = cms.InputTag("centralityBins")
	)

process.eventSelection = cms.Sequence(
        process.hfCoincFilter3
        + process.primaryVertexFilter
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

process.monHFsumEtVsGMONoff = process.monHFsumEtVsNoff.clone(
		srcY = cms.untracked.InputTag('dbGMONoff'),
		)

process.monGMONoffVsNoff = cms.EDAnalyzer('QWCorrAnalyzer',
                srcX = cms.untracked.InputTag('dbGMONoff'),
                NbinsX = cms.untracked.int32(1000),
                hstartX = cms.untracked.double(0.),
                hendX = cms.untracked.double(1000.),
                srcY = cms.untracked.InputTag('dbNoff'),
                NbinsY = cms.untracked.int32(1000),
                hstartY = cms.untracked.double(0.),
                hendY = cms.untracked.double(1000.),
                )

## new vtx collection

process.load("RecoVertex.Configuration.RecoVertex_cff")
process.GMOVertex = process.unsortedOfflinePrimaryVertices.clone(
  TkFilterParameters = cms.PSet(
        algorithm=cms.string('filter'),
        maxNormalizedChi2 = cms.double(20.0),
        minPixelLayersWithHits=cms.int32(2),
        minSiliconLayersWithHits = cms.int32(5),
        maxD0Significance = cms.double(3.0),
        minPt = cms.double(0.0),
        trackQuality = cms.string("any")
    ),
    TkClusParameters = cms.PSet(
        algorithm   = cms.string("gap"),
        TkGapClusParameters = cms.PSet(
            zSeparation = cms.double(1.0)
        )
    ),
)

process.GMONoff = cms.EDProducer("QWNtrkOfflineProducer",
                vertexSrc = cms.untracked.InputTag("GMOVertex"),
                trackSrc  = cms.untracked.InputTag("generalTracks")
                )

process.QWGMOEvent = process.QWEvent.clone(
		vertexSrc = cms.untracked.InputTag('GMOVertex')
		)


process.dbGMONoff = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('GMONoff'),
		)


process.makeGMOEvent = cms.Sequence( process.GMONoff * process.QWGMOEvent * process.dbGMONoff )

process.makeEvent = cms.Sequence(process.centralityBins * process.Noff * process.QWEvent * process.dbNoff)

process.histGMONoff = process.histNoff.clone(
		src = cms.untracked.InputTag("GMONoff"),
		)

process.vectGMOPhi = process.vectPhi.clone(
		src = cms.untracked.InputTag("QWGMOEvent", "phi"),
		)

process.vectGMOEta = process.vectEta.clone(
		src = cms.untracked.InputTag("QWGMOEvent", "eta"),
		)

process.vectGMOPt = process.vectPt.clone(
		src = cms.untracked.InputTag("QWGMOEvent", "pt"),
		)

process.vectGMOPhiW = process.vectGMOPhi.clone(
		srcW = cms.untracked.InputTag("QWGMOEvent", "weight")
		)

process.vectGMOEtaW = process.vectGMOEta.clone(
		srcW = cms.untracked.InputTag("QWGMOEvent", "weight")
		)

process.vectGMOPtW = process.vectGMOPt.clone(
		srcW = cms.untracked.InputTag("QWGMOEvent", "weight")
		)

process.vectGMOMonW = cms.Sequence( process.histGMONoff *
		process.vectGMOPhi *
		process.vectGMOEta *
		process.vectGMOPt *
		process.vectGMOPhiW *
		process.vectGMOEtaW *
		process.vectGMOPtW )


#process.ana = cms.Path(process.eventSelection*process.makeEvent*process.ppRecoCentFilter*process.cumugap * process.vectMonW )
process.ana = cms.Path(
		process.GMOVertex *
		process.eventSelection *
		process.makeEvent *
		process.makeGMOEvent *
		process.cumugap *
		process.monHFsumEtVsNoff *
		process.monHFsumEtVsGMONoff *
		process.monGMONoffVsNoff *
		process.histGMONoff *
		process.vectGMOMonW *
		process.vectMonW )

process.schedule = cms.Schedule(
	process.ana,
)
