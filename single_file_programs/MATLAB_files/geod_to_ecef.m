function r_ecef = geod_to_ecef(latgd,lon,alt)

% Reference: Vallado (p173)

R_e=6378137;         
f=1/298.257223563;
e=sqrt(2*f-f^2);
latgd=latgd*pi/180;
lon=lon*pi/180;
        
R_e=R_e/sqrt(1-(e^2*sin(latgd)*sin(latgd)));
r_delta=(R_e+alt)*cos(latgd);
r_k=((1-e^2)*R_e+alt)*sin(latgd);

r_ecef=zeros(3,1);
r_ecef(1)=r_delta*cos(lon);
r_ecef(2)=r_delta*sin(lon);
r_ecef(3)=r_k;

        