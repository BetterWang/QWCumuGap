import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuGap")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('GeneratorInterface.HiGenCommon.AfterBurnerGenerator_cff')

#process.load('QWAna.QWCumuV3.PionFlatPt_cfi')


process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100000))

process.options = cms.untracked.PSet(
		Rethrow = cms.untracked.vstring('ProductNotFound'),
		wantSummary = cms.untracked.bool(True)
		)

#from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:startup', '')

process.source = cms.Source("EmptySource")

process.generator = cms.EDProducer("FlatRandomPtGunProducer",
		PGunParameters = cms.PSet(
			MaxPt = cms.double(2.0),
			MinPt = cms.double(1.0),
			PartID = cms.vint32(),
			MaxEta = cms.double(2.4),
			MaxPhi = cms.double(3.14159265359),
			MinEta = cms.double(-2.4),
			MinPhi = cms.double(-3.14159265359) ## in radians
			),
		Verbosity = cms.untracked.int32(0), ## set to 1 (or greater)  for printouts
		psethack = cms.string('pi pt 0.3 12.3'),
		AddAntiParticle = cms.bool(True),
		firstRun = cms.untracked.uint32(1)
		)

process.AftBurner.modv1 = cms.InputTag("0.0")
process.AftBurner.modv2 = cms.InputTag("0.06")
process.AftBurner.modv3 = cms.InputTag("0.02")
process.AftBurner.fluct_v1 = cms.double(0.0)
process.AftBurner.fluct_v2 = cms.double(0.0)
process.AftBurner.modmethod = cms.int32(1)
process.AftBurner.fixEP = cms.untracked.bool(False)

partid = cms.vint32()
for i in range(150):
	partid.append(211)

process.generator.PGunParameters.PartID = partid

process.QWGenEvent = cms.EDProducer('QWGenEventProducer'
		, trackSrc  = cms.untracked.InputTag("genParticles")
		, isPrompt  = cms.untracked.bool(True)
		)

process.Noff = cms.EDProducer('QWVectCounter'
		, src = cms.untracked.InputTag('QWGenEvent', 'phi')
		)

process.cumugap = cms.EDAnalyzer('QWCumuGap'
		, trackEta = cms.untracked.InputTag('QWGenEvent', "eta")
		, trackPhi = cms.untracked.InputTag('QWGenEvent', "phi")
		, trackPt = cms.untracked.InputTag('QWGenEvent', "pt")
		, trackWeight = cms.untracked.InputTag('QWGenEvent', "weight")
		, vertexZ = cms.untracked.InputTag('QWGenEvent', "vz")
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

process.vectPhi = cms.EDAnalyzer('QWVectorAnalyzer',
                src = cms.untracked.InputTag("QWGenEvent", "phi"),
                hNbins = cms.untracked.int32(5000),
                hstart = cms.untracked.double(0),
                hend = cms.untracked.double(5000),
                cNbins = cms.untracked.int32(1000),
                cstart = cms.untracked.double(-3.14159265358979323846),
                cend = cms.untracked.double(3.14159265358979323846),
                )

process.vectPhiW = process.vectPhi.clone( srcW = cms.untracked.InputTag("QWGenEvent", "weight") )



process.pgen = cms.Sequence(process.generator + cms.SequencePlaceholder("randomEngineStateProducer")+process.AftBurner+process.GeneInfo + process.QWGenEvent + process.Noff + process.cumugap + process.vectPhi + process.vectPhiW)

#process.pgen = cms.Sequence(process.generator + cms.SequencePlaceholder("randomEngineStateProducer") + process.AftBurner + process.GeneInfo)
#process.pgen = cms.Sequence( process.generator )

from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randSvc.populate()

process.TFileService = cms.Service("TFileService",
		fileName = cms.string("cumu.root")
		)

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
		splitLevel = cms.untracked.int32(0),
		eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
		outputCommands = cms.untracked.vstring('keep *'),
		fileName = cms.untracked.string('Hijing.root'),
		dataset = cms.untracked.PSet(
			filterName = cms.untracked.string(''),
			dataTier = cms.untracked.string('GEN-SIM')
			),
		SelectEvents = cms.untracked.PSet(
			SelectEvents = cms.vstring('generation_step')
			)
		)


process.generation_step   = cms.Path(process.pgen )
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

#process.ana = cms.Path(process.QWGenEvent * process.Noff * process.cumugap)

process.schedule = cms.Schedule(
		process.generation_step,
#		process.RAWSIMoutput_step,
		)


#for path in process.paths:
#	getattr(process,path)._seq = process.generator * getattr(process,path)._seq
#




