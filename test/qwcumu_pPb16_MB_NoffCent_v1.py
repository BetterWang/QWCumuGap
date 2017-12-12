import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuV3")

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
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/pPb_8_FEVT.root")
)

import HLTrigger.HLTfilters.hltHighLevel_cfi
process.hltMB = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltMB.HLTPaths = [
	"HLT_PAL1MinimumBiasHF_OR_SinglePixelTrack_part*",
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



process.load("HeavyIonsAnalysis.VertexAnalysis.PAPileUpVertexFilter_cff")

process.PAprimaryVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2 && tracksSize >= 2"),
    filter = cms.bool(True), # otherwise it won't filter the events
)

process.NoScraping = cms.EDFilter("FilterOutScraping",
 applyfilter = cms.untracked.bool(True),
 debugOn = cms.untracked.bool(False),
 numtrack = cms.untracked.uint32(10),
 thresh = cms.untracked.double(0.25)
)

process.load("HeavyIonsAnalysis.Configuration.hfCoincFilter_cff")
process.load("HeavyIonsAnalysis.EventAnalysis.pileUpFilter_cff")

process.eventSelection = cms.Sequence(process.hfCoincFilter * process.PAprimaryVertexFilter * process.NoScraping * process.olvFilter_pPb8TeV_dz1p0)
process.eventSelection_Scrapping = cms.Sequence(process.hfCoincFilter * process.PAprimaryVertexFilter * ~process.NoScraping * process.olvFilter_pPb8TeV_dz1p0)
process.eventSelection_PU = cms.Sequence(process.hfCoincFilter * process.PAprimaryVertexFilter * ~process.NoScraping * ~process.olvFilter_pPb8TeV_dz1p0)


process.load('pPb_HM_eff')
process.QWEvent.fweight = cms.untracked.InputTag('Hijing_8TeV_dataBS.root')


process.centralityBins = cms.EDProducer("QWPPRecoCentBinProducer")

process.dbNoff = cms.EDProducer('QWInt2Double',
                src = cms.untracked.InputTag('Noff'),
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

process.monHFsumEtVsNoff_Scrapping = process.monHFsumEtVsNoff.clone()
process.monHFsumEtVsNoff_PU = process.monHFsumEtVsNoff.clone()

#process.ana = cms.Path(process.hltMB*process.eventSelection*process.Noff* process.centralityBins * process.dbNoff )

process.ana = cms.Path(process.hltMB*process.eventSelection*process.Noff* process.centralityBins * process.dbNoff * process.monHFsumEtVsNoff)
process.ana_Scrapping = cms.Path(process.hltMB*process.eventSelection_Scrapping*process.Noff* process.centralityBins * process.dbNoff * process.monHFsumEtVsNoff_Scrapping)
process.ana_PU = cms.Path(process.hltMB*process.eventSelection_PU*process.Noff* process.centralityBins * process.dbNoff * process.monHFsumEtVsNoff_PU)

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
	process.ana_Scrapping,
	process.ana_PU,
#	process.out
)
