#########################################################
#                 DIT MAG JE VERANDEREN                 #
#########################################################

## BEGINVARIABELEN ## 

O2_PERC_OUT =19.00      # percentage  O2 (uit analysator)
CO2_PERC_OUT = 1.50     # percentage CO2 (uit analysator)

O2_VEL = 0.35           # snelhed lucht analysator (L/min)
CO2_VEL = 0.35          # snelhed lucht analysator (L/min)

MINUTEN = 1             # tijd analysator lucht afzuigen(min)
SECONDEN = 0            # tijd analysator lucht afzuigen(sec)

LUCHTDRUK = 1024.0      # Barometer (in mBar)

STARTLUCHT = 923.0000   # van vacuumpomp (m^3)
EINDLUCHT  = 923.0930   # van vacuumpomp (m^3)

TEMPERATUUR = 25.0      # van vacuumpomp (graden celcius)

TIJD = 10.0             # tijd van meting (min)

GEWICHT = 100.0         # gewicht proefpersoon (kg)
LENGTE =  1.90          #  lengte proefpersoon (m)
 
#########################################################
#             VANAF HIER NIETS VERANDEREN!!             #
#########################################################
import pandas as pd
PRECISION = 5
pd.set_option('precision', PRECISION)
## STANDAARDWAARDEN ##

O2_PERC_IN = 20.93
CO2_PERC_IN =  0.03
N2_PERC_IN = 100.0 - (O2_PERC_IN + CO2_PERC_IN)
print("## STANDAARDWAARDEN ##")
print("%  O2 in: " + str(O2_PERC_IN))
print("% CO2 in:  " + str(CO2_PERC_IN))
print("%  N2 in: " + str(N2_PERC_IN))
print(" ")

## VARIABLE CHECK ##
 
O2_PERC_OUT = float(O2_PERC_OUT)
CO2_PERC_OUT = float(CO2_PERC_OUT)

O2_VEL = float(O2_VEL)
CO2_VEL = float(CO2_VEL)

MINUTEN = float(MINUTEN)
SECONDEN = float(SECONDEN)

LUCHTDRUK = float(LUCHTDRUK) * 0.750061683

STARTLUCHT = float(STARTLUCHT)
EINDLUCHT = float(EINDLUCHT)

TEMPERATUUR = float(TEMPERATUUR)

TIJD = float(TIJD)

GEWICHT = float(GEWICHT)
LENGTE = float(LENGTE)

## BEREKENINGEN ##

print("## ANTWOORDEN ##")

print('Vraag 3')# Vraag 3
def FPH2O(t):
    return ((6.11 * 10.0**((7.5*t)/(237.3+t))) * 0.750061683)

def atps2btps(Vatps, ts, P, PH2O):
    return (Vatps * (310.0/(273.0+ts)) * ((P-PH2O) / (P-47.0)))
        
def atps2stpd(Vatps, ts, P, PH2O):
    return (Vatps * (273.0/(273.0+ts)) * ((P-PH2O) / (760.0)))
    
VEatps =   ((EINDLUCHT - STARTLUCHT) * 1000.0) + ((MINUTEN+(SECONDEN/60.0))   * (O2_VEL + CO2_VEL))
VEbtps = atps2btps(VEatps, TEMPERATUUR, LUCHTDRUK, FPH2O(TEMPERATUUR))
VEstpd = atps2stpd(VEatps, TEMPERATUUR, LUCHTDRUK, FPH2O(TEMPERATUUR))

VEtbl = pd.DataFrame(data=[[VEatps/TIJD, VEbtps/TIJD, VEstpd/TIJD],[VEatps, VEbtps, VEstpd]],
columns=['VEatps', 'VEbtps', 'VEstpd'],
index=['1.0 min',str(TIJD) + ' min'])
print(VEtbl)
print(" ")

print('Vraag 4')# vraag 4
def F(perc):
    return perc/100.0

def ve2vi(VE, O2i, CO2i, O2e, CO2e):
    return VE * (( 1.0 - (O2e + CO2e)) / (1.0 - (O2i + CO2i )))
    
VIatps = ve2vi(VEatps, F(O2_PERC_IN), F(CO2_PERC_IN), F(O2_PERC_OUT), F(CO2_PERC_OUT))
VIbtps = ve2vi(VEbtps, F(O2_PERC_IN), F(CO2_PERC_IN), F(O2_PERC_OUT), F(CO2_PERC_OUT))
VIstpd = ve2vi(VEstpd, F(O2_PERC_IN), F(CO2_PERC_IN), F(O2_PERC_OUT), F(CO2_PERC_OUT))

VItbl = pd.DataFrame(data=[[VIatps/TIJD, VIbtps/TIJD, VIstpd/TIJD],[VIatps, VIbtps, VIstpd]],
columns=['VIatps', 'VIbtps', 'VIstpd'],
index=['1.0 min',str(TIJD) + ' min'])
print(VItbl)
print(" ")

print('Vraag 5')         # vraag 5
def VO2(VI, VE, O2i, O2e):
    return (VI * O2i) - (VE * O2e)

def VCO2(VI, VE, CO2i, CO2e):
    return (VE * CO2e) - (VI * CO2i)

VO2atps = VO2(VIatps, VEatps, F(O2_PERC_IN), F(O2_PERC_OUT))/TIJD
VO2btps = VO2(VIbtps, VEbtps, F(O2_PERC_IN), F(O2_PERC_OUT))/TIJD
VO2stpd = VO2(VIstpd, VEstpd, F(O2_PERC_IN), F(O2_PERC_OUT))/TIJD

VO2tbl = pd.DataFrame(data=[[VO2atps, VO2btps, VO2stpd],[TIJD*VO2atps, TIJD*VO2btps, TIJD*VO2stpd]],
columns=['VO2atps','VO2btps','VO2stpd'],
index=['1.0 min', str(TIJD)+ ' min'])
print(VO2tbl)
print(" ")

print('Vraag 6')# vraag 6
VCO2atps = VCO2(VIatps, VEatps, F(CO2_PERC_IN), F(CO2_PERC_OUT))/TIJD
VCO2btps = VCO2(VIbtps, VEbtps, F(CO2_PERC_IN), F(CO2_PERC_OUT))/TIJD
VCO2stpd = VCO2(VIstpd, VEstpd, F(CO2_PERC_IN), F(CO2_PERC_OUT))/TIJD

VCO2tbl = pd.DataFrame(data=[[VCO2atps, VCO2btps, VCO2stpd],[TIJD*VCO2atps, TIJD*VCO2btps, TIJD*VCO2stpd]],
columns=['VCO2atps','VCO2btps','VCO2stpd'],
index=['1.0 min', str(TIJD)+ ' min'])
print(VCO2tbl)
print(" ")

print('Vraag 7')# vraag 7
RERatps = VCO2atps / VO2atps
RERbtps = VCO2btps / VO2btps
RERstpd = VCO2stpd / VO2stpd

RERtbl = pd.DataFrame(data=[RERatps, RERbtps, RERstpd], 
columns=['RER'], 
index=['atps','btps','stpd'])
print(RERtbl)
print(" ")

print"## Vanaf hier wordt alleen nog gewerkt in STPD eenheden ##"
print " "

print('Vraag 8')# vraag 8
def KCal(RQ, VO2):
    return ((1.1 * RQ) + 3.9) * VO2

KCal_min =   KCal(RERstpd, (VO2stpd))

KCaltbl = pd.DataFrame([KCal_min, TIJD*KCal_min], 
columns=['KCal'], 
index=['1.0 min',str(TIJD) + ' min'])
print(KCaltbl)
print(" ")

print('Vraag 9')# vraag 9
KCal_60_kg = KCal_min * 60.0 / GEWICHT
print "{0:<10} = {2:6.{1}f}".format('KCal_60_kg', PRECISION-1, KCal_60_kg)
print(" ")

print('Vraag 10')# vraag 10
KCal_dag = KCal_min * 60.0 * 24.0
print "{0:<10} = {2:6.{1}f}".format('KCal_dag', PRECISION-1, KCal_dag)
print(" ")

print('Vraag 11')# vraag 11
def DuboisDubois(gewicht, lengte):
    return (gewicht**0.425 * lengte**0.725)  * 0.007184
    "{0:<10} = {2:6.{1}f}".format('KCal_min', PRECISION-1, KCal_min)
KCal_60_M2 = (KCal_min * 60.0) / (DuboisDubois(GEWICHT, (LENGTE*100.0)))
print"Let op! formule van DuboisDubois: m^2 = 0.007184 * (gewicht^0.425 * lengte^0.725)"
print "{0:<10} = {2:6.{1}f}".format('KCal_60_M2', PRECISION-1, KCal_60_M2)
print(" ")

print('Finished!')