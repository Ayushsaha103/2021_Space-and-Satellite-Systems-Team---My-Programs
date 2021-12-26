
import xlrd
import numpy as np

#------------------------------------------------------------------------------------------------------
# VARIABLE DEFINITIONS
#------------------------------------------------------------------------------------------------------

coeff2 = []
fract_v2 = []

# starter variable definitions (these are the command line parameters of the matlab program)
JD_tt = 0.1
moon_eci = [8.147236863931790, 9.057919370756192, 1.269868162935061]

wb1 = xlrd.open_workbook("sol_emb_eph_coeff.xls")
sol_emb_eph_coeff = wb1.sheet_by_index(0)
#print(sol_emb_eph_coeff.cell_value(11, 0))

wb2 = xlrd.open_workbook("sol_sun_eph_coeff.xls")
sol_sun_eph_coeff = wb2.sheet_by_index(0)

wb3 = xlrd.open_workbook("sol_sun_jd_lookup.xls")
sol_sun_jd_lookup = wb3.sheet_by_index(0)


#------------------------------------------------------------------------------------------------------
# COMPUTATIONS
#------------------------------------------------------------------------------------------------------

list_end = sol_sun_jd_lookup.nrows - 1
#print(sol_sun_jd_lookup.cell_value(list_end, 0))
if JD_tt > sol_sun_jd_lookup.cell_value(list_end, 0):
    print('Error, JD is past final moon table value.')

#print(list_end)

k = -1
f = -1

#index and fraction of JD
for i in range(1,list_end+1):
    #print(i)
    if JD_tt >= sol_sun_jd_lookup.cell_value(i-1, 0) and JD_tt <= sol_sun_jd_lookup.cell_value(i, 0):
        k = i
        f = (JD_tt - sol_sun_jd_lookup.cell_value(i-1, 0)) / (sol_sun_jd_lookup.cell_value(i, 0) - sol_sun_jd_lookup.cell_value(i-1, 0))
        break

#print(sol_sun_jd_lookup.cell_value(i-1, 0))

#print('-------------------')
f = 2 * f - 1 #fraction scaled in valid range -1,1
if k < 0:   #past end of table, k never reset
    k = list_end
    f = 1

#cheby
order = 12
y = np.zeros((order+1))

#print(len(y))
#print('------')

if len(coeff2) == 0:
    coeff2 = np.zeros(((order+1), (order+1)))
    # print(coeff)
    coeff2[0][0] = 1
    coeff2[1][1] = 1
    #for p in coeff:
    #    print(p)

    for idx in range(2, (order+1)):
        #print(idx+1)
        coeff_len = len(coeff2[idx]) - 1
        mid_arr = 2*np.concatenate(([0], coeff2[idx-1,0:(order)]))
        # print(mid_arr)
        coeff2[idx][:] = mid_arr - coeff2[idx-2][0:(order+1)]
        # print(coeff2[idx][:])
    idx = idx+1
    #print(idx)

    #for p in coeff2:
    #    print(*p)

    fract_v2 = np.zeros((order+1))
    fract_v2[0] = 1
    #print(fract_v2)

y[0] = 1

for ind in range(2,(order+2)):
    #print(ind)
    fract_v2[ind-1] = fract_v2[ind-2] * f
    # print(*fract_v2)
    for sub_ind in range(ind, 0, -2):        
        #print('subind: ' + str(sub_ind))
        y[ind-1] = y[ind-1] + fract_v2[sub_ind-1] * coeff2[ind-1, sub_ind-1]
        #print(y[ind-1])
    #print('-------------')

y11 = y[0:11]
#print(y11)

#print('-------------')
#print(*y)
#print('-------------')
#print(*fract_v2)
#print('-------------')
#for line in coeff2:
#    print(*line)
#print('-------------')


coeff_x1 = np.zeros(13)
coeff_y1 = np.zeros(13)
coeff_z1 = np.zeros(13)

#print('k:' + str(k))
for ii in range(0,13):
    #print(ii)
    #print(mop_moon_eph_coeff.cell_value(k, ii))
    coeff_x1[ii] = sol_emb_eph_coeff.cell_value(k-1, ii)

    jj = ii+13
    coeff_y1[ii] = sol_emb_eph_coeff.cell_value(k-1, jj)

    pp = ii+26
    coeff_z1[ii] = sol_emb_eph_coeff.cell_value(k-1, pp)

#print(*coeff_x1)
#print(*coeff_y1)
#print(*coeff_z1)
#print("y-->",*y)


coeff_x2 = np.zeros(11)
coeff_y2 = np.zeros(11)
coeff_z2 = np.zeros(11)

for ii2 in range(0,11):
    #print(ii2)
    #print(mop_moon_eph_coeff.cell_value(k, ii2))
    coeff_x2[ii2] = sol_sun_eph_coeff.cell_value(k-1, ii2)

    jj2 = ii2 +11
    coeff_y2[ii2] = sol_sun_eph_coeff.cell_value(k-1, jj2)

    pp2 = ii2 +22
    coeff_z2[ii2] = sol_sun_eph_coeff.cell_value(k-1, pp2)

#print(*coeff_x2)
#print(*coeff_y2)
#print(*coeff_z2)
#print("y-->",*y)


moon_pos = np.zeros(3)
moon_pos = np.multiply(0.012150585609624, moon_eci)
#print(moon_pos)

sun_eci = np.zeros((3,1))
sun_eci[0,0] = 1000*np.dot(coeff_x1, y)
sun_eci[1,0] = 1000*np.dot(coeff_y1, y)
sun_eci[2,0] = 1000*np.dot(coeff_z1, y)

#print(sun_eci)

sun_eci = sun_eci - moon_pos

sun_eci[0,0] = 1000* np.dot(coeff_x2, y11)-sun_eci[0,0]
sun_eci[1,0] = 1000* np.dot(coeff_y2, y11)-sun_eci[1,0]
sun_eci[2,0] = 1000* np.dot(coeff_z2, y11)-sun_eci[2,0]

print(sun_eci)

# Supposed answer (what the sun_eci turned out to be in Matlab)
# ans =
#    -136692256334.966          135451987205.431          135451987205.526
#    -54642460746.8418          55179034938.9701          55179034939.0647
#    -23686723628.7498          23945641204.3966          23945641204.4912


# close the .xls files
del wb1
del wb2
del wb3

