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
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/pp_TOTEM_HM.root")
)

import HLTrigger.HLTfilters.hltHighLevel_cfi

process.hltHM60 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM60.HLTPaths = [
	"HLT_PixelTracks_Multiplicity60_v*"
#	"HLT_PixelTracks_Multiplicity60*_v*"
]
process.hltHM60.andOr = cms.bool(True)
process.hltHM60.throw = cms.bool(False)

process.hltHM85 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM85.HLTPaths = [
	"HLT_PixelTracks_Multiplicity60_v*",
	"HLT_PixelTracks_Multiplicity85_v*"
#        "HLT_PixelTracks_Multiplicity85*_v*"
]
process.hltHM85.andOr = cms.bool(True)
process.hltHM85.throw = cms.bool(False)

process.hltHM135 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM135.HLTPaths = [
	"HLT_PixelTracks_Multiplicity60_v*",
	"HLT_PixelTracks_Multiplicity85_v*",
	"HLT_PixelTracks_Multiplicity110_v*",
	"HLT_PixelTracks_Multiplicity135_v*"
#        "HLT_PixelTracks_Multiplicity110*_v*"
]
process.hltHM135.andOr = cms.bool(True)
process.hltHM135.throw = cms.bool(False)

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


process.load('ppPileupFilter.PPPileUpVertexFilter.PPPileUpVertexFilter_cff')

process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
process.ppNoffFilter60 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(60, 105)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.ppNoffFilter85 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(105, 130)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.ppNoffFilter135 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(130, 500)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.load('pPb_HM_eff')
process.QWEvent.fweight = cms.untracked.InputTag('trkEff_pp_all_74X_origin.root')
process.QWEvent.ptMin = cms.untracked.double(0.3)
process.QWEvent.ptMax = cms.untracked.double(10)

process.vectPhi60 = process.vectPhi.clone()
process.vectPhi85 = process.vectPhi.clone()
process.vectPhi135 = process.vectPhi.clone()

process.vectPhiW60 = process.vectPhiW.clone()
process.vectPhiW85 = process.vectPhiW.clone()
process.vectPhiW135 = process.vectPhiW.clone()

process.vectEta60 = process.vectEta.clone()
process.vectEta85 = process.vectEta.clone()
process.vectEta135 = process.vectEta.clone()

process.vectEtaW60 = process.vectEtaW.clone()
process.vectEtaW85 = process.vectEtaW.clone()
process.vectEtaW135 = process.vectEtaW.clone()

process.vectPt60 = process.vectPt.clone()
process.vectPt85 = process.vectPt.clone()
process.vectPt135 = process.vectPt.clone()

process.vectPtW60 = process.vectPtW.clone()
process.vectPtW85 = process.vectPtW.clone()
process.vectPtW135 = process.vectPtW.clone()

process.mon60 = cms.Sequence(process.histNoff + process.vectPhi60 + process.vectPt60 + process.vectEta60 + process.vectPhiW60 + process.vectPtW60 + process.vectEtaW60)
process.mon85 = cms.Sequence(process.histNoff + process.vectPhi85 + process.vectPt85 + process.vectEta85 + process.vectPhiW85 + process.vectPtW85 + process.vectEtaW85)
process.mon135 = cms.Sequence(process.histNoff + process.vectPhi135 + process.vectPt135 + process.vectEta135 + process.vectPhiW135 + process.vectPtW135 + process.vectEtaW135)

process.ana60 = cms.Path(process.hltHM60*process.Noff*process.ppNoffFilter60*process.QWEvent*process.cumugap* process.mon60)
process.ana85 = cms.Path(process.hltHM85*process.Noff*process.ppNoffFilter85*process.QWEvent*process.cumugap* process.mon85)
process.ana135 = cms.Path(process.hltHM135*process.Noff*process.ppNoffFilter135*process.QWEvent*process.cumugap* process.mon135)

process.schedule = cms.Schedule(
	process.ana60,
	process.ana85,
	process.ana135,
)

