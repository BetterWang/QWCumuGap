#include <correlations/Types.hh>
#include <correlations/Result.hh>
#include <correlations/QVector.hh>
#include <correlations/recursive/FromQVector.hh>
#include <correlations/recurrence/FromQVector.hh>
#include <correlations/closed/FromQVector.hh>
#include <TComplex.h>
#include <TH1.h>
#include <TH2.h>
#include <TTree.h>
#include <TNtupleD.h>
#include <TRandom3.h>
#include <TFile.h>
#include <RecoHI/HiEvtPlaneAlgos/interface/HiEvtPlaneList.h>
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
//
// constants, enums and typedefs
//

//#define QW_DEBUG 1
//#define QW_PEREVENT 1

#define PRD(x) cout << "!!QW!! " << __LINE__ << " DEBUG OUTPUT " << (#x) << " = " << (x) << endl;
#define PR(x) cout << "!!QW!! " << __LINE__ << " DEBUG OUTPUT " << (#x) << endl;
//
// class declaration
//

///////////////// Class ////////////////////////////

class QWCumuGap : public edm::EDAnalyzer {
	public:
		explicit QWCumuGap(const edm::ParameterSet&);
		~QWCumuGap();

		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

	private:
		virtual void beginJob() ;
		virtual void analyze(const edm::Event&, const edm::EventSetup&);
		virtual void endJob() ;

		virtual void beginRun(edm::Run const&, edm::EventSetup const&);
		virtual void endRun(edm::Run const&, edm::EventSetup const&);
		virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
		virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

	/////////////////////////////////////////////
		//TRandom3 * gRandom;
		// ----------member data ---------------------------

		edm::InputTag					trackEta_;
		edm::InputTag					trackPhi_;
		edm::InputTag					trackPt_;
		edm::InputTag					trackWeight_;
		edm::InputTag					vertexZ_;

		edm::InputTag					centralityTag_;

		double	minvz_, maxvz_;
	/////////////////////////////////////////////
		double	rfpmineta_, rfpmaxeta_;
		double	rfpminpt_, rfpmaxpt_;

		int	cmode_;

		int	nvtx_;

	/////////////////////////////////////////////
		TTree * trV;

		int gNoff;
		int gMult;

		double rQaabc[7];
		double iQaabc[7];
		double wQaabc[7];

		double rQab[7];
		double iQab[7];
		double wQab[7];

		double rQac[7];
		double iQac[7];
		double wQac[7];

		double rQ2[7];
		double iQ2[7];
		double wQ2[7];

		double rQ4[7];
		double iQ4[7];
		double wQ4[7];

		correlations::HarmonicVector	hc[7];
		correlations::HarmonicVector	h4[7];
		correlations::QVector		qA[7];
		correlations::QVector		qB[7];
		correlations::QVector		qC[7];
		correlations::QVector		q4[7];

		double etabin[4];

		void initQ();
		void doneQ();

};



