

#MATLAB TUTORIAL: https://www.mathworks.com/help/matlabmobile/ug/creating-matrices-and-arrays.html


import xlrd
import numpy as np

#------------------------------------------------------------------------------------------------------
# VARIABLE DEFINITIONS
#------------------------------------------------------------------------------------------------------

coeff = []
fract_v = []

# starter variable definitions (these are the command line parameters of the matlab program)
mop_moon_jd_lookup = [0.655740699156587,0.0357116785741896,0.849129305868777,0.933993247757551,0.678735154857774,0.757740130578333,0.743132468124916,0.392227019534168,0.655477890177557,0.171186687811562]
JD_tt = 0.1

# Opening data file (xls format)
# You MAY have to give full path of data file so program knows where to look
wb = xlrd.open_workbook("mop_moon_eph_coeff_as_xls.xls")
mop_moon_eph_coeff = wb.sheet_by_index(0)
#print(mop_moon_eph_coeff.cell_value(5, 11))

#------------------------------------------------------------------------------------------------------
# COMPUTATIONS
#------------------------------------------------------------------------------------------------------

#JD_tt = JD + SSN / (24*3600)
list_end = len(mop_moon_jd_lookup) -1
if JD_tt > mop_moon_jd_lookup[list_end]:
    print('Error, JD is past final moon table value.')

#index and fraction of JD
k = -1
f = -1

for i in range(1,list_end+1):
    #print(i)
    if JD_tt >= mop_moon_jd_lookup[i-1] and JD_tt <= mop_moon_jd_lookup[i]:
        k = i
        f = (JD_tt-mop_moon_jd_lookup[i-1]) / (mop_moon_jd_lookup[i]-mop_moon_jd_lookup[i-1]); #f in range 0,1
        break

f = 2 * f - 1 #fraction scaled in valid range -1,1
if k<0:   #past end of table, k never reset
    k = list_end
    f = 1

#cheby
order = 12
y = np.zeros((order+1))

#print('----------')

if len(coeff) == 0:
    coeff = np.zeros(((order+1), (order+1)))
    # print(coeff)
    coeff[0][0] = 1
    coeff[1][1] = 1
    #for p in coeff:
    #    print(p)

    for idx in range(2, (order+1)):
        #print(idx+1)
        coeff_len = len(coeff[idx]) - 1
        # coeff_len VARIABLE CAN BE USED INTERCHANGEABLY WITH order VARIABLE
        mid_arr = 2*np.concatenate(([0], coeff[idx-1,0:(order)]))
        # print(mid_arr)
        coeff[idx][:] = mid_arr - coeff[idx-2][0:(order+1)]
        #print(*coeff[idx][:])
    idx = idx+1
    #print(idx)
        
    #for p in coeff:
    #    print(*p)

    fract_v = np.zeros((order+1))
    fract_v[0] = 1
    #print(fract_v)

y[0] = 1


for ind in range(2,(order+2)):
    #print('ind: ' + str(ind))
    fract_v[ind-1] = fract_v[ind-2] * f
    #print(*fract_v)
    for sub_ind in range(ind, 0, -2):        
        #print(sub_ind)
        y[ind-1] = y[ind-1] + fract_v[sub_ind-1] * coeff[ind-1, sub_ind-1]
        #print(y[ind-1])
    #print('-------------')

coeff_x = np.zeros(13)
coeff_y = np.zeros(13)
coeff_z = np.zeros(13)

for ii in range(0,13):
    #print(ii)
    #print(mop_moon_eph_coeff.cell_value(k, ii))
    coeff_x[ii] = mop_moon_eph_coeff.cell_value(k-1, ii)

    jj = ii+13
    coeff_y[ii] = mop_moon_eph_coeff.cell_value(k-1, jj)

    pp = ii+26
    coeff_z[ii] = mop_moon_eph_coeff.cell_value(k-1, pp)


#print(*coeff_x)
#print(*coeff_y)
#print(*coeff_z)
#print("y-->",*y)

moon_eci = np.zeros((3,1))
moon_eci[0,0] = 1000*np.dot(coeff_x, y)
moon_eci[1,0] = 1000*np.dot(coeff_y, y)
moon_eci[2,0] = 1000*np.dot(coeff_z, y)

print(moon_eci)


## Supposed output (copied from MATLAB)
#ans =
#          32282571.2372601
#         -377603308.974078
#         -142617176.483837

# close the .xls file
del wb
