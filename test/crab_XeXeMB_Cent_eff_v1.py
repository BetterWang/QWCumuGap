from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'XeXe1_CumuGap_eff_Cent_v1'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qwcumu_XeXe_ppReco_Cent_eff_v1.py'
config.JobType.maxJobRuntimeMin = 2500
config.JobType.inputFiles = ['XeXe_eff_table_92x_cent.root']
config.Data.inputDataset = '/HIMinimumBias1/XeXeRun2017-PromptReco-v1/AOD'
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 200
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/XeXe/'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/HI/Cert_304899-304907_5TeV_PromptReco_XeXe_Collisions17_JSON.txt'
config.Data.publication = False
config.Data.useParent = False
config.Site.storageSite = 'T2_CH_CERN'
##config.Data.allowNonValidInputDataset = True
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
###### MB2
#config.General.requestName = 'XeXe2_CumuGap_eff_Cent_v1'
#config.Data.inputDataset = '/HIMinimumBias2/XeXeRun2017-PromptReco-v1/AOD'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
###### MB3
#config.General.requestName = 'XeXe3_CumuGap_eff_Cent_v1'
#config.Data.inputDataset = '/HIMinimumBias3/XeXeRun2017-PromptReco-v1/AOD'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
###### MB4
#config.General.requestName = 'XeXe4_CumuGap_eff_Cent_v1'
#config.Data.inputDataset = '/HIMinimumBias4/XeXeRun2017-PromptReco-v1/AOD'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
#
###### MB5
#config.General.requestName = 'XeXe5_CumuGap_eff_Cent_v1'
#config.Data.inputDataset = '/HIMinimumBias5/XeXeRun2017-PromptReco-v1/AOD'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
###### MB6
#config.General.requestName = 'XeXe6_CumuGap_eff_Cent_v1'
#config.Data.inputDataset = '/HIMinimumBias6/XeXeRun2017-PromptReco-v1/AOD'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
###### MB7
#config.General.requestName = 'XeXe7_CumuGap_eff_Cent_v1'
#config.Data.inputDataset = '/HIMinimumBias7/XeXeRun2017-PromptReco-v1/AOD'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
#
###### MB8
#config.General.requestName = 'XeXe8_CumuGap_eff_Cent_v1'
#config.Data.inputDataset = '/HIMinimumBias8/XeXeRun2017-PromptReco-v1/AOD'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
###### MB9
#config.General.requestName = 'XeXe9_CumuGap_eff_Cent_v1'
#config.Data.inputDataset = '/HIMinimumBias9/XeXeRun2017-PromptReco-v1/AOD'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
###### MB10
#config.General.requestName = 'XeXe10_CumuGap_eff_Cent_v1'
#config.Data.inputDataset = '/HIMinimumBias10/XeXeRun2017-PromptReco-v1/AOD'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#

##### MB11
config.General.requestName = 'XeXe11_CumuGap_eff_Cent_v1'
config.Data.inputDataset = '/HIMinimumBias11/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB12
config.General.requestName = 'XeXe12_CumuGap_eff_Cent_v1'
config.Data.inputDataset = '/HIMinimumBias12/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB13
config.General.requestName = 'XeXe13_CumuGap_eff_Cent_v1'
config.Data.inputDataset = '/HIMinimumBias13/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB14
config.General.requestName = 'XeXe14_CumuGap_eff_Cent_v1'
config.Data.inputDataset = '/HIMinimumBias14/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB15
config.General.requestName = 'XeXe15_CumuGap_eff_Cent_v1'
config.Data.inputDataset = '/HIMinimumBias15/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB16
config.General.requestName = 'XeXe16_CumuGap_eff_Cent_v1'
config.Data.inputDataset = '/HIMinimumBias16/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB17
config.General.requestName = 'XeXe17_CumuGap_eff_Cent_v1'
config.Data.inputDataset = '/HIMinimumBias17/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB18
config.General.requestName = 'XeXe18_CumuGap_eff_Cent_v1'
config.Data.inputDataset = '/HIMinimumBias18/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB19
config.General.requestName = 'XeXe19_CumuGap_eff_Cent_v1'
config.Data.inputDataset = '/HIMinimumBias19/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


##### MB20
config.General.requestName = 'XeXe20_CumuGap_eff_Cent_v1'
config.Data.inputDataset = '/HIMinimumBias20/XeXeRun2017-PromptReco-v1/AOD'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


