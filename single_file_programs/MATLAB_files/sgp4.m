function [r_eci, v_eci]  = sgp4(JD,info)
%#eml
%JD=JD+ssn/86400; % u/86400+2440587.5;
JD_2000=JD-2451545;

r_eci=zeros(3,1);
v_eci = zeros(3,1);

% Get R and V of current calculated JD
[rr,vv] = NORADwis(JD_2000,info);

% Save results in output structure
v_eci(1) = vv(1)*1000;
v_eci(2) = vv(2)*1000;
v_eci(3) = vv(3)*1000;
r_eci(1) = rr(1)*1000;
r_eci(2) = rr(2)*1000;
r_eci(3) = rr(3)*1000;

function [rr,vv,JDdte] = NORADwis( dEnd, info )

%-------------------------------------------------------------------------------
%   Propagates the NORAD two line elements. [] can be entered for any input.
%-------------------------------------------------------------------------------
%-------------------------------------------------------------------------------
%	References:	Hoots, F. R. and R. L. Roehrich, "Spacetrack Report No. 3:
%             Models for Propagation of NORAD Element Sets", Dec. 1980.
%-------------------------------------------------------------------------------
%	 Copyright 1997 Princeton Satellite Systems, Inc. All rights reserved.
%-------------------------------------------------------------------------------

degToRad = pi/180;
dayToMin = 1440;

% Line 1
 epochYear        = info(1);
 epochJulianDate  = info(2);
 bStar            = info(3)*10^info(4)/1e5;
% Line 2
 i0             =  info(5)*degToRad;
 f0             =  info(6)*degToRad;
 e0             =  info(7);
 w0             =  info(8)*degToRad;
 M0             =  info(9)*degToRad;
 n0             =  info(10)*2*pi/dayToMin;  

 JDdte=367*( epochYear+2000) - floor(7/4*( epochYear+2000))+  epochJulianDate + 1721013.5+30;
 dStart=JDdte-2451545;
   
 [rr,vv] = SGP4( i0,f0,e0,w0,M0,n0,bStar,dStart,dEnd);
	               
 % Coordinate frames
 %------------------
	if( nargout > 0 )
		rr = rr*6378.135;
		vv = vv*6378.135*1440.0/86400;
    end

function z = ACTan( x, y )

z = atan2( x, y );

if z < 0
 z = z + 2*pi;
end

function y = FMod2Pi( x )

twoPi = 2*pi;
k = floor(x/twoPi);
y = x - k*twoPi;
if( y < 0 )
  y = y + twoPi;
end


%-------------------------------------------------------------------------------
%  SGP4
%-------------------------------------------------------------------------------
function [rr,vv] = SGP4(  i0,f0,e0,w0,M0,n0,bStar,dStart,dEnd)
     
% Constants
%----------
true      =    1;
false     =    0;
kE        =    0.743669161e-1;
aE        =    1.0;
rE        =    6378.135;
j2        =    1.082616e-3;
j3        =   -0.253881e-5;
j4        =   -1.65597e-6;
a30       =   -j3*aE^3;
daysToMin = 1440.0;
s         = 1.01222928;
q0MS4     = 1.88027916e-9;

% Values independent of time since epoch
%---------------------------------------
cI0     = cos(i0);
sI0     = sin(i0);
e0      = e0;
e0Sq    = e0^2;
a1      = (kE/n0)^(2/3);
k2      = 0.5*j2*aE^2;
k4      = -(3/8)*j4*aE^4;
beta0   = sqrt(1 - e0Sq);
beta0Sq = beta0^2;
z       = (3*cI0^2 - 1)/beta0^3;
d1      = 1.5*(k2/a1^2)*z;
a0      = a1*(1 - d1/3 - d1^2 - (134/81)*d1^3);
d0      = 1.5*(k2/a0^2)*z;
n0PP    = n0/(1 + d0);
a0PP    =   a0/(1 - d0);

if( a0PP*(1-e0)/aE < (220/rE + aE) )
  lowAltitude = true;
else
  lowAltitude = false;
end

% Adjust s and q0MS4 if s is adjusted
%------------------------------------
rP = (a0PP*(1 - e0) - aE)*rE;
if( (rP > 98) & (rP < 156) )
  sStar = (rP - 78)/rE + aE;
	q0MS4 = (q0MS4^0.25 + s - sStar)^4;
	s     = sStar;
elseif( rP < 98 )
	sStar = 20/rE + aE;
	q0MS4 = (q0MS4^0.25 + s - sStar)^4;
	s     = sStar;
end

theta   = cI0; % For consistency with the documentation
theta2  = theta^2;
zeta    = 1/(a0PP - s);
eta     = a0PP*e0*zeta;
etaSq   = eta^2;
fEta    = abs(1 - etaSq);
z       = q0MS4*zeta^4/fEta^3.5;
en      = e0*eta;

c2 = z*n0PP*(   a0PP*(1 + 1.5*etaSq + en*(4 + etaSq))...
              + 0.75*k2*(zeta/fEta)*(3*theta2 - 1)*(8 + 3*etaSq*(8 + etaSq)));
c1 = bStar*c2;
c3 = q0MS4*zeta^5*a30*n0PP*aE*sI0/(k2*e0);
c4 = 2*n0PP*z*a0PP*beta0Sq*( (2*eta*(1 + en) + (e0 + eta^3)/2) - (2*k2*zeta/(a0PP*fEta))...
                              *( 3*(1 - 3*theta2)*(1 + 1.5*etaSq - en*(2 + 0.5*etaSq))...
													     + 0.75*(1 - theta2)*(2*etaSq - en*(1 + etaSq))*cos(2*w0)));

IL2 = 1.5*c1;

d2=0;
d3=0;
d4=0;
c5=0;
IL3=0;
IL4=0;
IL5=0;

if( lowAltitude == false )
  c5  = 2*z*a0PP*beta0Sq*(1 + 2.75*eta*(eta + e0) + e0*eta^3);
  d2  =     4*a0PP*zeta                    *c1^2;
  d3  = (4/3)*a0PP*zeta^2*( 17*a0PP +    s)*c1^3;
  d4  = (2/3)*a0PP*zeta^3*(221*a0PP + 31*s)*c1^4;
							
  IL3 = d2 + 2*c1^2;
  IL4 = 0.25*(3*d3 + 12*c1*d2 + 10*c1^3);
  IL5 = 0.20*(3*d4 + 12*c1*d3 + 6*d2^2 + 30*c1^2*d2 + 15*c1^4);
end

% Constant quantities
%--------------------
a2B4   = a0PP^2*beta0^4;
a4B8   = a2B4^2;

m1 = n0PP*(1 + 3*k2  *(3*theta2 - 1)                 *beta0/( 2*a2B4)...       
             + 3*k2^2*(13 + theta2*(137*theta2 - 78))*beta0/(16*a4B8)...
					);
							
w1 = n0PP*(    3*k2^2*( 7 + theta2*(395*theta2 - 114))/(16*a4B8)...      
             + 5*k4  *( 3 + theta2*( 49*theta2 -  36))/( 4*a4B8)...
						 - 3*k2  *( 1 - 5*theta2)                 /( 2*a2B4)...
					);
							
f1 = n0PP*(   3*k2^2*theta*(4 - 19*theta2)/(2*a4B8)...      
            + 5*k4  *theta*(3 -  7*theta2)/(2*a4B8)...
						- 3*k2  *theta                /(  a2B4)...
					);
					

t    = linspace(dStart,dEnd,1);
tol  = eps;

rr  = zeros(3,1);
vv  = zeros(3,1);
cM0  = cos(M0);
sM0  = sin(M0);


	dT  = daysToMin*(t(1) - dStart);
	mDF = M0 + m1*dT;
	wDF = w0 + w1*dT;
	fDF = f0 + f1*dT;

	f   = fDF - 10.5*n0PP*k2*theta*c1*dT^2/(a0PP^2*beta0Sq);
	
	  if( lowAltitude == false )
		  dW = bStar*c3*cos(w0)*dT;
		  dM = -(2/3)*q0MS4*bStar*zeta^4*(aE/(e0*eta))*((1 + eta*cos(mDF))^3 - (1 + eta*cM0)^3);
	    a  = a0PP*(1 - c1*dT - d2*dT^2 - d3*dT^3 - d4*dT^4)^2;
	    mP = mDF + dW + dM;
	    w  = wDF - dW - dM;
	    e  = e0 - bStar*(c4*dT + c5*(sin(mP) - sM0));
	    IL = mP + w + f + n0PP*(IL2 + IL3*dT + IL4*dT^2 + IL5*dT^3)*dT^2;
	  else
	    mP = mDF;
	    w  = wDF;
 	    a  = a0PP*(1 - c1*dT)^2;
	    e  = e0 - bStar*c4*dT;
 	    IL = mP + w + f + n0PP*IL2*dT^2;
    end
		inc = i0;
	
	beta = sqrt(1-e^2);
	n    = kE/a^1.5;
	sW   = sin(w);
	cW   = cos(w);
	aXN  = e*cW;
	aYNL = a30*sI0/(4*k2*a*beta^2);
	aYN  = e*sW + aYNL;
	ILL  = 0.5*aYNL*aXN*(3 + 5*theta)/(1 + theta);
	
	ILT  = IL + ILL;
	
	% Solve Kepler's Equation
	%------------------------
	u     = FMod2Pi(ILT - f);
	ePW   = Kepler( u, aYN, aXN, 4*eps );

	% Short period periodics
	%-----------------------
	cE     = cos(ePW);
	sE     = sin(ePW);
	eCosE  = aXN*cE + aYN*sE;
	eSinE  = aXN*sE - aYN*cE;
	eL2    = aXN^2 + aYN^2;
	fEL    = 1 - eL2;
	pL     = a*fEL;
	r      = a*(1 - eCosE);
	rDot   = kE*sqrt(a)*eSinE/r;
	rFDot  = kE*sqrt(pL)/r;
	betaL  = sqrt(fEL);
	z      = eSinE/(1 + betaL);
	cosU   = (a/r)*(cE - aXN + aYN*z);
	sinU   = (a/r)*(sE - aYN - aXN*z);
	u      = ACTan(sinU,cosU);
	cos2U  = 2*cosU^2 - 1;
	sin2U  = 2*sinU*cosU;
	
	dR     =  0.5 *(k2/pL)*(1 - theta2)*cos2U;
	dU     = -0.25*(k2/pL^2)*(7*theta2 - 1)*sin2U;
	z      =  1.5*k2*theta/pL^2;
	dF     =  z*sin2U;
	dI     =  z*sI0*cos2U;
	dRDot  = -(k2*n/pL)*(1 - theta2)*sin2U;
	dRFDot =  (k2*n/pL)*((1 - theta2)*cos2U - 1.5*(1 - 3*theta2));
	
	rK     =  r*(1 - 1.5*k2*betaL*(3*theta2 - 1)/pL^2) + dR;
	uK     =  u + dU;
	fK     =  f + dF;
	iK     =  inc + dI;
	rDotK  =  rDot  + dRDot;
	rFDotK =  rFDot + dRFDot;

	[rr,vv] = RV( fK, iK, uK, rK, rDotK, rFDotK );

    
function [r, v] = RV( fK, iK, uK, rK, rDot, rFDot )
cF     = cos(fK);
sF     = sin(fK);
cI     = cos(iK);
sI     = sin(iK);
M      = [-sF*cI;cF*cI;sI];
N      = [cF;sF;0];
cUK    = cos(uK);
sUK    = sin(uK);
U      = M*sUK + N*cUK;
V      = M*cUK - N*sUK;
r      = rK*U;
v      = rDot*U + rFDot*V;

function ePW = Kepler( u, aYNSL, aXNSL, tol );
ePW   = u;
delta = 1;
while( abs(delta/ePW) > tol );
	c     = cos(ePW);
	s     = sin(ePW);
	delta = (u - aYNSL*c + aXNSL*s - ePW)/(1 - aYNSL*s - aXNSL*c);
	if( abs(delta) > 1 )
		delta = sign(delta);
	end
	ePW   = ePW + delta;
end