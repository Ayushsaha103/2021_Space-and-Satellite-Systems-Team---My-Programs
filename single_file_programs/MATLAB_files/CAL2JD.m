function JD   = CAL2JD( date )
%INPUT: Calendar date, MM,DD,YYYY
%OUTPUT: Modified Julian Date, MJD
%source: Montenbruck A.1.1 page 321
Y = date(1);
M = date(2);
D = date(3);
hr  = date(4);
min = date(5);
sec = date(6);

if(Y < 1583)
    disp('Error, year is out of bounds.')
    JD = 0;
else
    if(M <= 2)
        y = Y-1;
        m = M+12;
    else
        y = Y;
        m = M;
    end
    B = floor(y/400)-floor(y/100)+floor(y/4);
    MJD = 365*y-679004+floor(B)+floor(30.6001*(m+1))+D + hr/24 + min/(24*60) + sec/(24*60*60);
    JD = MJD + 2400000.5;
end
end
