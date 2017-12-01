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


process.QWEvent = cms.EDProducer("QWEventProducer"
		, vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices')
		, trackSrc = cms.untracked.InputTag('generalTracks')
		, fweight = cms.untracked.InputTag('Hydjet_PbPb_eff_v1.root')
                , centralitySrc = cms.untracked.InputTag("Noff")
		, dzdzerror = cms.untracked.double(3.0)
		, d0d0error = cms.untracked.double(3.0)
		, pterrorpt = cms.untracked.double(0.1)
		, ptMin = cms.untracked.double(0.3)
		, ptMax= cms.untracked.double(3.0)
		, Etamin = cms.untracked.double(-2.4)
		, Etamax = cms.untracked.double(2.4)
                )

process.QWGMOEvent = process.QWEvent.clone(
		vertexSrc = cms.untracked.InputTag('GMOVertex'),
                centralitySrc = cms.untracked.InputTag("GMONoff")
		)

process.QWEventloose = process.QWEvent.clone(
		fweight = cms.untracked.InputTag('Hydjet_ppReco_v5_loose.root'),
		dzdzerror = cms.untracked.double(5.0),
		d0d0error = cms.untracked.double(5.0)
		)

process.QWGMOEventloose = process.QWGMOEvent.clone(
		fweight = cms.untracked.InputTag('Hydjet_ppReco_v5_loose.root'),
		dzdzerror = cms.untracked.double(5.0),
		d0d0error = cms.untracked.double(5.0)
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

process.histNChi2 = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag('QWEvent', 'Nchi2'),
		hNbins = cms.untracked.int32(1000),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(1000),
		cNbins = cms.untracked.int32(500),
		cstart = cms.untracked.double(0),
		cend = cms.untracked.double(50),
		)

process.histNChi2loose = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag('QWEventloose', 'Nchi2'),
		hNbins = cms.untracked.int32(1000),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(1000),
		cNbins = cms.untracked.int32(500),
		cstart = cms.untracked.double(0),
		cend = cms.untracked.double(50),
		)

process.histGMONChi2 = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag('QWGMOEvent', 'Nchi2'),
		hNbins = cms.untracked.int32(1000),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(1000),
		cNbins = cms.untracked.int32(500),
		cstart = cms.untracked.double(0),
		cend = cms.untracked.double(50),
		)

process.histGMONChi2loose = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag('QWGMOEventloose', 'Nchi2'),
		hNbins = cms.untracked.int32(1000),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(1000),
		cNbins = cms.untracked.int32(500),
		cstart = cms.untracked.double(0),
		cend = cms.untracked.double(50),
		)

process.histNChi2oNLayers = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag('QWEvent', 'Nchi2oNLayers'),
		hNbins = cms.untracked.int32(1000),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(1000),
		cNbins = cms.untracked.int32(500),
		cstart = cms.untracked.double(0),
		cend = cms.untracked.double(50),
		)

process.histNChi2oNLayersloose = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag('QWEventloose', 'Nchi2oNLayers'),
		hNbins = cms.untracked.int32(1000),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(1000),
		cNbins = cms.untracked.int32(500),
		cstart = cms.untracked.double(0),
		cend = cms.untracked.double(50),
		)

process.histGMONChi2oNLayers = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag('QWGMOEvent', 'Nchi2oNLayers'),
		hNbins = cms.untracked.int32(1000),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(1000),
		cNbins = cms.untracked.int32(500),
		cstart = cms.untracked.double(0),
		cend = cms.untracked.double(50),
		)

process.histGMONChi2oNLayersloose = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag('QWGMOEventloose', 'Nchi2oNLayers'),
		hNbins = cms.untracked.int32(1000),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(1000),
		cNbins = cms.untracked.int32(500),
		cstart = cms.untracked.double(0),
		cend = cms.untracked.double(50),
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

process.RECO = cms.OutputModule("PoolOutputModule",
		outputCommands = cms.untracked.vstring('keep *_GMOVertex_*_*'),
		SelectEvents = cms.untracked.PSet(
			SelectEvents = cms.vstring('ana')
			),
		fileName = cms.untracked.string('reco.root')
		)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('cumu.root')
)

process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')

process.ana = cms.Path(
		process.GMOVertex
		)

process.ana_p = cms.Path(
		process.hfCoincFilter3 *
		process.GMOVertex *
		process.Noff *
		process.dbNoff *
		process.GMONoff *
		process.dbGMONoff *
		process.QWEvent *
		process.QWGMOEvent *
		process.QWEventloose *
		process.QWGMOEventloose *
		process.QWOfflineVtx *
		process.QWGMOVtx *
		process.histVtxSize *
		process.histGMOVtxSize *
		process.histNChi2 *
		process.histNChi2loose *
		process.histGMONChi2 *
		process.histGMONChi2loose *
		process.histNChi2oNLayers *
		process.histNChi2oNLayersloose *
		process.histGMONChi2oNLayers *
		process.histGMONChi2oNLayersloose *
		process.monGMONoffVsNoff
		)

process.out = cms.EndPath(process.RECO)

process.schedule = cms.Schedule(
	process.ana,
	process.ana_p,
	process.out
)
