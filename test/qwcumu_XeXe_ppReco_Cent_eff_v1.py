import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuGap")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
process.GlobalTag.toGet.extend([
   cms.PSet(record = cms.string("HeavyIonRcd"),
      tag = cms.string("CentralityTable_HFtowers200_DataXeXe_eff942_run2v9313x02_offline"),
      connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
      label = cms.untracked.string("HFtowersCymbal5Ev8")
   ),
])

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


process.primaryVertexFilter = cms.EDFilter("VertexSelector",
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
process.hfPosFilter2 = process.hfPosFilter.clone(minNumber=cms.uint32(2))
process.hfNegFilter2 = process.hfNegFilter.clone(minNumber=cms.uint32(2))
process.hfCoincFilter2 = cms.Sequence(
    process.towersAboveThreshold 
    + process.hfPosTowers 
    + process.hfNegTowers 
    + process.hfPosFilter2 
    + process.hfNegFilter2
)

process.eventSelection = cms.Sequence(
        process.hfCoincFilter2
        + process.primaryVertexFilter
        + process.NoScraping
)

process.QWEvent = cms.EDProducer("QWEventProducer"
		, vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices', "")
		, trackSrc = cms.untracked.InputTag('generalTracks')
		, fweight = cms.untracked.InputTag('XeXe_eff_table_92x_cent.root')
                , centralitySrc = cms.untracked.InputTag("centralityBin", 'HFtowers')
		, dzdzerror = cms.untracked.double(3.0)
		, d0d0error = cms.untracked.double(3.0)
		, pterrorpt = cms.untracked.double(0.1)
		, ptMin = cms.untracked.double(0.3)
		, ptMax= cms.untracked.double(3.0)
		, Etamin = cms.untracked.double(-2.4)
		, Etamax = cms.untracked.double(2.4)
                )


process.QWVtxSize = cms.EDProducer('QWVectCounter',
                src = cms.untracked.InputTag("QWEvent", "vz")
		)

process.histVtxSize = cms.EDAnalyzer('QWHistAnalyzer',
                src = cms.untracked.InputTag("QWVtxSize"),
                Nbins = cms.untracked.int32(50),
                start = cms.untracked.double(0),
                end = cms.untracked.double(50),
                )

process.load('RecoHI.HiCentralityAlgos.HiCentrality_cfi')
process.hiCentrality.produceHFhits = False
process.hiCentrality.produceHFtowers = True
process.hiCentrality.produceEcalhits = False
process.hiCentrality.produceZDChits = False
process.hiCentrality.produceETmidRapidity = True
process.hiCentrality.producePixelhits = False
process.hiCentrality.produceTracks = True
process.hiCentrality.producePixelTracks = False
process.hiCentrality.reUseCentrality = False
process.hiCentrality.srcTracks = cms.InputTag("generalTracks")
process.hiCentrality.srcVertex = cms.InputTag("offlinePrimaryVertices")

process.QWCent = cms.EDProducer('QWCentralityProducer',
                src = cms.untracked.InputTag("hiCentrality")
		)


process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")
process.centralityBin.nonDefaultGlauberModel = cms.string("Cymbal5Ev8")


process.Noff = cms.EDProducer("QWNtrkOfflineProducer",
		vertexSrc = cms.untracked.InputTag("offlinePrimaryVertices"),
		trackSrc  = cms.untracked.InputTag("generalTracks")
		)

process.dbCent = cms.EDProducer('QWInt2Double',
                src = cms.untracked.InputTag('centralityBin', "HFtowers")
                )

process.dbNoff = cms.EDProducer('QWInt2Double',
                src = cms.untracked.InputTag('Noff')
                )

# monitoring
process.histCent = cms.EDAnalyzer('QWHistAnalyzer',
		src = cms.untracked.InputTag("centralityBin", 'HFtowers'),
		Nbins = cms.untracked.int32(200),
		start = cms.untracked.double(0),
		end = cms.untracked.double(200),
		)


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

process.PhiEta2D = cms.EDAnalyzer('QWVCorrAnalyzer',
		srcX = cms.untracked.InputTag('QWEvent', 'eta'),
		NbinsX = cms.untracked.int32(48),
		hstartX = cms.untracked.double(-2.4),
		hendX = cms.untracked.double(2.4),
		srcY = cms.untracked.InputTag('QWEvent', 'phi'),
		NbinsY = cms.untracked.int32(48),
		hstartY = cms.untracked.double(-3.14159265358979323846),
		hendY = cms.untracked.double(3.14159265358979323846),
		)

#process.NoffCent2D = cms.EDAnalyzer('QWCorrAnalyzer',
#		srcX = cms.untracked.InputTag('dbNoff'),
#		NbinsX = cms.untracked.int32(5000),
#		hstartX = cms.untracked.double(0),
#		hendX = cms.untracked.double(5000),
#		srcY = cms.untracked.InputTag('dbCent'),
#		NbinsY = cms.untracked.int32(200),
#		hstartY = cms.untracked.double(0),
#		hendY = cms.untracked.double(200),
#		)

process.monHFsumEtVsNoff = cms.EDAnalyzer('QWCorrAnalyzer',
                srcX = cms.untracked.InputTag('QWCent', "EtHFtowerSum"),
                NbinsX = cms.untracked.int32(2500),
                hstartX = cms.untracked.double(0.),
                hendX = cms.untracked.double(2500.),
                srcY = cms.untracked.InputTag('dbNoff'),
                NbinsY = cms.untracked.int32(1000),
                hstartY = cms.untracked.double(0.),
                hendY = cms.untracked.double(1000.),
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

process.vectMon = cms.Sequence(process.histCent * process.histVtxSize * process.histNoff * process.vectPhi * process.vectPt * process.vectEta * process.PhiEta2D )

process.ana = cms.Path(process.hltMB *
		process.eventSelection *
		process.hiCentrality *
		process.centralityBin *
		process.QWCent *
		process.Noff *
		process.dbNoff *
		process.dbCent *
		process.QWEvent *
		process.QWVtxSize *
		process.cumugap *
		process.monHFsumEtVsNoff *
		process.monCentVsNoff *
		process.vectMon )

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
