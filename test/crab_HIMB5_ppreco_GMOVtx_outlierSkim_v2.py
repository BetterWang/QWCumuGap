from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'HIMB5_ppReco_GMOVtx_outlierSkim_v7'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = False
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qwcumu_PbPb15_GMOVtx_outlierSkim_v2.py'
config.JobType.maxJobRuntimeMin = 2500
#config.JobType.inputFiles = ['Hydjet_PbPb_eff_v1.root', 'Hydjet_ppReco_v5_loose.root']
config.Data.inputDataset = '/HIMinimumBias5/qwang-crab_HIMB5_ppReco_GMOVtx_Skim_v2-24f43a5e005f1179c2354ff225d730bc/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 20
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/PbPb2015_cumu/'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/HI/Cert_262548-263757_PromptReco_HICollisions15_JSON_v2.txt'
config.Data.publication = True
config.Data.useParent = True
config.Site.storageSite = 'T2_CH_CERN'
config.Data.allowNonValidInputDataset = True
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


#########HIMB6
config.General.requestName = 'HIMB6_ppReco_GMOVtx_outlierSkim_v7'
config.Data.inputDataset = '/HIMinimumBias6/qwang-crab_HIMB6_ppReco_GMOVtx_Skim_v2-24f43a5e005f1179c2354ff225d730bc/USER'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


########HIMB7
config.General.requestName = 'HIMB7_ppReco_GMOVtx_outlierSkim_v7'
config.Data.inputDataset = '/HIMinimumBias7/qwang-crab_HIMB7_ppReco_GMOVtx_Skim_v2-24f43a5e005f1179c2354ff225d730bc/USER'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)

