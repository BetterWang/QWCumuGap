import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuGap")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

#from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '75X_dataRun2_v12', '')

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

flist = cms.untracked.vstring(
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_1.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_10.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_100.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_101.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_102.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_103.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_104.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_105.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_106.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_107.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_108.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_109.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_11.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_110.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_111.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_112.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_113.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_114.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_115.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_116.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_117.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_118.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_119.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_12.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_120.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_121.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_122.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_123.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_124.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_125.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_126.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_127.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_128.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_129.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_13.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_130.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_131.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_132.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_133.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_134.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_135.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_136.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_137.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_138.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_139.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_14.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_140.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_141.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_142.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_143.root",
"root://cms-xrd-global.cern.ch//store/user/davidlw/Hydjet_Quenched_MinBias_5020GeV_750/ppRECO_std_v3/160216_232421/0000/step2pp_RAW2DIGI_L1Reco_RECO_144.root",
)

process.source = cms.Source("PoolSource",
        fileNames = flist
#        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/Hydjet_PbPb_ppreco_RECODEBUG.root")
)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('cumuMC.root')
)


process.QWTrack = cms.EDProducer('QWTrackProducer'
		, vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices', "")
		, trackSrc = cms.untracked.InputTag('generalTracks')
		)

process.QWTreeMaker = cms.EDAnalyzer('QWTreeMaker',
		src = cms.untracked.InputTag('QWTrack'),
		vTag = cms.untracked.vstring('phi', 'eta', 'pt', 'charge', 'pterr', 'pd0', 'pdz', 'pd0err', 'pdzerr', 'nhits', 'algo', 'nChi2'),
		)

process.ana = cms.Path(process.QWTrack * process.QWTreeMaker)

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = cms.untracked.vstring('keep *_QWTrack_*_*'),
    fileName = cms.untracked.string('track.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('ana')
    )
)
process.RAWoutput_step = cms.EndPath(process.RAWSIMoutput)

process.schedule = cms.Schedule(
	process.ana,
#	process.RAWoutput_step
)
