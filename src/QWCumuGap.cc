// -*- C++ -*-
//
// Package:    QWCumuGap
// Class:      QWCumuGap
// 
/**\class QWCumuGap QWCumuGap.cc QWAna/QWCumuGap/src/QWCumuGap.cc

Description: [one line class summary]

Implementation:
[Notes on implementation]
*/
//
// Original Author:  Quan Wang
//         Created:  05/23/2014
// $Id: QWCumuGap.cc,v 1.0 2014/05/23 15:56:58 qwang Exp $
//
//


// system include files
#include <memory>
#include <algorithm>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h>
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidate.h>
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HeavyIonEvent/interface/EvtPlane.h"
#include "TH1.h"
#include "TH2.h"
#include "TNtuple.h"
#include "TComplex.h"
#include <complex>


#include "QWAna/QWCumuGap/interface/QWCumuGap.h"


using namespace std;

//#ifdef QW_DEBUG
//
// constructors and destructor
//
QWCumuGap::QWCumuGap(const edm::ParameterSet& iConfig):
	trackEta_( iConfig.getUntrackedParameter<edm::InputTag>("trackEta") ),
	trackPhi_( iConfig.getUntrackedParameter<edm::InputTag>("trackPhi") ),
	trackPt_( iConfig.getUntrackedParameter<edm::InputTag>("trackPt") ),
	trackWeight_( iConfig.getUntrackedParameter<edm::InputTag>("trackWeight") ),
	vertexZ_( iConfig.getUntrackedParameter<edm::InputTag>("vertexZ") ),
	centralityTag_( iConfig.getUntrackedParameter<edm::InputTag>("centrality") )
{
	//now do what ever initialization is needed
	minvz_ = iConfig.getUntrackedParameter<double>("minvz", -15.);
	maxvz_ = iConfig.getUntrackedParameter<double>("maxvz", 15.);

	rfpmineta_ = iConfig.getUntrackedParameter<double>("rfpmineta", -2.4);
	rfpmaxeta_ = iConfig.getUntrackedParameter<double>("rfpmaxeta", 2.4);
	rfpminpt_ = iConfig.getUntrackedParameter<double>("rfpminpt", 0.3);
	rfpmaxpt_ = iConfig.getUntrackedParameter<double>("rfpmaxpt", 100);

	cmode_ = iConfig.getUntrackedParameter<int>("cmode", 1);
	nvtx_ = iConfig.getUntrackedParameter<int>("nvtx", 100);

        consumes<int>(centralityTag_);
        consumes<std::vector<double> >(trackEta_);
        consumes<std::vector<double> >(trackPhi_);
        consumes<std::vector<double> >(trackPt_);
        consumes<std::vector<double> >(trackWeight_);
        consumes<std::vector<double> >(vertexZ_);

	for ( int n = 1; n < 7; n++ ) {
		qA[n] = correlations::QVector(0, 0, true);
		qB[n] = correlations::QVector(0, 0, true);
		qC[n] = correlations::QVector(0, 0, true);
	}

	//
	//cout << __LINE__ << "\t" << tracks_.label().c_str() << "\t|" << tracks_.instance() << "\t|" << tracks_.process() << endl;
	//
	edm::Service<TFileService> fs;

	trV = fs->make<TTree>("trV", "trV");
	trV->Branch("Noff", &gNoff, "Noff/I");
	trV->Branch("Mult", &gMult, "Mult/I");

	trV->Branch("wQaabc", &wQaabc[2], "wQaabc/D");
	trV->Branch("wQab", &wQab[2], "wQab/D");
	trV->Branch("wQac", &wQac[2], "wQac/D");

	for ( int n = 2; n < 7; n++ ) {
		trV->Branch(Form("rQaabc%i", n), &rQaabc[n], Form("rQaabc%i/D", n));
		trV->Branch(Form("rQab%i", n), &rQab[n], Form("rQab%i/D", n));
		trV->Branch(Form("rQac%i", n), &rQac[n], Form("rQac%i/D", n));
	}

	cout << " cmode_ = " << cmode_ << endl;

	initQ();
}


QWCumuGap::~QWCumuGap()
{

	// do anything here that needs to be done at desctruction time
	// (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

void
QWCumuGap::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;

	Handle<std::vector<double> >	hEta;
	Handle<std::vector<double> >	hPhi;
	Handle<std::vector<double> >	hPt;
	Handle<std::vector<double> >	hWeight;
	Handle<std::vector<double> >	hVz;

	iEvent.getByLabel(trackEta_,	hEta);
	iEvent.getByLabel(trackPhi_,	hPhi);
	iEvent.getByLabel(trackPt_,	hPt);
	iEvent.getByLabel(trackWeight_, hWeight);
	iEvent.getByLabel(vertexZ_, 	hVz);

	if ( hVz->size() < 1 ) return;
	if ( (*hVz)[0] > maxvz_ or (*hVz)[0] < minvz_ ) return;
	int sz = int(hEta->size());
	if ( sz == 0 ) return;

	double etabin[4] = { rfpmineta_, rfpminpt_ + (rfpmaxeta_ - rfpminpt_)/3., rfpminpt_ + 2*(rfpmaxeta_ - rfpminpt_)/3., rfpmaxeta_};

	int rfp_sz = 0;
	for ( int i = 0; i < sz; i++ ) {
		if ( (*hPt)[i] < rfpminpt_ or (*hPt)[i] > rfpmaxpt_ ) continue;
		if ( (*hEta)[i] > etabin[0] and (*hEta)[i] < etabin[1] ) {
			// B
			for ( int n = 1; n < 7; n++ ) {
				qB[n].fill( (*hPhi)[i], (*hWeight)[i] );
			}
			rfp_sz++;
		} else if ( (*hEta)[i] > etabin[1] and (*hEta)[i] < etabin[2] ) {
			// A
			for ( int n = 1; n < 7; n++ ) {
				qA[n].fill( (*hPhi)[i], (*hWeight)[i] );
			}
			rfp_sz++;
		} else if ( (*hEta)[i] > etabin[2] and (*hEta)[i] < etabin[3] ) {
			// C
			for ( int n = 1; n < 7; n++ ) {
				qC[n].fill( (*hPhi)[i], (*hWeight)[i] );
			}
			rfp_sz++;
		}
	}

	for ( int n = 2; n < 7; n++ ) {
		correlations::FromQVector *cqA = nullptr;
		correlations::FromQVector *cqB = nullptr;
		correlations::FromQVector *cqC = nullptr;

		switch ( cmode_ ) {
			case 1:
				cqA = new correlations::closed::FromQVector(qA[n]);
				cqB = new correlations::closed::FromQVector(qB[n]);
				cqC = new correlations::closed::FromQVector(qC[n]);
				break;
			case 2:
				cqA = new correlations::recurrence::FromQVector(qA[n]);
				cqB = new correlations::recurrence::FromQVector(qB[n]);
				cqC = new correlations::recurrence::FromQVector(qC[n]);
				break;
			case 3:
				cqA = new correlations::recursive::FromQVector(qA[n]);
				cqB = new correlations::recursive::FromQVector(qB[n]);
				cqC = new correlations::recursive::FromQVector(qC[n]);
				break;
		}
		auto rA = cqA->calculate(2, hc[n]);
		auto rB = cqB->calculate(1, hc[n]);
		auto rC = cqC->calculate(1, hc[n]);
		auto rA1= cqA->calculate(1, hc[n]);

		correlations::Complex Qaabc = rA.sum() * std::conj(rB.sum()) * std::conj(rC.sum());
		rQaabc[n] = Qaabc.real();
		iQaabc[n] = Qaabc.imag();
		wQaabc[n] = rA.weight() * rB.weight() * rC.weight();

		correlations::Complex Qab = rA1.sum() * std::conj(rB.sum());
		rQab[n] = Qab.real();
		iQab[n] = Qab.imag();
		wQab[n] = rA1.weight() * rB.weight();

		correlations::Complex Qac = rA1.sum() * std::conj(rC.sum());
		rQac[n] = Qac.real();
		iQac[n] = Qac.imag();
		wQac[n] = rA1.weight() * rC.weight();

		delete cqA;
		delete cqB;
		delete cqC;
	}

	edm::Handle<int> ch;
	iEvent.getByLabel(centralityTag_,ch);
	gNoff = *ch;
	gMult = rfp_sz;

	trV->Fill();
	doneQ();

}


void
QWCumuGap::initQ()
{
	hc[1] = correlations::HarmonicVector(2);
	hc[1][0] =  1;
	hc[1][1] =  1;

	hc[2] = correlations::HarmonicVector(2);
	hc[2][0] =  2;
	hc[2][1] =  2;

	hc[3] = correlations::HarmonicVector(2);
	hc[3][0] =  3;
	hc[3][1] =  3;

	hc[4] = correlations::HarmonicVector(2);
	hc[4][0] =  4;
	hc[4][1] =  4;

	hc[5] = correlations::HarmonicVector(2);
	hc[5][0] =  5;
	hc[5][1] =  5;

	hc[6] = correlations::HarmonicVector(2);
	hc[6][0] =  6;
	hc[6][1] =  6;

	qA[1].resize(hc[1]);
	qA[2].resize(hc[2]);
	qA[3].resize(hc[3]);
	qA[4].resize(hc[4]);
	qA[5].resize(hc[5]);
	qA[6].resize(hc[6]);

	qB[1].resize(hc[1]);
	qB[2].resize(hc[2]);
	qB[3].resize(hc[3]);
	qB[4].resize(hc[4]);
	qB[5].resize(hc[5]);
	qB[6].resize(hc[6]);

	qC[1].resize(hc[1]);
	qC[2].resize(hc[2]);
	qC[3].resize(hc[3]);
	qC[4].resize(hc[4]);
	qC[5].resize(hc[5]);
	qC[6].resize(hc[6]);

}

void
QWCumuGap::doneQ()
{
	qA[1].reset();
	qA[2].reset();
	qA[3].reset();
	qA[4].reset();
	qA[5].reset();
	qA[6].reset();

	qB[1].reset();
	qB[2].reset();
	qB[3].reset();
	qB[4].reset();
	qB[5].reset();
	qB[6].reset();

	qC[1].reset();
	qC[2].reset();
	qC[3].reset();
	qC[4].reset();
	qC[5].reset();
	qC[6].reset();
}

// ------------ method called once each job just before starting event loop  ------------
	void 
QWCumuGap::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
	void 
QWCumuGap::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
	void 
QWCumuGap::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
	void 
QWCumuGap::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
	void 
QWCumuGap::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
	void 
QWCumuGap::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
QWCumuGap::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	//The following says we do not know what parameters are allowed so do no validation
	// Please change this to state exactly what you do use, even if it is no parameters
	edm::ParameterSetDescription desc;
	desc.setUnknown();
	descriptions.addDefault(desc);

	//Specify that only 'tracks' is allowed
	//To use, remove the default given above and uncomment below
	//ParameterSetDescription desc;
	//desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
	//descriptions.addDefault(desc);
}

//////////////////////////////////////////


//define this as a plug-in
DEFINE_FWK_MODULE(QWCumuGap);
