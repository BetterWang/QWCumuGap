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

	etabin[0] = rfpmineta_;
	etabin[1] = rfpmineta_ + (rfpmaxeta_ - rfpmineta_)/3.;
	etabin[2] = rfpmineta_ + 2*(rfpmaxeta_ - rfpmineta_)/3.;
	etabin[3] = rfpmaxeta_;

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
		q4[n] = correlations::QVector(0, 0, true);
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
	trV->Branch("wQ2", &wQ2[2], "wQ2/D");
	trV->Branch("wQ4", &wQ4[2], "wQ4/D");

	for ( int n = 2; n < 7; n++ ) {
		trV->Branch(Form("rQaabc%i", n), &rQaabc[n], Form("rQaabc%i/D", n));
		trV->Branch(Form("rQab%i", n), &rQab[n], Form("rQab%i/D", n));
		trV->Branch(Form("rQac%i", n), &rQac[n], Form("rQac%i/D", n));
		trV->Branch(Form("rQ2%i", n), &rQ2[n], Form("rQ2%i/D", n));
		trV->Branch(Form("rQ4%i", n), &rQ4[n], Form("rQ4%i/D", n));
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


	int rfp_sz = 0;
	for ( int i = 0; i < sz; i++ ) {
		if ( (*hPt)[i] < rfpminpt_ or (*hPt)[i] > rfpmaxpt_ ) continue;
		if ( (*hEta)[i] > rfpmineta_ or (*hEta)[i] < rfpmaxeta_ ) {
			for ( int n = 1; n < 7; n++ ) {
				q4[n].fill( (*hPhi)[i], (*hWeight)[i] );
			}
			rfp_sz++;
		}
		if ( (*hEta)[i] > etabin[0] and (*hEta)[i] < etabin[1] ) {
			// B
			for ( int n = 1; n < 7; n++ ) {
				qB[n].fill( (*hPhi)[i], (*hWeight)[i] );
			}
		} else if ( (*hEta)[i] > etabin[1] and (*hEta)[i] < etabin[2] ) {
			// A
			for ( int n = 1; n < 7; n++ ) {
				qA[n].fill( (*hPhi)[i], (*hWeight)[i] );
			}
		} else if ( (*hEta)[i] > etabin[2] and (*hEta)[i] < etabin[3] ) {
			// C
			for ( int n = 1; n < 7; n++ ) {
				qC[n].fill( (*hPhi)[i], (*hWeight)[i] );
			}
		}
	}

	for ( int n = 2; n < 7; n++ ) {
		correlations::FromQVector *cqA = nullptr;
		correlations::FromQVector *cqB = nullptr;
		correlations::FromQVector *cqC = nullptr;
		correlations::FromQVector *cq4 = nullptr;

		switch ( cmode_ ) {
			case 1:
				cqA = new correlations::closed::FromQVector(qA[n]);
				cqB = new correlations::closed::FromQVector(qB[n]);
				cqC = new correlations::closed::FromQVector(qC[n]);
				cq4 = new correlations::closed::FromQVector(q4[n]);
				break;
			case 2:
				cqA = new correlations::recurrence::FromQVector(qA[n]);
				cqB = new correlations::recurrence::FromQVector(qB[n]);
				cqC = new correlations::recurrence::FromQVector(qC[n]);
				cq4 = new correlations::recurrence::FromQVector(q4[n]);
				break;
			case 3:
				cqA = new correlations::recursive::FromQVector(qA[n]);
				cqB = new correlations::recursive::FromQVector(qB[n]);
				cqC = new correlations::recursive::FromQVector(qC[n]);
				cq4 = new correlations::recursive::FromQVector(q4[n]);
				break;
		}
		auto rA = cqA->calculate(2, hc[n]);
		auto rB = cqB->calculate(1, hc[n]);
		auto rC = cqC->calculate(1, hc[n]);
		auto rA1= cqA->calculate(1, hc[n]);
		auto r4 = cq4->calculate(4, h4[n]);
		auto r2 = cq4->calculate(2, h4[n]);

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

		rQ2[n] = r2.sum().real();
		iQ2[n] = r2.sum().imag();
		wQ2[n] = r2.weight();

		rQ4[n] = r4.sum().real();
		iQ4[n] = r4.sum().imag();
		wQ4[n] = r4.weight();

		delete cqA;
		delete cqB;
		delete cqC;
		delete cq4;
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
	for ( int n = 1; n < 7; n++ ) {
		hc[n] = correlations::HarmonicVector(2);
		hc[n][0] =  n;
		hc[n][1] =  n;
		qA[n].resize(hc[n]);
		qB[n].resize(hc[n]);
		qC[n].resize(hc[n]);

		h4[n] = correlations::HarmonicVector(4);
		h4[n][0] =  n;
		h4[n][1] = -n;
		h4[n][2] =  n;
		h4[n][3] = -n;
		q4[n].resize(h4[n]);
	}
}

void
QWCumuGap::doneQ()
{
	for ( int n = 1; n < 7; n++ ) {
		qA[n].reset();
		qB[n].reset();
		qC[n].reset();

		q4[n].reset();
	}
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
