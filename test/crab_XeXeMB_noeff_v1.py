from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'XeXe1_CumuGap_noeff_noff_v3'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qwcumu_XeXe_ppReco_Cent_noeff_v1.py'
config.JobType.maxJobRuntimeMin = 2500
#config.JobType.inputFiles = ['Hydjet_PbPb_eff_v1.root']
config.Data.inputDataset = '/HIMinimumBias1/XeXeRun2017-PromptReco-v1/AOD'
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 200
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/XeXe/'
config.Data.lumiMask = 'XeXe_DCS.json'
config.Data.publication = False
config.Data.useParent = False
config.Site.storageSite = 'T2_CH_CERN'
#config.Data.allowNonValidInputDataset = True
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB2
config.General.requestName = 'XeXe2_CumuGap_noeff_noff_v3'
config.Data.inputDataset = '/HIMinimumBias2/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB3
config.General.requestName = 'XeXe3_CumuGap_noeff_noff_v3'
config.Data.inputDataset = '/HIMinimumBias3/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB4
config.General.requestName = 'XeXe4_CumuGap_noeff_noff_v3'
config.Data.inputDataset = '/HIMinimumBias4/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)



##### MB5
config.General.requestName = 'XeXe5_CumuGap_noeff_noff_v3'
config.Data.inputDataset = '/HIMinimumBias5/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB6
config.General.requestName = 'XeXe6_CumuGap_noeff_noff_v3'
config.Data.inputDataset = '/HIMinimumBias6/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB7
config.General.requestName = 'XeXe7_CumuGap_noeff_noff_v3'
config.Data.inputDataset = '/HIMinimumBias7/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)



##### MB8
config.General.requestName = 'XeXe8_CumuGap_noeff_noff_v3'
config.Data.inputDataset = '/HIMinimumBias8/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB9
config.General.requestName = 'XeXe9_CumuGap_noeff_noff_v3'
config.Data.inputDataset = '/HIMinimumBias9/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB10
config.General.requestName = 'XeXe10_CumuGap_noeff_noff_v3'
config.Data.inputDataset = '/HIMinimumBias10/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


