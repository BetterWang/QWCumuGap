#define CORRELATIONS_CLOSED_ENABLE_U8 1
#define CORRELATIONS_CLOSED_ENABLE_U7 1
#ifndef CORRELATIONS_CLOSED_FROMQVECTOR_HH
#define CORRELATIONS_CLOSED_FROMQVECTOR_HH
/**
 * @file   correlations/closed/FromQVector.hh
 * @author Christian Holm Christensen <cholm@nbi.dk>
 * @date   Thu Oct 24 23:45:40 2013
 *
 * @brief  Cumulant using closed-form expressions
 */
/*
 * Multi-particle correlations
 * Copyright (C) 2013 K.Gulbrandsen, A.Bilandzic, C.H. Christensen.
 *
 * This program is free software: you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see http://www.gnu.org/licenses.
 */
#include <correlations/QVector.hh>
#include <correlations/FromQVector.hh>

namespace correlations {
  /**
   * Namespace for closed form calculations
   */
  namespace closed {
    //____________________________________________________________________
    /**
     * Structure to calculate Cumulants of up to 8th order and power from
     * a given Q vector.
     *
     * This implementation used closed-form expression to evaluate up
     * to @f$ QC\{8\}@f$.
     *
     * @note This implementation is probably one of the fastest, but
     * it is not very flexible and it taked a very long time to
     * compile.  A better option would probably be to use pre-defined
     * functions with recurssion - at least up to some order
     *
     * @headerfile correlations/closed/FromQVector.hh  <correlations/closed/FromQVector.hh>
     */
    struct FromQVector : public correlations::FromQVector
    {
      /**
       * Constructor
       *
       * @param q Q vector to use
       */
      FromQVector(QVector& q) : correlations::FromQVector(q)
      {
#ifdef CORRELATIONS_CLOSED_ENABLE_U8
	_maxFixed = 8;
#elif  CORRELATIONS_CLOSED_ENABLE_U7
	_maxFixed = 7;
#else
	_maxFixed = 6;
#endif
      }
      /**
       * @return Name of the correlator
       */
      virtual const char* name() const { return "Closed form cumulant"; }
    protected:
      /**
       * Calculate the @a n particle correlation using harmonics @a h
       *
       * @param n How many particles to correlate
       * @param h Harmonic of each term
       *
       * @return The correlator and the summed weights
       */
      Complex ucN(const Size n, const HarmonicVector& h) const
      {
	switch (n) {
	case 1: return uc1(h[0]);
	case 2: return uc2(h[0], h[1]);
	case 3: return uc3(h[0], h[1], h[2]);
	case 4: return uc4(h[0], h[1], h[2], h[3]);
	case 5: return uc5(h[0], h[1], h[2], h[3], h[4]);
	case 6: return uc6(h[0], h[1], h[2], h[3], h[4], h[5]);
	case 7:
#ifdef CORRELATIONS_CLOSED_ENABLE_U7
	  return uc7(h[0], h[1], h[2], h[3], h[4], h[5], h[6]);
#else
	  std::cerr << "closed-form C7 disabled at compile-time" << std::endl;
	  break;
#endif
	case 8:
#ifdef CORRELATIONS_CLOSED_ENABLE_U8
	  return uc8(h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7]);
#else
	  std::cerr << "closed-form C8 disabled at compile-time" << std::endl;
	  break;
#endif
	}
	std::cerr << "Number of correlators too big:" << n << std::endl;
	return Complex();
      }
      /**
       * Generic 1-particle correlation
       * @f[
       * QC\{1\} = \langle\exp[i(\sum_j^1 h_j\phi_j)]\rangle
       * @f]
       *
       * @param n1 Harmonics @f$ h_1@f$
       *
       * @return @f$ QC\{1\}@f$
       */
      Complex uc1(const Harmonic n1) const
      {
	return _q(n1, 1);
      }
      /**
       * Do the 2-particle calculation
       *
       * @param n1 1st Harmonic
       * @param n2 2nd Harmonic
       *
       * @return the correlator
       */
      Complex uc2(const Harmonic n1, const Harmonic n2) const
      {
	return _q(n1,1) * _q(n2,1) - _q(n1+n2,2);
      }
      /**
       * Do the 3-particle calculation
       *
       * @param n1 1st Harmonic
       * @param n2 2nd Harmonic
       * @param n3 3rd Harmonic
       *
       * @return the correlator
       */
      Complex uc3(const Harmonic n1,
		  const Harmonic n2,
		  const Harmonic n3) const
      {
	const Real k2 = 2;
	return (_q(n1,1)*_q(n2,1)*_q(n3,1)
		- _q(n1+n2,2)*_q(n3,1)
		- _q(n2,1)*_q(n1+n3,2)
		- _q(n1,1)*_q(n2+n3,2)
		+ k2*_q(n1+n2+n3,3));
      }
      /**
       * Do the 4-particle calculation
       *
       * @param n1 1st Harmonic
       * @param n2 2nd Harmonic
       * @param n3 3rd Harmonic
       * @param n4 4th Harmonic
       *
       * @return the correlator
       */
      Complex uc4(const Harmonic n1,
		  const Harmonic n2,
		  const Harmonic n3,
		  const Harmonic n4) const
      {
	const Real k2 = 2;
	const Real k6 = 6;
	return (_q(n1,1)*_q(n2,1)*_q(n3,1)*_q(n4,1)
		- _q(n1+n2,2)*_q(n3,1)*_q(n4,1)
		- _q(n2,1)*_q(n1+n3,2)*_q(n4,1)
		- _q(n1,1)*_q(n2+n3,2)*_q(n4,1)
		+ k2*_q(n1+n2+n3,3)*_q(n4,1)
		- _q(n2,1)*_q(n3,1)*_q(n1+n4,2)
		+ _q(n2+n3,2)*_q(n1+n4,2)
		- _q(n1,1)*_q(n3,1)*_q(n2+n4,2)
		+ _q(n1+n3,2)*_q(n2+n4,2)
		+ k2*_q(n3,1)*_q(n1+n2+n4,3)
		- _q(n1,1)*_q(n2,1)*_q(n3+n4,2)
		+ _q(n1+n2,2)*_q(n3+n4,2)
		+ k2*_q(n2,1)*_q(n1+n3+n4,3)
		+ k2*_q(n1,1)*_q(n2+n3+n4,3)
		- k6*_q(n1+n2+n3+n4,4));
      }
      /**
       * Do the 5-particle calculation
       *
       * @param n1 1st Harmonic
       * @param n2 2nd Harmonic
       * @param n3 3rd Harmonic
       * @param n4 4th Harmonic
       * @param n5 5th Harmonic
       *
       * @return The correlator
       */
      Complex uc5(const Harmonic n1,
		  const Harmonic n2,
		  const Harmonic n3,
		  const Harmonic n4,
		  const Harmonic n5) const;
      /**
       * Do the 6-particle calculation
       *
       * @param n1 1st Harmonic
       * @param n2 2nd Harmonic
       * @param n3 3rd Harmonic
       * @param n4 4th Harmonic
       * @param n5 5th Harmonic
       * @param n6 6th Harmonic
       *
       * @return The correlator
       */
      virtual Complex uc6(const Harmonic n1,
			  const Harmonic n2,
			  const Harmonic n3,
			  const Harmonic n4,
			  const Harmonic n5,
			  const Harmonic n6) const;
      /**
       * Do the 7-particle calculation
       *
       * @param n1 1st Harmonic
       * @param n2 2nd Harmonic
       * @param n3 3rd Harmonic
       * @param n4 4th Harmonic
       * @param n5 5th Harmonic
       * @param n6 6th Harmonic
       * @param n7 7th Harmonic
       *
       * @return The correlator
       */
      virtual Complex uc7(const Harmonic n1,
			  const Harmonic n2,
			  const Harmonic n3,
			  const Harmonic n4,
			  const Harmonic n5,
			  const Harmonic n6,
			  const Harmonic n7) const;
#ifdef CORRELATIONS_CLOSED_ENABLE_U8
      Complex uc8P1(const Harmonic n1,
		    const Harmonic n2,
		    const Harmonic n3,
		    const Harmonic n4,
		    const Harmonic n5,
		    const Harmonic n6,
		    const Harmonic n7,
		    const Harmonic n8) const;

      Complex uc8P2(const Harmonic n1,
		    const Harmonic n2,
		    const Harmonic n3,
		    const Harmonic n4,
		    const Harmonic n5,
		    const Harmonic n6,
		    const Harmonic n7,
		    const Harmonic n8) const;
      Complex uc8P3(const Harmonic n1,
		    const Harmonic n2,
		    const Harmonic n3,
		    const Harmonic n4,
		    const Harmonic n5,
		    const Harmonic n6,
		    const Harmonic n7,
		    const Harmonic n8) const;
      Complex uc8P4(const Harmonic n1,
		    const Harmonic n2,
		    const Harmonic n3,
		    const Harmonic n4,
		    const Harmonic n5,
		    const Harmonic n6,
		    const Harmonic n7,
		    const Harmonic n8) const;
      /**
       * Do the 8-particle calculation
       *
       * @param n1 1st Harmonic
       * @param n2 2nd Harmonic
       * @param n3 3rd Harmonic
       * @param n4 4th Harmonic
       * @param n5 5th Harmonic
       * @param n6 6th Harmonic
       * @param n7 7th Harmonic
       * @param n8 8th Harmonic
       *
       * @return The correlator
       */
      Complex uc8(const Harmonic n1,
		  const Harmonic n2,
		  const Harmonic n3,
		  const Harmonic n4,
		  const Harmonic n5,
		  const Harmonic n6,
		  const Harmonic n7,
		  const Harmonic n8) const
      {
	return (uc8P1(n1,n2,n3,n4,n5,n6,n7,n8)
		+ uc8P2(n1,n2,n3,n4,n5,n6,n7,n8)
		+ uc8P3(n1,n2,n3,n4,n5,n6,n7,n8)
		+ uc8P4(n1,n2,n3,n4,n5,n6,n7,n8));
      }
#else
      Complex uc8(const Harmonic,
		  const Harmonic,
		  const Harmonic,
		  const Harmonic,
		  const Harmonic,
		  const Harmonic,
		  const Harmonic,
		  const Harmonic) const
      {
	std::cerr << "closed-form un-correted 8-particle correlator disabled at compile-time" << std::endl;
	return Complex(0,0);
      }
#endif // CORRELATIONS_CLOSED_IGNORE_U8
    };
  }
}
#endif
// Local Variables:
//  mode: C++
// End:
