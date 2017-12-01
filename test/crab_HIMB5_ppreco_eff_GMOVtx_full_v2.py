from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'HIMB5_CumuGap_ppReco_eff_noff_GMOVtx_full_v6'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qwcumu_PbPb15_ppReco_eff_GMOVtx_full_v3.py'
config.JobType.maxJobRuntimeMin = 2500
config.JobType.inputFiles = ['Hydjet_PbPb_eff_v1.root']
config.Data.inputDataset = '/HIMinimumBias5/HIRun2015-02May2016-v1/AOD'
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/PbPb2015_cumu/'
config.Data.lumiMask = 'HIMB5_GMOVertex_full.txt'
config.Data.publication = False
#config.Data.useParent = True
config.Site.storageSite = 'T2_CH_CERN'
#config.Data.allowNonValidInputDataset = True
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##########HIMB6
#config.General.requestName = 'HIMB6_CumuGap_ppReco_eff_noff_GMOVtx_full_v6'
#config.Data.inputDataset = '/HIMinimumBias6/HIRun2015-02May2016-v1/AOD'
#config.Data.lumiMask = 'HIMB6_GMOVertex_full.txt'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
#########HIMB7
#config.General.requestName = 'HIMB7_CumuGap_ppReco_eff_noff_GMOVtx_full_v6'
#config.Data.inputDataset = '/HIMinimumBias7/HIRun2015-02May2016-v1/AOD'
#config.Data.lumiMask = 'HIMB7_GMOVertex_full.txt'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
