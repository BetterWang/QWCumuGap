from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'HIMB5_CumuGap_ppReco_eff_noff_sysTight2Xstd_v2'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qwcumu_PbPb15_ppReco_eff_sysTight2Xstd_v1.py'
config.JobType.maxJobRuntimeMin = 2500
config.JobType.inputFiles = ['Hydjet_PbPb_eff_v1.root']
config.Data.inputDataset = '/HIMinimumBias5/HIRun2015-02May2016-v1/AOD'
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 20
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/PbPb2015_cumu/'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/HI/Cert_262548-263757_PromptReco_HICollisions15_JSON_v2.txt'
config.Data.publication = False
config.Data.useParent = False
config.Site.storageSite = 'T2_CH_CERN'
#config.Data.allowNonValidInputDataset = True
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)


config.JobType.psetName = 'qwcumu_PbPb15_ppReco_eff_sysLooseXstd_v1.py'
config.General.requestName = 'HIMB5_CumuGap_ppReco_eff_noff_sysLooseXstd_v2'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)

config.JobType.psetName = 'qwcumu_PbPb15_ppReco_eff_sysLooseXTight2_v1.py'
config.General.requestName = 'HIMB5_CumuGap_ppReco_eff_noff_sysLooseXTight2_v2'
config.JobType.inputFiles = ['Hydjet_ppReco_tight2_v2.root']
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)


config.JobType.psetName = 'qwcumu_PbPb15_ppReco_eff_sysTight2XLoose_v1.py'
config.General.requestName = 'HIMB5_CumuGap_ppReco_eff_noff_sysTight2XLoose_v2'
config.JobType.inputFiles = ['Hydjet_ppReco_v5_loose.root']
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)
