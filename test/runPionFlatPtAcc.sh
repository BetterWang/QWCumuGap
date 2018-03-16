#/bin/bash

echo $PWD
WORKDIR=$PWD
ls -l
cd /afs/cern.ch/work/q/qwang/cleanroom2/CMSSW_5_3_20/src/QWAna/QWCumuV3/test
cd /afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/CMSSW_7_5_8_patch3/src/QWAna/QWCumuGap/test
eval `scramv1 runtime -sh`
cp qwcumu_FlatPt_Acc_Gen.py $WORKDIR/cfg.py
cd $WORKDIR
cmsRun cfg.py
ls -l
NEW_UUID=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 8)
echo /eos/cms/store/group/phys_heavyions/qwang/PbPb2015_cumu/MC/FlatPtAcc/cumu_$NEW_UUID.root
cp cumu.root /eos/cms/store/group/phys_heavyions/qwang/PbPb2015_cumu/MC/FlatPtAcc/cumu_$NEW_UUID.root
echo done transfter
