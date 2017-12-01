import FWCore.ParameterSet.Config as cms

process = cms.Process("vtx")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '75X_dataRun2_PromptHI_v3', '')

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring("file:reco.root"),
#        secondaryFileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/ppReco.root")
)


process.Noff = cms.EDProducer("QWNtrkOfflineProducer",
                vertexSrc = cms.untracked.InputTag("offlinePrimaryVertices"),
                trackSrc  = cms.untracked.InputTag("generalTracks")
                )
process.dbNoff = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('Noff'),
		)

process.GMONoff = cms.EDProducer("QWNtrkOfflineProducer",
                vertexSrc = cms.untracked.InputTag("GMOVertex"),
                trackSrc  = cms.untracked.InputTag("generalTracks")
                )
process.dbGMONoff = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('GMONoff'),
		)


process.QWOfflineVtx = cms.EDProducer('QWVertexProducer',
		vertexSrc = cms.untracked.InputTag("offlinePrimaryVertices")
		)

process.QWGMOVtx = cms.EDProducer('QWVertexProducer',
		vertexSrc = cms.untracked.InputTag("GMOVertex")
		)

process.histVtxSize = cms.EDAnalyzer('QWHistAnalyzer',
		src = cms.untracked.InputTag("QWOfflineVtx", "size"),
		Nbins = cms.untracked.int32(50),
		start = cms.untracked.double(0),
		end = cms.untracked.double(50),
		)

process.histGMOVtxSize = process.histVtxSize.clone(
		src = cms.untracked.InputTag("QWGMOVtx", "size"),
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

process.cut = cms.EDFilter('QWHFNoffFilter',
		srcHF = cms.untracked.InputTag('dbGMONoff'),
		srcNoff = cms.untracked.InputTag('dbNoff'),
		curve = cms.untracked.InputTag('x+100')
		)

process.RECO = cms.OutputModule("PoolOutputModule",
		outputCommands = cms.untracked.vstring('keep *',
			'drop *_dbNoff_*_*',
			'drop *_dbGMONoff_*_*',
			'drop *_TriggerResults_*_*',
			'drop *_hfNegTowers_*_*',
			'drop *_hfPosTowers_*_*',
			'drop *_towersAboveThreshold_*_*',
			'drop *_QWGMOVtx_*_*',
			'drop *_QWOfflineVtx_*_*',
			),
		SelectEvents = cms.untracked.PSet(
			SelectEvents = cms.vstring('ana')
			),
		fileName = cms.untracked.string('recoskim.root')
		)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('cumu.root')
)

process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')

process.ana = cms.Path(
		process.hfCoincFilter3 *
		process.Noff *
		process.dbNoff *
		process.GMONoff *
		process.dbGMONoff *
		process.cut
		)

process.ana_p = cms.Path(
		process.hfCoincFilter3 *
		process.Noff *
		process.dbNoff *
		process.GMONoff *
		process.dbGMONoff *
		process.cut *
		process.QWOfflineVtx *
		process.QWGMOVtx *
		process.histVtxSize *
		process.histGMOVtxSize *
		process.monGMONoffVsNoff
		)

process.out = cms.EndPath(process.RECO)

process.schedule = cms.Schedule(
	process.ana,
	process.ana_p,
	process.out
)
