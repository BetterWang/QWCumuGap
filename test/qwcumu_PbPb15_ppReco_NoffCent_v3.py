import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuDiff")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

#from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '75X_dataRun2_v13', '')

#process.options = cms.untracked.PSet(
#    SkipEvent = cms.untracked.vstring('ProductNotFound')
#)

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

process.TFileService = cms.Service("TFileService",
	fileName = cms.string('noff.root')
)


process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')

process.primaryVertexFilter.src = cms.InputTag("offlinePrimaryVertices")

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


process.centralityBins = cms.EDProducer("QWPPRecoCentBinProducer")
process.Noff = cms.EDProducer("QWNtrkOfflineProducer",
                vertexSrc = cms.untracked.InputTag("offlinePrimaryVertices"),
                trackSrc  = cms.untracked.InputTag("generalTracks")
                )

process.dbNoff = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('Noff'),
		)

process.dbCent = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('centralityBins'),
		)

process.monCentVsNoff = cms.EDAnalyzer('QWCorrAnalyzer',
                srcX = cms.untracked.InputTag('dbCent'),
                NbinsX = cms.untracked.int32(200),
                hstartX = cms.untracked.double(0.),
                hendX = cms.untracked.double(200.),
                srcY = cms.untracked.InputTag('dbNoff'),
                NbinsY = cms.untracked.int32(1000),
                hstartY = cms.untracked.double(0.),
                hendY = cms.untracked.double(1000.),
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

process.ana = cms.Path(process.eventSelection * process.centralityBins * process.Noff * process.dbNoff * process.dbCent * process.monCentVsNoff * process.monHFsumEtVsNoff)

process.RECO = cms.OutputModule("PoolOutputModule",
		outputCommands = cms.untracked.vstring('keep *'),
		SelectEvents = cms.untracked.PSet(
			SelectEvents = cms.vstring('ana')
			),
		fileName = cms.untracked.string('recoV0.root')
		)

process.out = cms.EndPath(process.RECO)


process.schedule = cms.Schedule(
	process.ana,
)
