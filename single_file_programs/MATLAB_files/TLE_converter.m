function [info] = TLE_converter(TLE)
% ***Input as one line string***
% ***Ensure spacing is the same as when copied (some with double or triple
% spaces***
% Format and data extracted per: https://en.wikipedia.org/wiki/Two-line_element_set

%% EXAMPLE TLE
% Standard format:
% ISS (ZARYA)
% 1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
% 2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537

%NANOSATC-BR1            
%1 40024U 14033Q   18096.82617434  .00000325  00000-0  40055-4 0  9998
%2 40024  97.9109  13.7983 0013653  59.0946 301.1611 14.89517477206250

%% EXAMPLE TLE reformated
% Input format:
% TLE_ISS = TLE_converter('1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0 2927  2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537');
% TLE_GEO = TLE_converter('1 99999U          18093.50000000 -.00000019  00000-0 -10758+5 0 00001 2 99999 000.0044 327.9601 0000024 102.8766 178.8790 01.00279711000018');

% TLE_AZ1 = TLE_converter('1 43855U 18104G   19056.63241998  .00000042  00000-0  00000-0 0  9998 2 43855  85.0368 131.1811 0018294  19.7011 340.4950 15.22161332 10828');

dpa = '0.'; % Decimal point assumed 

info1  = str2num(TLE(19:20)); % Epoch Year (last two digits of year)
info2  = str2num(TLE(21:32)); % Epoch Year Julian Date (day of the year as fractional portion of the day)
info3  = str2num(TLE(54:59)); % BSTAR drag term (decimal point assumed), base
info4  = str2num(TLE(60:61)); % BSTAR drag term (decimal point assumed), exponent

info5  = str2num(TLE(79:86)); % Inclination (degrees)
info6  = str2num(TLE(88:95)); % RAAN (degrees)
i7  = (TLE(97:103)); % Eccentricity 
in7 = [dpa i7];
info7 = str2num(in7);
info8  = str2num(TLE(105:112)); % Argument of perigee (degrees)
info9  = str2num(TLE(114:121)); % Mean anomaly (degrees)
info10 = str2num(TLE(123:133)); % Mean motion (revolutions per day)

info = [info1 info2 info3 info4 info5 info6 info7 info8 info9 info10];