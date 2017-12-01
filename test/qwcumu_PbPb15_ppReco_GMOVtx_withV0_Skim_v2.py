import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuGap")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
#process.MessageLogger.cerr.FwkReport.reportEvery = 100
#process.MessageLogger.suppressWarning = cms.untracked.vstring('GMOVertex')

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '75X_dataRun2_PromptHI_v3', '')

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/ppReco.root")
)

## new vtx collection
process.load("RecoVertex.Configuration.RecoVertex_cff")
process.GMOVertex = process.unsortedOfflinePrimaryVertices.clone(
  TkFilterParameters = cms.PSet(
        algorithm=cms.string('filter'),
        maxNormalizedChi2 = cms.double(20.0),
        minPixelLayersWithHits=cms.int32(2),
        minSiliconLayersWithHits = cms.int32(5),
        maxD0Significance = cms.double(5.0), # 3.0 -> 5.0
        minPt = cms.double(0.0),
        trackQuality = cms.string("any")
    ),
    TkClusParameters = cms.PSet(
        algorithm   = cms.string("gap"),
        TkGapClusParameters = cms.PSet(
            zSeparation = cms.double(1.0)
        )
    ),
    vertexCollections = cms.VPSet(cms.PSet(
        algorithm = cms.string('AdaptiveVertexFitter'),
        label = cms.string(''),
        maxDistanceToBeam = cms.double(1.0),
        minNdof = cms.double(0.0),
        useBeamConstraint = cms.bool(False)
    )
    )
)

from RecoVertex.V0Producer.generalV0Candidates_cff import *

process.generalV0CandidatesNew = process.generalV0Candidates.clone (
	tkNhitsCut = cms.int32(3),
	tkChi2Cut = cms.double(7.0),
	dauTransImpactSigCut = cms.double(1.0),
	dauLongImpactSigCut = cms.double(1.0),
	vtxSignificance2DCut = cms.double(0.0),
	vtxSignificance3DCut = cms.double(2.5),
	collinearityCut = cms.double(0.997),
	vertices = cms.InputTag('GMOVertex')
)


process.GMONoff = cms.EDProducer("QWNtrkOfflineProducer",
                vertexSrc = cms.untracked.InputTag("GMOVertex"),
                trackSrc  = cms.untracked.InputTag("generalTracks")
                )



process.RECO = cms.OutputModule("PoolOutputModule",
		outputCommands = cms.untracked.vstring(
			'keep *_GMOVertex_*_*',
			'keep *_generalV0CandidatesNew_*_*'
			),
		SelectEvents = cms.untracked.PSet(
			SelectEvents = cms.vstring('ana')
			),
		fileName = cms.untracked.string('reco.root')
		)

#process.TFileService = cms.Service("TFileService",
#    fileName = cms.string('cumu.root')
#)

process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')

process.ana = cms.Path(
		process.GMOVertex *
		process.generalV0CandidatesNew
		)

process.out = cms.EndPath(process.RECO)

process.schedule = cms.Schedule(
	process.ana,
	process.out
)
