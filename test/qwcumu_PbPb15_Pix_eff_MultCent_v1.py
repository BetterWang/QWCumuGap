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
	"HLT_HIL1Centralityext30100MinimumumBiasHF*"
]
process.hltMB.andOr = cms.bool(True)
process.hltMB.throw = cms.bool(False)


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


process.eventSelection_cluster = cms.Sequence(
	~process.clusterCompatibilityFilter
)

process.QWEvent = cms.EDProducer("QWEventProducer"
		, vertexSrc = cms.untracked.InputTag('hiSelectedVertex', "")
		, trackSrc = cms.untracked.InputTag('hiGeneralTracks')
		, fweight = cms.untracked.InputTag('NA')
                , centralitySrc = cms.untracked.InputTag("centralityBin", "HFtowers")
		, dzdzerror = cms.untracked.double(3.0)
		, d0d0error = cms.untracked.double(3.0)
		, pterrorpt = cms.untracked.double(0.1)
		, ptMin = cms.untracked.double(0.3)
		, ptMax= cms.untracked.double(3.0)
		, Etamin = cms.untracked.double(-2.4)
		, Etamax = cms.untracked.double(2.4)
                )

process.Mult = cms.EDProducer("QWVectCounter",
                src = cms.untracked.InputTag("QWEvent", "phi")
                )

process.dbMult = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('Mult'),
		)

process.dbCent = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('centralityBin', "HFtowers")
		)

process.QWCent = cms.EDProducer('QWCentralityProducer',
		src = cms.untracked.InputTag('hiCentrality')
		)

process.monHFsumEtVsMult = cms.EDAnalyzer('QWCorrAnalyzer',
                srcX = cms.untracked.InputTag('QWCent', "EtHFtowerSum"),
                NbinsX = cms.untracked.int32(2500),
                hstartX = cms.untracked.double(0.),
                hendX = cms.untracked.double(2500.),
                srcY = cms.untracked.InputTag('dbMult'),
                NbinsY = cms.untracked.int32(1000),
                hstartY = cms.untracked.double(0.),
                hendY = cms.untracked.double(1000.),
                )

process.monHFsumEtVsMult_cluster = process.monHFsumEtVsMult.clone()

process.ana = cms.Path(process.hltMB * process.eventSelection * process.QWEvent * process.QWCent * process.Mult * process.dbMult * process.dbCent * process.monHFsumEtVsMult)
process.ana_cluster = cms.Path(process.hltMB * process.eventSelection_cluster * process.QWEvent * process.QWCent * process.Mult * process.dbMult * process.dbCent * process.monHFsumEtVsMult_cluster)

process.schedule = cms.Schedule(
	process.ana,
	process.ana_cluster,
)
