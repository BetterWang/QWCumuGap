#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "iostream"
#include "TF1.h"

class QWHFNoffFilter : public edm::EDFilter {
public:
	explicit QWHFNoffFilter(const edm::ParameterSet&);
	~QWHFNoffFilter() {return;}
private:
	virtual bool filter(edm::Event&, const edm::EventSetup&);

	edm::InputTag	srcHF_;
	edm::InputTag	srcNoff_;
	bool	bAbove_;
	edm::InputTag	curve_;

	TF1 * f1;
};

QWHFNoffFilter::QWHFNoffFilter(const edm::ParameterSet& pset) :
	srcHF_(pset.getUntrackedParameter<edm::InputTag>("srcHF")),
	srcNoff_(pset.getUntrackedParameter<edm::InputTag>("srcNoff")),
	bAbove_(pset.getUntrackedParameter<bool>("bAbove", true)),
	curve_(pset.getUntrackedParameter<edm::InputTag>("curve"))
{
	consumes<double>(srcHF_);
	consumes<double>(srcNoff_);

	f1 = new TF1("f1", curve_.label().c_str());
	return;
}

bool QWHFNoffFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	edm::Handle<double> pHF;
	edm::Handle<double> pNoff;
	iEvent.getByLabel( srcHF_, pHF );
	iEvent.getByLabel( srcNoff_, pNoff );

	double cut = f1->Eval(*pHF);
	if ( *pNoff > cut ) {
		if ( bAbove_ ) return true;
		else return false;
	} else {
		if ( bAbove_ ) return false;
		else return true;
	}
}

DEFINE_FWK_MODULE(QWHFNoffFilter);
