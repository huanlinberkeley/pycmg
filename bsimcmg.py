import re
from math import *

class BSIMCMG:
    """
    A BSIM-CMG version 110.0.0 model in Python. Model package can be downloaded at
    http://bsim.berkeley.edu/BSIMCMG/BSIMCMG110.0.0_20160101.tar.gz
    """

    def __repr__(self):
        return f'BSIMCMG()'

    def __init__(self, **kwargs):
        self.given = kwargs # parameters from modelcard

        # Instance parameters in Python (P001-P006, 6)
        self.vd = self.given.get('vd', 1.0) # P001
        self.vg = self.given.get('vg', 1.0) # P002
        self.vs = self.given.get('vs', 0.0) # P003
        self.vb = self.given.get('vb', 0.0) # P004
        self.temp = self.given.get('temp', 27.0) # P005
        self.vdd = self.given.get('vdd', 1.0) # P006

        # Instance parameters (I001-I024, 24)
        self.L = self.given.get('L', 3.0e-8) # I001
        self.D = self.given.get('D', 4.0e-8) # I002
        self.TFIN = self.given.get('TFIN', 1.5e-8) # I003
        self.FPITCH = self.given.get('FPITCH', 8.0e-8) # I004
        self.NF = self.given.get('NF', 1) # I005
        self.NFIN = self.given.get('NFIN', 1.0) # I006
        self.NGCON = self.given.get('NGCON', 1) # I007
        self.ASEO = self.given.get('ASEO', 0.0) # I008
        self.ADEO = self.given.get('ADEO', 0.0) # I009
        self.PSEO = self.given.get('PSEO', 0.0) # I010
        self.PDEO = self.given.get('PDEO', 0.0) # I011
        self.ASEJ = self.given.get('ASEJ', 0.0) # I012
        self.ADEJ = self.given.get('ADEJ', 0.0) # I013
        self.PSEJ = self.given.get('PSEJ', 0.0) # I014
        self.PDEJ = self.given.get('PDEJ', 0.0) # I015
        self.NRS = self.given.get('NRS', 0.0) # I021
        self.NRD = self.given.get('NRD', 0.0) # I022
        self.LRSD = self.given.get('LRSD', self.L) # I023
        self.NFINNOM = self.given.get('NFINNOM', 1.0) # I024

        # Model parameters (1027)
        self.XL = self.given.get('XL', 0.0) # M001
        self.DTEMP = self.given.get('DTEMP', 0.0) # M002
        self.DELVTRAND = self.given.get('DELVTRAND', 0.0) # M003
        self.U0MULT = self.given.get('U0MULT', 1.0) # M004
        self.IDS0MULT = self.given.get('IDS0MULT', 1.0) # M005
        self.TYPE = self.given.get('TYPE', 1) # M007
        self.BULKMOD = self.given.get('BULKMOD', 0) # M008
        self.GEOMOD = self.given.get('GEOMOD', 0) # M009
        self.RDSMOD = self.given.get('RDSMOD', 0) # M011
        self.ASYMMOD = self.given.get('ASYMMOD', 0) # M012
        self.IGCMOD = self.given.get('IGCMOD', 0) # M013
        self.IGBMOD = self.given.get('IGBMOD', 0) # M014
        self.GIDLMOD = self.given.get('GIDLMOD', 0) # M015
        self.IIMOD = self.given.get('IIMOD', 0) # M016
        self.TEMPMOD = self.given.get('TEMPMOD', 0) # M020
        self.RGATEMOD = self.given.get('RGATEMOD', 0) # M021
        self.RGEOMOD = self.given.get('RGEOMOD', 0) # M022
        self.IGCLAMP = self.given.get('IGCLAMP', 1) # M025
        self.LINT = self.given.get('LINT', 0.0) # M026
        self.LL = self.given.get('LL', 0.0) # M027
        self.LLN = self.given.get('LLN', 1.0) # M028
        self.DLC = self.given.get('DLC', 0.0) # M029
        self.DLBIN = self.given.get('DLBIN', 0.0) # M031
        self.LLC = self.given.get('LLC', 0.0) # M032
        self.EOT = self.given.get('EOT', 1.0e-9) # M033
        self.TOXP = self.given.get('TOXP', 1.2e-9) # M034
        self.EOTBOX = self.given.get('EOTBOX', 1.4e-7) # M035
        self.HFIN = self.given.get('HFIN', 3.0e-8) # M036
        self.FECH = self.given.get('FECH', 1.0) # M037
        self.DELTAW = self.given.get('DELTAW', 0.0) # M038
        self.NBODY = self.given.get('NBODY', 1e22) # M041
        self.NBODYN1 = self.given.get('NBODYN1', 0.0) # M042
        self.NBODYN2 = self.given.get('NBODYN2', 1.0e5) # M043
        self.NSD = self.given.get('NSD', 2.0e26) # M044
        self.PHIG = self.given.get('PHIG', 4.61) # M045
        self.PHIGL = self.given.get('PHIGL', 0.0) # M046
        self.PHIGLT = self.given.get('PHIGLT', 0.0) # M047
        self.PHIGN1 = self.given.get('PHIGN1', 0.0) # M048
        self.PHIGN2 = self.given.get('PHIGN2', 1.0e5) # M049
        self.EPSROX = self.given.get('EPSROX', 3.9) # M050
        self.EPSRSUB = self.given.get('EPSRSUB', 11.9) # M051
        self.EASUB = self.given.get('EASUB', 4.05) # M052
        self.NI0SUB = self.given.get('NI0SUB', 1.1e16) # M053
        self.BG0SUB = self.given.get('BG0SUB', 1.12) # M054
        self.NC0SUB = self.given.get('NC0SUB', 2.86e25) # M055
        self.NGATE = self.given.get('NGATE', 0) # M056
        self.IMIN = self.given.get('IMIN', 1.0e-15) # M057

        # Short channel effects (M058-M095, 38)
        self.CIT = self.given.get('CIT', 0.0) # M058
        self.CITR = self.given.get('CITR', self.CIT) # M059
        self.CDSC = self.given.get('CDSC', 7.0e-3) # M060
        self.CDSCN1 = self.given.get('CDSCN1', 0.0) # M061
        self.CDSCN2 = self.given.get('CDSCN2', 1.0e5) # M062
        self.CDSCD = self.given.get('CDSCD', 7.0e-3) # M063
        self.CDSCDN1 = self.given.get('CDSCDN1', 0.0) # M064
        self.CDSCDN2 = self.given.get('CDSCDN2', 1.0e5) # M065
        self.CDSCDR = self.given.get('CDSCDR', self.CDSCD) # M066
        self.CDSCDRN1 = self.given.get('CDSCDRN1', self.CDSCDN1) # M067
        self.CDSCDRN2 = self.given.get('CDSCDRN2', self.CDSCDN2) # M068
        self.DVT0 = self.given.get('DVT0', 0) # M069
        self.DVT1 = self.given.get('DVT1', 0.6) # M070
        self.DVT1SS = self.given.get('DVT1SS', self.DVT1) # M071
        self.PHIN = self.given.get('PHIN', 0.05) # M072
        self.ETA0 = self.given.get('ETA0', 0.6) # M073
        self.ETA0N1 = self.given.get('ETA0N1', 0.0) # M074
        self.ETA0N2 = self.given.get('ETA0N2', 1.0e5) # M075
        self.ETA0LT = self.given.get('ETA0LT', 0.0) # M076
        self.TETA0 = self.given.get('TETA0', 0.0) # M077
        self.ETA0R = self.given.get('ETA0R', self.ETA0) # M078
        self.TETA0R = self.given.get('TETA0R', self.TETA0) # M079
        self.DSUB = self.given.get('DSUB', 1.06) # M080
        self.DVTP0 = self.given.get('DVTP0', 0.0) # M081
        self.DVTP1 = self.given.get('DVTP1', 0.0) # M082
        self.ADVTP0 = self.given.get('ADVTP0', 0.0) # M083
        self.BDVTP0 = self.given.get('BDVTP0', 1.0e-7) # M084
        self.ADVTP1 = self.given.get('ADVTP1', 0) # M085
        self.BDVTP1 = self.given.get('BDVTP1', 1.0e-7) # M086
        self.DVTP2 = self.given.get('DVTP2', 0.0) # M087
        self.K1RSCE = self.given.get('K1RSCE', 0.0) # M088
        self.LPE0 = self.given.get('LPE0', 5.0e-9) # M089
        self.DVTSHIFT = self.given.get('DVTSHIFT', 0.0) # M090
        self.DVTSHIFTR = self.given.get('DVTSHIFTR', self.DVTSHIFT) # M091
        self.THETASCE = self.given.get('THETASCE', 0.0) # M092
        self.THETADIBL = self.given.get('THETADIBL', 0.0) # M093
        self.THETASW = self.given.get('THETASW', 0.0) # M094
        self.NVTM = self.given.get('NVTM', 0.0) # M095

        # Lateral non-uniform doping effect (IV-CV Vth shift) (M096-M105, 10)
        self.K0 = self.given.get('K0', 0.0) # M096
        self.K01 = self.given.get('K01', 0.0) # M097
        self.K0SI = self.given.get('K0SI', 1.0) # M098
        self.K0SI1 = self.given.get('K0SI1', 0.0) # M099
        self.K2SI = self.given.get('K2SI', self.K0SI) # M100
        self.K2SI1 = self.given.get('K2SI1', self.K0SI1) # M101
        self.K0SISAT = self.given.get('K0SISAT', 0.0) # M102
        self.K0SISAT1 = self.given.get('K0SISAT1', 0.0) # M103
        self.K2SISAT = self.given.get('K2SISAT', self.K0SISAT) # M104
        self.K2SISAT1 = self.given.get('K2SISAT1', self.K0SISAT1) # M105

        # Body effect for MG devices on bulk substrate (ex: FinFETs on BULK) (M106-M112, 7)
        self.PHIBE = self.given.get('PHIBE', 0.7) # M106
        self.K1 = self.given.get('K1', 1.0e-6) # M107
        self.K11 = self.given.get('K11', 0.0) # M108
        self.K2SAT = self.given.get('K2SAT', 0.0) # M109
        self.K2SAT1 = self.given.get('K2SAT1', 0.0) # M110
        self.K2 = self.given.get('K2', 0.0) # M111
        self.K21 = self.given.get('K21', 0.0) # M112

        # Quantum mechanical effects (M113-M122, 10)
        self.QMFACTOR = self.given.get('QMFACTOR', 0.0) # M113
        self.QMTCENCV = self.given.get('QMTCENCV', 0.0) # M114
        self.QMTCENCVA = self.given.get('QMTCENCVA', 0.0) # M115
        self.AQMTCEN = self.given.get('AQMTCEN', 0.0) # M116
        self.BQMTCEN = self.given.get('BQMTCEN', 1.2e-8) # M117
        self.ETAQM = self.given.get('ETAQM', 0.54) # M118
        self.QM0 = self.given.get('QM0', 1.0e-3) # M119
        self.PQM = self.given.get('PQM', 0.66) # M120
        self.QM0ACC = self.given.get('QM0ACC', 1.0e-3) # M121
        self.PQMACC = self.given.get('PQMACC', 0.66) # M122

        # Velocity saturation model (M123-M167, 45)
        self.VSAT = self.given.get('VSAT', 8.5e4) # M123
        self.VSATR = self.given.get('VSATR', self.VSAT) # M124
        self.VSATN1 = self.given.get('VSATN1', 0.0) # M125
        self.VSATN2 = self.given.get('VSATN2', 1.0e5) # M126
        self.VSATRN1 = self.given.get('VSATRN1', self.VSATN1) # M127
        self.VSATRN2 = self.given.get('VSATRN2', self.VSATN2) # M128
        self.AVSAT = self.given.get('AVSAT', 0.0) # M129
        self.BVSAT = self.given.get('BVSAT', 1.0e-7) # M130
        self.VSAT1 = self.given.get('VSAT1', self.VSAT) # M131
        self.VSAT1N1 = self.given.get('VSAT1N1', self.VSATN1) # M132
        self.VSAT1N2 = self.given.get('VSAT1N2', self.VSATN2) # M133
        self.VSAT1R = self.given.get('VSAT1R', self.VSAT1) # M134
        self.VSAT1RN1 = self.given.get('VSAT1RN1', self.VSAT1N1) # M135
        self.VSAT1RN2 = self.given.get('VSAT1RN2', self.VSAT1N2) # M136
        self.AVSAT1 = self.given.get('AVSAT1', self.AVSAT) # M137
        self.BVSAT1 = self.given.get('BVSAT1', self.BVSAT) # M138
        self.DELTAVSAT = self.given.get('DELTAVSAT', 1.0) # M139
        self.PSAT = self.given.get('PSAT', 2.0) # M140
        self.APSAT = self.given.get('APSAT', 0.0) # M141
        self.BPSAT = self.given.get('BPSAT', 1.0) # M142
        self.KSATIV = self.given.get('KSATIV', 1.0) # M143
        self.KSATIVR = self.given.get('KSATIVR', self.KSATIV) # M144
        self.MEXP = self.given.get('MEXP', 4.0) # M152
        self.AMEXP = self.given.get('AMEXP', 0.0) # M153
        self.BMEXP = self.given.get('BMEXP', 1.0) # M154
        self.MEXPR = self.given.get('MEXPR', self.MEXP) # M155
        self.AMEXPR = self.given.get('AMEXPR', self.AMEXP) # M156
        self.BMEXPR = self.given.get('BMEXPR', self.BMEXP) # M157
        self.PTWG = self.given.get('PTWG', 0.0) # M158
        self.PTWGR = self.given.get('PTWGR', self.PTWG) # M159
        self.APTWG = self.given.get('APTWG', 0.0) # M160
        self.BPTWG = self.given.get('BPTWG', 1.0e-7) # M161
        self.AT = self.given.get('AT', -1.56e-3) # M162
        self.ATR = self.given.get('ATR', self.AT) # M163
        self.ATCV = self.given.get('ATCV', self.AT) # M164
        self.TMEXP = self.given.get('TMEXP', 0.0) # M165
        self.TMEXPR = self.given.get('TMEXPR', self.TMEXP) # M166
        self.PTWGT = self.given.get('PTWGT', 4.0e-3) # M167

        # Mobility model (M168-M213, 46)
        self.U0 = self.given.get('U0', 3.0e-2) # M168
        self.U0R = self.given.get('U0R', self.U0) # M169
        self.U0N1 = self.given.get('U0N1', 0.0) # M170
        self.U0N1R = self.given.get('U0N1R', self.U0N1) # M171
        self.U0N2 = self.given.get('U0N2', 1.0e5) # M172
        self.U0N2R = self.given.get('U0N2R', self.U0N2) # M173
        self.U0LT = self.given.get('U0LT', 0.0) # M174
        self.ETAMOB = self.given.get('ETAMOB', 2.0) # M175
        self.UP = self.given.get('UP', 0.0) # M176
        self.LPA = self.given.get('LPA', 1.0) # M177
        self.UPR = self.given.get('UPR', self.UP) # M178
        self.LPAR = self.given.get('LPAR', self.LPA) # M179
        self.UA = self.given.get('UA', 0.3) # M180
        self.UAR = self.given.get('UAR', self.UA) # M181
        self.AUA = self.given.get('AUA', 0.0) # M182
        self.AUAR = self.given.get('AUAR', self.AUA) # M183
        self.BUA = self.given.get('BUA', 1.0e-7) # M184
        self.BUAR = self.given.get('BUAR', self.BUA) # M185
        self.UC = self.given.get('UC', 0.0) # M186
        self.UCR = self.given.get('UCR', self.UC) # M187
        self.EU = self.given.get('EU', 2.5) # M188
        self.EUR = self.given.get('EUR', self.EU) # M189
        self.AEU = self.given.get('AEU', 0.0) # M190
        self.AEUR = self.given.get('AEUR', self.AEU) # M191
        self.BEU = self.given.get('BEU', 1.0e-7) # M192
        self.BEUR = self.given.get('BEUR', self.BEU) # M193
        self.UD = self.given.get('UD', 0.0) # M194
        self.UDR = self.given.get('UDR', self.UD) # M195
        self.AUD = self.given.get('AUD', 0.0) # M196
        self.AUDR = self.given.get('AUDR', self.AUD) # M197
        self.BUD = self.given.get('BUD', 5.0e-8) # M198
        self.BUDR = self.given.get('BUDR', self.BUD) # M199
        self.UCS = self.given.get('UCS', 1.0) # M200
        self.UTE = self.given.get('UTE', 0.0) # M201
        self.UTER = self.given.get('UTER', self.UTE) # M202
        self.UTL = self.given.get('UTL', -1.5e-3) # M203
        self.UTLR = self.given.get('UTLR', self.UTL) # M204
        self.EMOBT = self.given.get('EMOBT', 0.0) # M205
        self.UA1 = self.given.get('UA1', 1.032e-3) # M206
        self.UA1R = self.given.get('UA1R', self.UA1) # M207
        self.UC1 = self.given.get('UC1', 5.6e-11) # M208
        self.UC1R = self.given.get('UC1R', self.UC1) # M209
        self.UD1 = self.given.get('UD1', 0.0) # M210
        self.UD1R = self.given.get('UD1R', self.UD1) # M211
        self.UCSTE = self.given.get('UCSTE', -4.775e-3) # M212
        self.CHARGEWF = self.given.get('CHARGEWF', 0.0) # M213

        # Access resistance model (M214-M237, 24)
        self.RDSWMIN = self.given.get('RDSWMIN', 0.0) # M214
        self.RDSW = self.given.get('RDSW', 1.0e2) # M215
        self.ARDSW = self.given.get('ARDSW', 0.0) # M216
        self.BRDSW = self.given.get('BRDSW', 1.0e-7) # M217
        self.RSWMIN = self.given.get('RSWMIN', 0.0) # M218
        self.RSW = self.given.get('RSW', 5.0e1) # M219
        self.ARSW = self.given.get('ARSW', 0.0) # M220
        self.BRSW = self.given.get('BRSW', 1.0e-7) # M221
        self.RDWMIN = self.given.get('RDWMIN', 0.0) # M222
        self.RDW = self.given.get('RDW', 5.0e1) # M223
        self.ARDW = self.given.get('ARDW', 0.0) # M224
        self.BRDW = self.given.get('BRDW', 1.0e-7) # M225
        self.RSDR = self.given.get('RSDR', 0.0) # M226
        self.RSDRR = self.given.get('RSDRR', self.RSDR) # M227
        self.RDDR = self.given.get('RDDR', self.RSDR) # M228
        self.RDDRR = self.given.get('RDDRR', self.RDDR) # M229
        self.PRSDR = self.given.get('PRSDR', 1.0) # M230
        self.PRDDR = self.given.get('PRDDR', self.PRSDR) # M231
        self.PRWGS = self.given.get('PRWGS', 0.0) # M232
        self.PRWGD = self.given.get('PRWGD', self.PRWGS) # M233
        self.WR = self.given.get('WR', 1.0) # M234
        self.PRT = self.given.get('PRT', 1.0e-3) # M235
        self.TRSDR = self.given.get('TRSDR', 0.0) # M236
        self.TRDDR = self.given.get('TRDDR', self.TRSDR) # M237

        # DIBL model (M238-M243, 6)
        self.PDIBL1 = self.given.get('PDIBL1', 1.3) # M238
        self.PDIBL1R = self.given.get('PDIBL1R', self.PDIBL1) # M239
        self.PDIBL2 = self.given.get('PDIBL2', 2.0e-4) # M240
        self.PDIBL2R = self.given.get('PDIBL2R', self.PDIBL2) # M241
        self.DROUT = self.given.get('DROUT', 1.06) # M242
        self.PVAG = self.given.get('PVAG', 1.0) # M243

        # Channel length modulation effect (M244-M251, 8)
        self.PCLM = self.given.get('PCLM', 1.3e-2) # M244
        self.PCLMR = self.given.get('PCLMR', self.PCLM) # M245
        self.APCLM = self.given.get('APCLM', 0.0) # M246
        self.APCLMR = self.given.get('APCLMR', self.APCLM) # M247
        self.BPCLM = self.given.get('BPCLM', 1.0e-7) # M248
        self.BPCLMR = self.given.get('BPCLMR', self.BPCLM) # M249
        self.PCLMG = self.given.get('PCLMG', 0.0) # M250

        # Non-saturation effect (M252-M255, 4)
        self.A1 = self.given.get('A1', 0.0) # M252
        self.A11 = self.given.get('A11', 0.0) # M253
        self.A2 = self.given.get('A2', 0.0) # M254
        self.A21 = self.given.get('A21', 0.0) # M255

        # Gate electrode resistance (M256-M257, 2)
        self.RGEXT = self.given.get('RGEXT', 0.0) # M256
        self.RGFIN = self.given.get('RGFIN', 1.0e-3) # M257

        # Geometry dependent source/drain resistance of RGEOMOD = 0 (M258-M259, 2)
        self.RSHS = self.given.get('RSHS', 0.0) # M258
        self.RSHD = self.given.get('RSHD', self.RSHS) # M259

        # Geometry dependent source/drain resistance of RGEOMOD = 1 for variability modeling
        # These parameters are shared with CGEOMOD = 2 (M260-M284, 25)
        self.HEPI = self.given.get('HEPI', 1.0e-8) # M260
        self.TSILI = self.given.get('TSILI', 1.0e-8) # M261
        self.RHOC = self.given.get('RHOC', 1.0e-12) # M262
        self.RHORSD = self.given.get('RHORSD', 1.0) # M263
        self.CRATIO = self.given.get('CRATIO', 0.5) # M264
        self.DELTAPRSD = self.given.get('DELTAPRSD', 0.0) # M265
        self.SDTERM = self.given.get('SDTERM', 0) # M266
        self.LSP = self.given.get('LSP', 0.2 * (self.L + self.XL)) # M267
        self.EPSRSP = self.given.get('EPSRSP', 3.9) # M268
        self.TGATE = self.given.get('TGATE', 3.0e-8) # M269
        self.TMASK = self.given.get('TMASK', 3.0e-8) # M270
        self.ASILIEND = self.given.get('ASILIEND', 0.0) # M271
        self.ARSDEND = self.given.get('ARSDEND', 0.0) # M272
        self.PRSDEND = self.given.get('PRSDEND', 0.0) # M273
        self.NSDE = self.given.get('NSDE', 2.0e25) # M274
        self.RGEOA = self.given.get('RGEOA', 1.0) # M275
        self.RGEOB = self.given.get('RGEOB', 0.0) # M276
        self.RGEOC = self.given.get('RGEOC', 0.0) # M277
        self.RGEOD = self.given.get('RGEOD', 0.0) # M278
        self.RGEOE = self.given.get('RGEOE', 0.0) # M279
        self.CGEOA = self.given.get('CGEOA', 1.0) # M280
        self.CGEOB = self.given.get('CGEOB', 0.0) # M281
        self.CGEOC = self.given.get('CGEOC', 0.0) # M282
        self.CGEOD = self.given.get('CGEOD', 0.0) # M283
        self.CGEOE = self.given.get('CGEOE', 1.0) # M284

        # Gate current (M285-M316, 32)
        self.AIGBINV = self.given.get('AIGBINV', 1.11e-2) # M285
        self.AIGBINV1 = self.given.get('AIGBINV1', 0.0) # M286
        self.BIGBINV = self.given.get('BIGBINV', 9.49e-4) # M287
        self.CIGBINV = self.given.get('CIGBINV', 6.0e-3) # M288
        self.EIGBINV = self.given.get('EIGBINV', 1.1) # M289
        self.NIGBINV = self.given.get('NIGBINV', 3.0) # M290
        self.AIGBACC = self.given.get('AIGBACC', 1.36e-2) # M291
        self.AIGBACC1 = self.given.get('AIGBACC1', 0.0) # M292
        self.BIGBACC = self.given.get('BIGBACC', 1.71e-3) # M293
        self.CIGBACC = self.given.get('CIGBACC', 7.5e-2) # M294
        self.NIGBACC = self.given.get('NIGBACC', 1.0) # M295
        self.AIGC = self.given.get('AIGC', 1.36e-2) # M296
        self.AIGC1 = self.given.get('AIGC1', 0.0) # M297
        self.BIGC = self.given.get('BIGC', 1.71e-3) # M298
        self.CIGC = self.given.get('CIGC', 7.5e-2) # M299
        self.PIGCD = self.given.get('PIGCD', 1.0) # M300
        self.DLCIGS = self.given.get('DLCIGS', 0.0) # M301
        self.AIGS = self.given.get('AIGS', 1.36e-2) # M302
        self.AIGS1 = self.given.get('AIGS1', 0.0) # M303
        self.BIGS = self.given.get('BIGS', 1.71e-3) # M304
        self.CIGS = self.given.get('CIGS', 7.5e-2) # M305
        self.DLCIGD = self.given.get('DLCIGD', self.DLCIGS) # M306
        self.AIGD = self.given.get('AIGS', self.AIGS) # M307
        self.AIGD1 = self.given.get('AIGS1', self.AIGS1) # M308
        self.BIGD = self.given.get('BIGS', self.BIGS) # M309
        self.CIGD = self.given.get('CIGS', self.CIGS) # M310
        self.VFBSD = self.given.get('VFBSD', 0.0) # M311
        self.VFBSDCV = self.given.get('VFBSDCV', self.VFBSD) # M312
        self.TOXREF = self.given.get('TOXREF', 1.2e-9) # M313
        self.TOXG = self.given.get('TOXG', self.TOXP) # M314
        self.NTOX = self.given.get('NTOX', 1.0) # M315
        self.POXEDGE = self.given.get('POXEDGE', 1.0) # M316

        # GIDL/GISL current (M317-M326, 10)
        self.AGISL = self.given.get('AGISL', 6.055e-12) # M317
        self.BGISL = self.given.get('BGISL', 3.0e8) # M318
        self.CGISL = self.given.get('CGISL', 0.5) # M319
        self.EGISL = self.given.get('EGISL', 0.2) # M320
        self.PGISL = self.given.get('PGISL', 1.0) # M321
        self.AGIDL = self.given.get('AGIDL', self.AGISL) # M322
        self.BGIDL = self.given.get('BGIDL', self.BGISL) # M323
        self.CGIDL = self.given.get('CGIDL', self.CGISL) # M324
        self.EGIDL = self.given.get('EGIDL', self.EGISL) # M325
        self.PGIDL = self.given.get('PGIDL', self.PGISL) # M326

        # Impact ionization current (21)
        # IIMOD = 1 (M327-M331, 5)
        self.ALPHA0 = self.given.get('ALPHA0', 0.0) # M327
        self.ALPHA01 = self.given.get('ALPHA01', 0.0) # M328
        self.ALPHA1 = self.given.get('ALPHA1', 0.0) # M329
        self.ALPHA11 = self.given.get('ALPHA11', 0.0) # M330
        self.BETA0 = self.given.get('BETA0', 0.0) # M331
        # IIMOD = 2 (M332-M347, 16)
        self.ALPHAII0 = self.given.get('ALPHAII0', 0.0) # M332
        self.ALPHAII01 = self.given.get('ALPHAII01', 0.0) # M333
        self.ALPHAII1 = self.given.get('ALPHAII1', 0.0) # M334
        self.ALPHAII11 = self.given.get('ALPHAII11', 0.0) # M335
        self.BETAII0 = self.given.get('BETAII0', 0.0) # M336
        self.BETAII1 = self.given.get('BETAII1', 0.0) # M337
        self.BETAII2 = self.given.get('BETAII2', 0.1) # M338
        self.ESATII = self.given.get('ESATII', 1.0e7) # M339
        self.LII = self.given.get('LII', 0.5e-9) # M340
        self.SII0 = self.given.get('SII0', 0.5) # M341
        self.SII1 = self.given.get('SII1', 0.1) # M342
        self.SII2 = self.given.get('SII2', 0.0) # M343
        self.SIID = self.given.get('SIID', 0.0) # M344
        self.IIMOD2CLAMP1 = self.given.get('IIMOD2CLAMP1', 0.1) # M345
        self.IIMOD2CLAMP2 = self.given.get('IIMOD2CLAMP2', 0.1) # M346
        self.IIMOD2CLAMP3 = self.given.get('IIMOD2CLAMP3', 0.1) # M347

        # Accumulation capacitance (M348-M349, 2)
        self.EOTACC = self.given.get('EOTACC', self.EOT) # M348
        self.DELVFBACC = self.given.get('DELVFBACC', 0.0) # M349

        # Junction current (M393-M408, 16)
        self.JSS = self.given.get('JSS', 1.0e-4) # M393
        self.JSD = self.given.get('JSD', self.JSS) # M394
        self.JSWS = self.given.get('JSWS', 0.0) # M395
        self.JSWD = self.given.get('JSWD', self.JSWS) # M396
        self.JSWGS = self.given.get('JSWGS', 0.0) # M397
        self.JSWGD = self.given.get('JSWGD', self.JSWGS) # M398
        self.NJS = self.given.get('NJS', 1.0) # M399
        self.NJD = self.given.get('NJD', self.NJS) # M400
        self.IJTHSFWD = self.given.get('IJTHSFWD', 0.1) # M401
        self.IJTHDFWD = self.given.get('IJTHDFWD', self.IJTHSFWD) # M402
        self.IJTHSREV = self.given.get('IJTHSREV', 0.1) # M403
        self.IJTHDREV = self.given.get('IJTHDREV', self.IJTHSREV) # M404
        self.BVS = self.given.get('BVS', 1.0e1) # M405
        self.BVD = self.given.get('BVD', self.BVS) # M406
        self.XJBVS = self.given.get('XJBVS', 1.0) # M407
        self.XJBVD = self.given.get('XJBVD', self.XJBVS) # M408

        # Tunneling component of junction current (M409-M427, 19)
        self.JTSS = self.given.get('JTSS', 0.0) # M409
        self.JTSD = self.given.get('JTSD', self.JTSS) # M410
        self.JTSSWS = self.given.get('JTSSWS', 0.0) # M411
        self.JTSSWD = self.given.get('JTSSWD', self.JTSSWS) # M412
        self.JTSSWGS = self.given.get('JTSSWGS', 0.0) # M413
        self.JTSSWGD = self.given.get('JTSSWGD', self.JTSSWGS) # M414
        self.JTWEFF = self.given.get('JTWEFF', 0.0) # M415
        self.NJTS = self.given.get('NJTS', 2.0e1) # M416
        self.NJTSD = self.given.get('NJTSD', self.NJTS) # M417
        self.NJTSSW = self.given.get('NJTSSW', 2.0e1) # M418
        self.NJTSSWD = self.given.get('NJTSSWD', self.NJTSSW) # M419
        self.NJTSSWG = self.given.get('NJTSSWG', 2.0e1) # M420
        self.NJTSSWGD = self.given.get('NJTSSWGD', self.NJTSSWG) # M421
        self.VTSS = self.given.get('VTSS', 1.0e1) # M422
        self.VTSD = self.given.get('VTSD', self.VTSS) # M423
        self.VTSSWS = self.given.get('VTSSWS', 1.0e1) # M424
        self.VTSSWD = self.given.get('VTSSWD', self.VTSSWS) # M425
        self.VTSSWGS = self.given.get('VTSSWGS', 1.0e1) # M426
        self.VTSSWGD = self.given.get('VTSSWGD', self.VTSSWGS) # M427

        # Recombination-generation current (M428-M431, 4)
        self.LINTIGEN = self.given.get('LINTIGEN', 0.0) # M428
        self.NTGEN = self.given.get('NTGEN', 1.0) # M429
        self.AIGEN = self.given.get('AIGEN', 0.0) # M430
        self.BIGEN = self.given.get('BIGEN', 0.0) # M431

        # Temperature effects (M449-M478, 30)
        self.TNOM = self.given.get('TNOM', 27.0) # M449
        self.TBGASUB = self.given.get('TBGASUB', 7.02e-4) # M450
        self.TBGBSUB = self.given.get('TBGBSUB', 1.108e3) # M451
        self.KT1 = self.given.get('KT1', 0.0) # M452
        self.KT1L = self.given.get('KT1L', 0.0) # M453
        self.TSS = self.given.get('TSS', 0.0) # M454
        self.IIT = self.given.get('IIT', -0.5) # M455
        self.TII = self.given.get('TII', 0.0) # M456
        self.TGIDL = self.given.get('TGIDL', -0.003) # M457
        self.IGT = self.given.get('IGT', 2.5) # M458
        self.TCJ = self.given.get('TCJ', 0.0) # M459
        self.TCJSW = self.given.get('TCJSW', 0.0) # M460
        self.TCJSWG = self.given.get('TCJSWG', 0.0) # M461
        self.TPB = self.given.get('TPB', 0.0) # M462
        self.TPBSW = self.given.get('TPBSW', 0.0) # M463
        self.TPBSWG = self.given.get('TPBSWG', 0.0) # M464
        self.XTIS = self.given.get('XTIS', 3.0) # M465
        self.XTID = self.given.get('XTID', self.XTIS) # M466
        self.XTSS = self.given.get('XTSS', 0.02) # M467
        self.XTSD = self.given.get('XTSD', self.XTSS) # M468
        self.XTSSWS = self.given.get('XTSSWS', 0.02) # M469
        self.XTSSWD = self.given.get('XTSSWD', self.XTSSWS) # M470
        self.XTSSWGS = self.given.get('XTSSWGS', 0.02) # M471
        self.XTSSWGD = self.given.get('XTSSWGD', self.XTSSWGS) # M472
        self.TNJTS = self.given.get('TNJTS', 0.0) # M473
        self.TNJTSD = self.given.get('TNJTSD', self.TNJTS) # M474
        self.TNJTSSW = self.given.get('TNJTSSW', 0.0) # M475
        self.TNJTSSWD = self.given.get('TNJTSSWD', self.TNJTSSW) # M476
        self.TNJTSSWG = self.given.get('TNJTSSWG', 0.0) # M477
        self.TNJTSSWGD = self.given.get('TNJTSSWGD', self.TNJTSSWG) # M478

        # Unified model (M484-M490, 7)
        self.ACH_UFCM = self.given.get('ACH_UFCM', 1.0) # M484
        self.CINS_UFCM = self.given.get('CINS_UFCM', 1.0) # M485
        self.W_UFCM = self.given.get('W_UFCM', 1.0) # M486
        self.TFIN_TOP = self.given.get('TFIN_TOP', 1.5e-8) # M487
        self.TFIN_BASE = self.given.get('TFIN_BASE', 1.5e-8) # M488
        self.QMFACTORCV = self.given.get('QMFACTORCV', 0.0) # M489
        self.ALPHA_UFCM = self.given.get('ALPHA_UFCM', 0.5556) # M490

        # Binning parameters (M491-M1027, 537)
        self.LNBODY = self.given.get('LNBODY', 0.0) # M491
        self.NNBODY = self.given.get('NNBODY', 0.0) # M492
        self.PNBODY = self.given.get('PNBODY', 0.0) # M493
        self.LPHIG = self.given.get('LPHIG', 0.0) # M494
        self.NPHIG = self.given.get('NPHIG', 0.0) # M495
        self.PPHIG = self.given.get('PPHIG', 0.0) # M496
        self.LNGATE = self.given.get('LNGATE', 0.0) # M497
        self.NNGATE = self.given.get('NNGATE', 0.0) # M498
        self.PNGATE = self.given.get('PNGATE', 0.0) # M499
        self.LCIT = self.given.get('LCIT', 0.0) # M500
        self.NCIT = self.given.get('NCIT', 0.0) # M501
        self.PCIT = self.given.get('PCIT', 0.0) # M502
        self.LCDSC = self.given.get('LCDSC', 0.0) # M503
        self.NCDSC = self.given.get('NCDSC', 0.0) # M504
        self.PCDSC = self.given.get('PCDSC', 0.0) # M505
        self.LCDSCD = self.given.get('LCDSCD', 0.0) # M506
        self.NCDSCD = self.given.get('NCDSCD', 0.0) # M507
        self.PCDSCD = self.given.get('PCDSCD', 0.0) # M508
        self.LDVT0 = self.given.get('LDVT0', 0.0) # M509
        self.NDVT0 = self.given.get('NDVT0', 0.0) # M510
        self.PDVT0 = self.given.get('PDVT0', 0.0) # M511
        self.LDVT1 = self.given.get('LDVT1', 0.0) # M512
        self.NDVT1 = self.given.get('NDVT1', 0.0) # M513
        self.PDVT1 = self.given.get('PDVT1', 0.0) # M514
        self.LPHIN = self.given.get('LPHIN', 0.0) # M515
        self.NPHIN = self.given.get('NPHIN', 0.0) # M516
        self.PPHIN = self.given.get('PPHIN', 0.0) # M517
        self.LETA0 = self.given.get('LETA0', 0.0) # M518
        self.NETA0 = self.given.get('NETA0', 0.0) # M519
        self.PETA0 = self.given.get('PETA0', 0.0) # M520
        self.LDSUB = self.given.get('LDSUB', 0.0) # M521
        self.NDSUB = self.given.get('NDSUB', 0.0) # M522
        self.PDSUB = self.given.get('PDSUB', 0.0) # M523
        self.LK1RSCE = self.given.get('LK1RSCE', 0.0) # M524
        self.NK1RSCE = self.given.get('NK1RSCE', 0.0) # M525
        self.PK1RSCE = self.given.get('PK1RSCE', 0.0) # M526
        self.LLPE0 = self.given.get('LLPE0', 0.0) # M527
        self.NLPE0 = self.given.get('NLPE0', 0.0) # M528
        self.PLPE0 = self.given.get('PLPE0', 0.0) # M529
        self.LDVTSHIFT = self.given.get('LDVTSHIFT', 0.0) # M530
        self.NDVTSHIFT = self.given.get('NDVTSHIFT', 0.0) # M531
        self.PDVTSHIFT = self.given.get('PDVTSHIFT', 0.0) # M532
        self.LPHIBE = self.given.get('LPHIBE', 0.0) # M533
        self.NPHIBE = self.given.get('NPHIBE', 0.0) # M534
        self.PPHIBE = self.given.get('PPHIBE', 0.0) # M535
        self.LK0 = self.given.get('LK0', 0.0) # M536
        self.NK0 = self.given.get('NK0', 0.0) # M537
        self.PK0 = self.given.get('PK0', 0.0) # M538
        self.LK01 = self.given.get('LK01', 0.0) # M539
        self.NK01 = self.given.get('NK01', 0.0) # M540
        self.PK01 = self.given.get('PK01', 0.0) # M541
        self.LK0SI = self.given.get('LK0SI', 0.0) # M542
        self.NK0SI = self.given.get('NK0SI', 0.0) # M543
        self.PK0SI = self.given.get('PK0SI', 0.0) # M544
        self.LK0SI1 = self.given.get('LK0SI1', 0.0) # M545
        self.NK0SI1 = self.given.get('NK0SI1', 0.0) # M546
        self.PK0SI1 = self.given.get('PK0SI1', 0.0) # M547
        self.LK1 = self.given.get('LK1', 0.0) # M548
        self.NK1 = self.given.get('NK1', 0.0) # M549
        self.PK1 = self.given.get('PK1', 0.0) # M550
        self.LK11 = self.given.get('LK11', 0.0) # M551
        self.NK11 = self.given.get('NK11', 0.0) # M552
        self.PK11 = self.given.get('PK11', 0.0) # M553
        self.LK0SISAT = self.given.get('LK0SISAT', 0.0) # M554
        self.NK0SISAT = self.given.get('NK0SISAT', 0.0) # M555
        self.PK0SISAT = self.given.get('PK0SISAT', 0.0) # M556
        self.LK0SISAT1 = self.given.get('LK0SISAT1', 0.0) # M557
        self.NK0SISAT1 = self.given.get('NK0SISAT1', 0.0) # M558
        self.PK0SISAT1 = self.given.get('PK0SISAT1', 0.0) # M559
        self.LK2SAT = self.given.get('LK2SAT', 0.0) # M560
        self.NK2SAT = self.given.get('NK2SAT', 0.0) # M561
        self.PK2SAT = self.given.get('PK2SAT', 0.0) # M562
        self.LK2SAT1 = self.given.get('LK2SAT1', 0.0) # M563
        self.NK2SAT1 = self.given.get('NK2SAT1', 0.0) # M564
        self.PK2SAT1 = self.given.get('PK2SAT1', 0.0) # M565
        self.LK2 = self.given.get('LK2', 0.0) # M566
        self.NK2 = self.given.get('NK2', 0.0) # M567
        self.PK2 = self.given.get('PK2', 0.0) # M568
        self.LK21 = self.given.get('LK21', 0.0) # M569
        self.NK21 = self.given.get('NK21', 0.0) # M570
        self.PK21 = self.given.get('PK21', 0.0) # M571
        self.LDVTB = self.given.get('LDVTB', 0.0) # M572
        self.NDVTB = self.given.get('NDVTB', 0.0) # M573
        self.PDVTB = self.given.get('PDVTB', 0.0) # M574
        self.LLPEB = self.given.get('LLPEB', 0.0) # M575
        self.NLPEB = self.given.get('NLPEB', 0.0) # M576
        self.PLPEB = self.given.get('PLPEB', 0.0) # M577
        self.LQMFACTOR = self.given.get('LQMFACTOR', 0.0) # M578
        self.NQMFACTOR = self.given.get('NQMFACTOR', 0.0) # M579
        self.PQMFACTOR = self.given.get('PQMFACTOR', 0.0) # M580
        self.LQMTCENCV = self.given.get('LQMTCENCV', 0.0) # M581
        self.NQMTCENCV = self.given.get('NQMTCENCV', 0.0) # M582
        self.PQMTCENCV = self.given.get('PQMTCENCV', 0.0) # M583
        self.LQMTCENCVA = self.given.get('LQMTCENCVA', 0.0) # M584
        self.NQMTCENCVA = self.given.get('NQMTCENCVA', 0.0) # M585
        self.PQMTCENCVA = self.given.get('PQMTCENCVA', 0.0) # M586
        self.LVSAT = self.given.get('LVSAT', 0.0) # M587
        self.NVSAT = self.given.get('NVSAT', 0.0) # M588
        self.PVSAT = self.given.get('PVSAT', 0.0) # M589
        self.LPSAT = self.given.get('LPSAT', 0.0) # M590
        self.NPSAT = self.given.get('NPSAT', 0.0) # M591
        self.PPSAT = self.given.get('PPSAT', 0.0) # M592
        self.LDELTAVSAT = self.given.get('LDELTAVSAT', 0.0) # M593
        self.NDELTAVSAT = self.given.get('NDELTAVSAT', 0.0) # M594
        self.PDELTAVSAT = self.given.get('PDELTAVSAT', 0.0) # M595
        self.LKSATIV = self.given.get('LKSATIV', 0.0) # M596
        self.NKSATIV = self.given.get('NKSATIV', 0.0) # M597
        self.PKSATIV = self.given.get('PKSATIV', 0.0) # M598
        self.LMEXP = self.given.get('LMEXP', 0.0) # M608
        self.NMEXP = self.given.get('NMEXP', 0.0) # M609
        self.PMEXP = self.given.get('PMEXP', 0.0) # M610
        self.LPTWG = self.given.get('LPTWG', 0.0) # M611
        self.NPTWG = self.given.get('NPTWG', 0.0) # M612
        self.PPTWG = self.given.get('PPTWG', 0.0) # M613
        self.LU0 = self.given.get('LU0', 0.0) # M614
        self.NU0 = self.given.get('NU0', 0.0) # M615
        self.PU0 = self.given.get('PU0', 0.0) # M616
        self.LETAMOB = self.given.get('LETAMOB', 0.0) # M617
        self.NETAMOB = self.given.get('NETAMOB', 0.0) # M618
        self.PETAMOB = self.given.get('PETAMOB', 0.0) # M619
        self.LUP = self.given.get('LUP', 0.0) # M620
        self.NUP = self.given.get('NUP', 0.0) # M621
        self.PUP = self.given.get('PUP', 0.0) # M622
        self.LUA = self.given.get('LUA', 0.0) # M623
        self.NUA = self.given.get('NUA', 0.0) # M624
        self.PUA = self.given.get('PUA', 0.0) # M625
        self.LUC = self.given.get('LUC', 0.0) # M626
        self.NUC = self.given.get('NUC', 0.0) # M627
        self.PUC = self.given.get('PUC', 0.0) # M628
        self.LEU = self.given.get('LEU', 0.0) # M629
        self.NEU = self.given.get('NEU', 0.0) # M630
        self.PEU = self.given.get('PEU', 0.0) # M631
        self.LUD = self.given.get('LUD', 0.0) # M632
        self.NUD = self.given.get('NUD', 0.0) # M633
        self.PUD = self.given.get('PUD', 0.0) # M634
        self.LUCS = self.given.get('LUCS', 0.0) # M635
        self.NUCS = self.given.get('NUCS', 0.0) # M636
        self.PUCS = self.given.get('PUCS', 0.0) # M637
        self.LPCLM = self.given.get('LPCLM', 0.0) # M638
        self.NPCLM = self.given.get('NPCLM', 0.0) # M639
        self.PPCLM = self.given.get('PPCLM', 0.0) # M640
        self.LPCLMG = self.given.get('LPCLMG', 0.0) # M641
        self.NPCLMG = self.given.get('NPCLMG', 0.0) # M642
        self.PPCLMG = self.given.get('PPCLMG', 0.0) # M643
        self.LA1 = self.given.get('LA1', 0.0) # M644
        self.NA1 = self.given.get('NA1', 0.0) # M645
        self.PA1 = self.given.get('PA1', 0.0) # M646
        self.LA11 = self.given.get('LA11', 0.0) # M647
        self.NA11 = self.given.get('NA11', 0.0) # M648
        self.PA11 = self.given.get('PA11', 0.0) # M649
        self.LA2 = self.given.get('LA2', 0.0) # M650
        self.NA2 = self.given.get('NA2', 0.0) # M651
        self.PA2 = self.given.get('PA2', 0.0) # M652
        self.LA21 = self.given.get('LA21', 0.0) # M653
        self.NA21 = self.given.get('NA21', 0.0) # M654
        self.PA21 = self.given.get('PA21', 0.0) # M655
        self.LRDSW = self.given.get('LRDSW', 0.0) # M656
        self.NRDSW = self.given.get('NRDSW', 0.0) # M657
        self.PRDSW = self.given.get('PRDSW', 0.0) # M658
        self.LRSW = self.given.get('LRSW', 0.0) # M659
        self.NRSW = self.given.get('NRSW', 0.0) # M660
        self.PRSW = self.given.get('PRSW', 0.0) # M661
        self.LRDW = self.given.get('LRDW', 0.0) # M662
        self.NRDW = self.given.get('NRDW', 0.0) # M663
        self.PRDW = self.given.get('PRDW', 0.0) # M664
        self.LPRWGS = self.given.get('LPRWGS', 0.0) # M665
        self.NPRWGS = self.given.get('NPRWGS', 0.0) # M666
        self.PPRWGS = self.given.get('PPRWGS', 0.0) # M667
        self.LPRWGD = self.given.get('LPRWGD', 0.0) # M668
        self.NPRWGD = self.given.get('NPRWGD', 0.0) # M669
        self.PPRWGD = self.given.get('PPRWGD', 0.0) # M670
        self.LWR = self.given.get('LWR', 0.0) # M671
        self.NWR = self.given.get('NWR', 0.0) # M672
        self.PWR = self.given.get('PWR', 0.0) # M673
        self.LPDIBL1 = self.given.get('LPDIBL1', 0.0) # M674
        self.NPDIBL1 = self.given.get('NPDIBL1', 0.0) # M675
        self.PPDIBL1 = self.given.get('PPDIBL1', 0.0) # M676
        self.LPDIBL2 = self.given.get('LPDIBL2', 0.0) # M677
        self.NPDIBL2 = self.given.get('NPDIBL2', 0.0) # M678
        self.PPDIBL2 = self.given.get('PPDIBL2', 0.0) # M679
        self.LDROUT = self.given.get('LDROUT', 0.0) # M680
        self.NDROUT = self.given.get('NDROUT', 0.0) # M681
        self.PDROUT = self.given.get('PDROUT', 0.0) # M682
        self.LPVAG = self.given.get('LPVAG', 0.0) # M683
        self.NPVAG = self.given.get('NPVAG', 0.0) # M684
        self.PPVAG = self.given.get('PPVAG', 0.0) # M685
        self.LAIGBINV = self.given.get('LAIGBINV', 0.0) # M686
        self.NAIGBINV = self.given.get('NAIGBINV', 0.0) # M687
        self.PAIGBINV = self.given.get('PAIGBINV', 0.0) # M688
        self.LAIGBINV1 = self.given.get('LAIGBINV1', 0.0) # M689
        self.NAIGBINV1 = self.given.get('NAIGBINV1', 0.0) # M690
        self.PAIGBINV1 = self.given.get('PAIGBINV1', 0.0) # M691
        self.LBIGBINV = self.given.get('LBIGBINV', 0.0) # M692
        self.NBIGBINV = self.given.get('NBIGBINV', 0.0) # M693
        self.PBIGBINV = self.given.get('PBIGBINV', 0.0) # M694
        self.LCIGBINV = self.given.get('LCIGBINV', 0.0) # M695
        self.NCIGBINV = self.given.get('NCIGBINV', 0.0) # M696
        self.PCIGBINV = self.given.get('PCIGBINV', 0.0) # M697
        self.LEIGBINV = self.given.get('LEIGBINV', 0.0) # M698
        self.NEIGBINV = self.given.get('NEIGBINV', 0.0) # M699
        self.PEIGBINV = self.given.get('PEIGBINV', 0.0) # M700
        self.LNIGBINV = self.given.get('LNIGBINV', 0.0) # M701
        self.NNIGBINV = self.given.get('NNIGBINV', 0.0) # M702
        self.PNIGBINV = self.given.get('PNIGBINV', 0.0) # M703
        self.LAIGBACC = self.given.get('LAIGBACC', 0.0) # M704
        self.NAIGBACC = self.given.get('NAIGBACC', 0.0) # M705
        self.PAIGBACC = self.given.get('PAIGBACC', 0.0) # M706
        self.LAIGBACC1 = self.given.get('LAIGBACC1', 0.0) # M707
        self.NAIGBACC1 = self.given.get('NAIGBACC1', 0.0) # M708
        self.PAIGBACC1 = self.given.get('PAIGBACC1', 0.0) # M709
        self.LBIGBACC = self.given.get('LBIGBACC', 0.0) # M710
        self.NBIGBACC = self.given.get('NBIGBACC', 0.0) # M711
        self.PBIGBACC = self.given.get('PBIGBACC', 0.0) # M712
        self.LCIGBACC = self.given.get('LCIGBACC', 0.0) # M713
        self.NCIGBACC = self.given.get('NCIGBACC', 0.0) # M714
        self.PCIGBACC = self.given.get('PCIGBACC', 0.0) # M715
        self.LNIGBACC = self.given.get('LNIGBACC', 0.0) # M716
        self.NNIGBACC = self.given.get('NNIGBACC', 0.0) # M717
        self.PNIGBACC = self.given.get('PNIGBACC', 0.0) # M718
        self.LAIGC = self.given.get('LAIGC', 0.0) # M719
        self.NAIGC = self.given.get('NAIGC', 0.0) # M720
        self.PAIGC = self.given.get('PAIGC', 0.0) # M721
        self.LAIGC1 = self.given.get('LAIGC1', 0.0) # M722
        self.NAIGC1 = self.given.get('NAIGC1', 0.0) # M723
        self.PAIGC1 = self.given.get('PAIGC1', 0.0) # M724
        self.LBIGC = self.given.get('LBIGC', 0.0) # M725
        self.NBIGC = self.given.get('NBIGC', 0.0) # M726
        self.PBIGC = self.given.get('PBIGC', 0.0) # M727
        self.LCIGC = self.given.get('LCIGC', 0.0) # M728
        self.NCIGC = self.given.get('NCIGC', 0.0) # M729
        self.PCIGC = self.given.get('PCIGC', 0.0) # M730
        self.LPIGCD = self.given.get('LPIGCD', 0.0) # M731
        self.NPIGCD = self.given.get('NPIGCD', 0.0) # M732
        self.PPIGCD = self.given.get('PPIGCD', 0.0) # M733
        self.LAIGS = self.given.get('LAIGS', 0.0) # M734
        self.NAIGS = self.given.get('NAIGS', 0.0) # M735
        self.PAIGS = self.given.get('PAIGS', 0.0) # M736
        self.LAIGS1 = self.given.get('LAIGS1', 0.0) # M737
        self.NAIGS1 = self.given.get('NAIGS1', 0.0) # M738
        self.PAIGS1 = self.given.get('PAIGS1', 0.0) # M739
        self.LBIGS = self.given.get('LBIGS', 0.0) # M740
        self.NBIGS = self.given.get('NBIGS', 0.0) # M741
        self.PBIGS = self.given.get('PBIGS', 0.0) # M742
        self.LCIGS = self.given.get('LCIGS', 0.0) # M743
        self.NCIGS = self.given.get('NCIGS', 0.0) # M744
        self.PCIGS = self.given.get('PCIGS', 0.0) # M745
        self.LNTOX = self.given.get('LNTOX', 0.0) # M746
        self.NNTOX = self.given.get('NNTOX', 0.0) # M747
        self.PNTOX = self.given.get('PNTOX', 0.0) # M748
        self.LPOXEDGE = self.given.get('LPOXEDGE', 0.0) # M749
        self.NPOXEDGE = self.given.get('NPOXEDGE', 0.0) # M750
        self.PPOXEDGE = self.given.get('PPOXEDGE', 0.0) # M751
        self.LAGISL = self.given.get('LAGISL', 0.0) # M752
        self.NAGISL = self.given.get('NAGISL', 0.0) # M753
        self.PAGISL = self.given.get('PAGISL', 0.0) # M754
        self.LBGISL = self.given.get('LBGISL', 0.0) # M755
        self.NBGISL = self.given.get('NBGISL', 0.0) # M756
        self.PBGISL = self.given.get('PBGISL', 0.0) # M757
        self.LCGISL = self.given.get('LCGISL', 0.0) # M758
        self.NCGISL = self.given.get('NCGISL', 0.0) # M759
        self.PCGISL = self.given.get('PCGISL', 0.0) # M760
        self.LEGISL = self.given.get('LEGISL', 0.0) # M761
        self.NEGISL = self.given.get('NEGISL', 0.0) # M762
        self.PEGISL = self.given.get('PEGISL', 0.0) # M763
        self.LPGISL = self.given.get('LPGISL', 0.0) # M764
        self.NPGISL = self.given.get('NPGISL', 0.0) # M765
        self.PPGISL = self.given.get('PPGISL', 0.0) # M766
        self.LALPHA0 = self.given.get('LALPHA0', 0.0) # M767
        self.NALPHA0 = self.given.get('NALPHA0', 0.0) # M768
        self.PALPHA0 = self.given.get('PALPHA0', 0.0) # M769
        self.LALPHA1 = self.given.get('LALPHA1', 0.0) # M770
        self.NALPHA1 = self.given.get('NALPHA1', 0.0) # M771
        self.PALPHA1 = self.given.get('PALPHA1', 0.0) # M772
        self.LALPHAII0 = self.given.get('LALPHAII0', 0.0) # M773
        self.NALPHAII0 = self.given.get('NALPHAII0', 0.0) # M774
        self.PALPHAII0 = self.given.get('PALPHAII0', 0.0) # M775
        self.LALPHAII1 = self.given.get('LALPHAII1', 0.0) # M776
        self.NALPHAII1 = self.given.get('NALPHAII1', 0.0) # M777
        self.PALPHAII1 = self.given.get('PALPHAII1', 0.0) # M778
        self.LBETA0 = self.given.get('LBETA0', 0.0) # M779
        self.NBETA0 = self.given.get('NBETA0', 0.0) # M780
        self.PBETA0 = self.given.get('PBETA0', 0.0) # M781
        self.LBETAII0 = self.given.get('LBETAII0', 0.0) # M782
        self.NBETAII0 = self.given.get('NBETAII0', 0.0) # M783
        self.PBETAII0 = self.given.get('PBETAII0', 0.0) # M784
        self.LBETAII1 = self.given.get('LBETAII1', 0.0) # M785
        self.NBETAII1 = self.given.get('NBETAII1', 0.0) # M786
        self.PBETAII1 = self.given.get('PBETAII1', 0.0) # M787
        self.LBETAII2 = self.given.get('LBETAII2', 0.0) # M788
        self.NBETAII2 = self.given.get('NBETAII2', 0.0) # M789
        self.PBETAII2 = self.given.get('PBETAII2', 0.0) # M790
        self.LESATII = self.given.get('LESATII', 0.0) # M791
        self.NESATII = self.given.get('NESATII', 0.0) # M792
        self.PESATII = self.given.get('PESATII', 0.0) # M793
        self.LLII = self.given.get('LLII', 0.0) # M794
        self.NLII = self.given.get('NLII', 0.0) # M795
        self.PLII = self.given.get('PLII', 0.0) # M796
        self.LSII0 = self.given.get('LSII0', 0.0) # M797
        self.NSII0 = self.given.get('NSII0', 0.0) # M798
        self.PSII0 = self.given.get('PSII0', 0.0) # M799
        self.LSII1 = self.given.get('LSII1', 0.0) # M800
        self.NSII1 = self.given.get('NSII1', 0.0) # M801
        self.PSII1 = self.given.get('PSII1', 0.0) # M802
        self.LSII2 = self.given.get('LSII2', 0.0) # M803
        self.NSII2 = self.given.get('NSII2', 0.0) # M804
        self.PSII2 = self.given.get('PSII2', 0.0) # M805
        self.LSIID = self.given.get('LSIID', 0.0) # M806
        self.NSIID = self.given.get('NSIID', 0.0) # M807
        self.PSIID = self.given.get('PSIID', 0.0) # M808
        self.LNTGEN = self.given.get('LNTGEN', 0.0) # M827
        self.NNTGEN = self.given.get('NNTGEN', 0.0) # M828
        self.PNTGEN = self.given.get('PNTGEN', 0.0) # M829
        self.LAIGEN = self.given.get('LAIGEN', 0.0) # M830
        self.NAIGEN = self.given.get('NAIGEN', 0.0) # M831
        self.PAIGEN = self.given.get('PAIGEN', 0.0) # M832
        self.LBIGEN = self.given.get('LBIGEN', 0.0) # M833
        self.NBIGEN = self.given.get('NBIGEN', 0.0) # M834
        self.PBIGEN = self.given.get('PBIGEN', 0.0) # M835
        self.LXRCRG1 = self.given.get('LXRCRG1', 0.0) # M836
        self.NXRCRG1 = self.given.get('NXRCRG1', 0.0) # M837
        self.PXRCRG1 = self.given.get('PXRCRG1', 0.0) # M838
        self.LXRCRG2 = self.given.get('LXRCRG2', 0.0) # M839
        self.NXRCRG2 = self.given.get('NXRCRG2', 0.0) # M840
        self.PXRCRG2 = self.given.get('PXRCRG2', 0.0) # M841
        self.LUTE = self.given.get('LUTE', 0.0) # M842
        self.NUTE = self.given.get('NUTE', 0.0) # M843
        self.PUTE = self.given.get('PUTE', 0.0) # M844
        self.LUTL = self.given.get('LUTL', 0.0) # M845
        self.NUTL = self.given.get('NUTL', 0.0) # M846
        self.PUTL = self.given.get('PUTL', 0.0) # M847
        self.LEMOBT = self.given.get('LEMOBT', 0.0) # M848
        self.NEMOBT = self.given.get('NEMOBT', 0.0) # M849
        self.PEMOBT = self.given.get('PEMOBT', 0.0) # M850
        self.LUA1 = self.given.get('LUA1', 0.0) # M851
        self.NUA1 = self.given.get('NUA1', 0.0) # M852
        self.PUA1 = self.given.get('PUA1', 0.0) # M853
        self.LUC1 = self.given.get('LUC1', 0.0) # M854
        self.NUC1 = self.given.get('NUC1', 0.0) # M855
        self.PUC1 = self.given.get('PUC1', 0.0) # M856
        self.LUD1 = self.given.get('LUD1', 0.0) # M857
        self.NUD1 = self.given.get('NUD1', 0.0) # M858
        self.PUD1 = self.given.get('PUD1', 0.0) # M859
        self.LUCSTE = self.given.get('LUCSTE', 0.0) # M860
        self.NUCSTE = self.given.get('NUCSTE', 0.0) # M861
        self.PUCSTE = self.given.get('PUCSTE', 0.0) # M862
        self.LPTWGT = self.given.get('LPTWGT', 0.0) # M863
        self.NPTWGT = self.given.get('NPTWGT', 0.0) # M864
        self.PPTWGT = self.given.get('PPTWGT', 0.0) # M865
        self.LAT = self.given.get('LAT', 0.0) # M866
        self.NAT = self.given.get('NAT', 0.0) # M867
        self.PAT = self.given.get('PAT', 0.0) # M868
        self.LATCV = self.given.get('LATCV', 0.0) # M869
        self.NATCV = self.given.get('NATCV', 0.0) # M870
        self.PATCV = self.given.get('PATCV', 0.0) # M871
        self.LSTTHETASAT = self.given.get('LSTTHETASAT', 0.0) # M872
        self.NSTTHETASAT = self.given.get('NSTTHETASAT', 0.0) # M873
        self.PSTTHETASAT = self.given.get('PSTTHETASAT', 0.0) # M874
        self.LPRT = self.given.get('LPRT', 0.0) # M875
        self.NPRT = self.given.get('NPRT', 0.0) # M876
        self.PPRT = self.given.get('PPRT', 0.0) # M877
        self.LKT1 = self.given.get('LKT1', 0.0) # M878
        self.NKT1 = self.given.get('NKT1', 0.0) # M879
        self.PKT1 = self.given.get('PKT1', 0.0) # M880
        self.LTSS = self.given.get('LTSS', 0.0) # M881
        self.NTSS = self.given.get('NTSS', 0.0) # M882
        self.PTSS = self.given.get('PTSS', 0.0) # M883
        self.LIIT = self.given.get('LIIT', 0.0) # M884
        self.NIIT = self.given.get('NIIT', 0.0) # M885
        self.PIIT = self.given.get('PIIT', 0.0) # M886
        self.LTII = self.given.get('LTII', 0.0) # M887
        self.NTII = self.given.get('NTII', 0.0) # M888
        self.PTII = self.given.get('PTII', 0.0) # M889
        self.LTGIDL = self.given.get('LTGIDL', 0.0) # M890
        self.NTGIDL = self.given.get('NTGIDL', 0.0) # M891
        self.PTGIDL = self.given.get('PTGIDL', 0.0) # M892
        self.LIGT = self.given.get('LIGT', 0.0) # M893
        self.NIGT = self.given.get('NIGT', 0.0) # M894
        self.PIGT = self.given.get('PIGT', 0.0) # M895
        self.LCITR = self.given.get('LCITR', self.LCIT) # M896
        self.NCITR = self.given.get('NCITR', self.NCIT) # M897
        self.PCITR = self.given.get('PCITR', self.PCIT) # M898
        self.LCDSCDR = self.given.get('LCDSCDR', self.LCDSCD) # M899
        self.NCDSCDR = self.given.get('NCDSCDR', self.NCDSCD) # M900
        self.PCDSCDR = self.given.get('PCDSCDR', self.PCDSCD) # M901
        self.LDVT1SS = self.given.get('LDVT1SS', self.LDVT1) # M902
        self.NDVT1SS = self.given.get('NDVT1SS', self.NDVT1) # M903
        self.PDVT1SS = self.given.get('PDVT1SS', self.PDVT1) # M904
        self.LETA0R = self.given.get('LETA0R', self.LETA0) # M905
        self.NETA0R = self.given.get('NETA0R', self.NETA0) # M906
        self.PETA0R = self.given.get('PETA0R', self.PETA0) # M907
        self.LDVTSHIFTR = self.given.get('LDVTSHIFTR', self.LDVTSHIFT) # M908
        self.NDVTSHIFTR = self.given.get('NDVTSHIFTR', self.NDVTSHIFT) # M909
        self.PDVTSHIFTR = self.given.get('PDVTSHIFTR', self.PDVTSHIFT) # M910
        self.LK2SI = self.given.get('LK2SI', self.LK0SI) # M911
        self.NK2SI = self.given.get('NK2SI', self.NK0SI) # M912
        self.PK2SI = self.given.get('PK2SI', self.PK0SI) # M913
        self.LK2SI1 = self.given.get('LK2SI1', self.LK0SI1) # M914
        self.NK2SI1 = self.given.get('NK2SI1', self.NK0SI1) # M915
        self.PK2SI1 = self.given.get('PK2SI1', self.PK0SI1) # M916
        self.LK2SISAT = self.given.get('LK2SISAT', self.LK0SISAT) # M917
        self.NK2SISAT = self.given.get('NK2SISAT', self.NK0SISAT) # M918
        self.PK2SISAT = self.given.get('PK2SISAT', self.PK0SISAT) # M919
        self.LK2SISAT1 = self.given.get('LK2SISAT1', self.LK0SISAT1) # M920
        self.NK2SISAT1 = self.given.get('NK2SISAT1', self.NK0SISAT1) # M921
        self.PK2SISAT1 = self.given.get('PK2SISAT1', self.PK0SISAT1) # M922
        self.LVSATR = self.given.get('LVSATR', self.LVSAT) # M923
        self.NVSATR = self.given.get('NVSATR', self.NVSAT) # M924
        self.PVSATR = self.given.get('PVSATR', self.PVSAT) # M925
        self.LVSAT1 = self.given.get('LVSAT1', self.LVSAT) # M926
        self.NVSAT1 = self.given.get('NVSAT1', self.NVSAT) # M927
        self.PVSAT1 = self.given.get('PVSAT1', self.PVSAT) # M928
        self.LKSATIVR = self.given.get('LKSATIVR', self.LKSATIV) # M929
        self.NKSATIVR = self.given.get('NKSATIVR', self.NKSATIV) # M930
        self.PKSATIVR = self.given.get('PKSATIVR', self.PKSATIV) # M931
        self.LMEXPR = self.given.get('LMEXPR', self.LMEXP) # M932
        self.NMEXPR = self.given.get('NMEXPR', self.NMEXP) # M933
        self.PMEXPR = self.given.get('PMEXPR', self.PMEXP) # M934
        self.LPTWGR = self.given.get('LPTWGR', self.LPTWG) # M935
        self.NPTWGR = self.given.get('NPTWGR', self.NPTWG) # M936
        self.PPTWGR = self.given.get('PPTWGR', self.PPTWG) # M937
        self.LU0R = self.given.get('LU0R', self.LU0) # M938
        self.NU0R = self.given.get('NU0R', self.NU0) # M939
        self.PU0R = self.given.get('PU0R', self.PU0) # M940
        self.LUPR = self.given.get('LUPR', self.LUP) # M941
        self.NUPR = self.given.get('NUPR', self.NUP) # M942
        self.PUPR = self.given.get('PUPR', self.PUP) # M943
        self.LUAR = self.given.get('LUAR', self.LUA) # M944
        self.NUAR = self.given.get('NUAR', self.NUA) # M945
        self.PUAR = self.given.get('PUAR', self.PUA) # M946
        self.LUCR = self.given.get('LUCR', self.LUC) # M947
        self.NUCR = self.given.get('NUCR', self.NUC) # M948
        self.PUCR = self.given.get('PUCR', self.PUC) # M949
        self.LEUR = self.given.get('LEUR', self.LEU) # M950
        self.NEUR = self.given.get('NEUR', self.NEU) # M951
        self.PEUR = self.given.get('PEUR', self.PEU) # M952
        self.LUDR = self.given.get('LUDR', self.LUD) # M953
        self.NUDR = self.given.get('NUDR', self.NUD) # M954
        self.PUDR = self.given.get('PUDR', self.PUD) # M955
        self.LPCLMR = self.given.get('LPCLMR', self.LPCLM) # M956
        self.NPCLMR = self.given.get('NPCLMR', self.NPCLM) # M957
        self.PPCLMR = self.given.get('PPCLMR', self.PPCLM) # M958
        self.LPDIBL1R = self.given.get('LPDIBL1R', self.LPDIBL1) # M962
        self.NPDIBL1R = self.given.get('NPDIBL1R', self.NPDIBL1) # M963
        self.PPDIBL1R = self.given.get('PPDIBL1R', self.PPDIBL1) # M964
        self.LPDIBL2R = self.given.get('LPDIBL2R', self.LPDIBL2) # M965
        self.NPDIBL2R = self.given.get('NPDIBL2R', self.NPDIBL2) # M966
        self.PPDIBL2R = self.given.get('PPDIBL2R', self.PPDIBL2) # M967
        self.LAIGD = self.given.get('LAIGD', self.LAIGS) # M968
        self.NAIGD = self.given.get('NAIGD', self.NAIGS) # M969
        self.PAIGD = self.given.get('PAIGD', self.PAIGS) # M970
        self.LAIGD1 = self.given.get('LAIGD1', self.LAIGS1) # M971
        self.NAIGD1 = self.given.get('NAIGD1', self.NAIGS1) # M972
        self.PAIGD1 = self.given.get('PAIGD1', self.PAIGS1) # M973
        self.LBIGD = self.given.get('LBIGD', self.LBIGS) # M974
        self.NBIGD = self.given.get('NBIGD', self.NBIGS) # M975
        self.PBIGD = self.given.get('PBIGD', self.PBIGS) # M976
        self.LCIGD = self.given.get('LCIGD', self.LCIGS) # M977
        self.NCIGD = self.given.get('NCIGD', self.NCIGS) # M978
        self.PCIGD = self.given.get('PCIGD', self.PCIGS) # M979
        self.LAGIDL = self.given.get('LAGIDL', self.LAGISL) # M980
        self.NAGIDL = self.given.get('NAGIDL', self.NAGISL) # M981
        self.PAGIDL = self.given.get('PAGIDL', self.PAGISL) # M982
        self.LBGIDL = self.given.get('LBGIDL', self.LBGISL) # M983
        self.NBGIDL = self.given.get('NBGIDL', self.NBGISL) # M984
        self.PBGIDL = self.given.get('PBGIDL', self.PBGISL) # M985
        self.LCGIDL = self.given.get('LCGIDL', self.LCGISL) # M986
        self.NCGIDL = self.given.get('NCGIDL', self.NCGISL) # M987
        self.PCGIDL = self.given.get('PCGIDL', self.PCGISL) # M988
        self.LEGIDL = self.given.get('LEGIDL', self.LEGISL) # M989
        self.NEGIDL = self.given.get('NEGIDL', self.NEGISL) # M990
        self.PEGIDL = self.given.get('PEGIDL', self.PEGISL) # M991
        self.LPGIDL = self.given.get('LPGIDL', self.LPGISL) # M992
        self.NPGIDL = self.given.get('NPGIDL', self.NPGISL) # M993
        self.PPGIDL = self.given.get('PPGIDL', self.PPGISL) # M994
        self.LUTER = self.given.get('LUTER', self.LUTE) # M1007
        self.NUTER = self.given.get('NUTER', self.NUTE) # M1008
        self.PUTER = self.given.get('PUTER', self.PUTE) # M1009
        self.LUTLR = self.given.get('LUTLR', self.LUTL) # M1010
        self.NUTLR = self.given.get('NUTLR', self.NUTL) # M1011
        self.PUTLR = self.given.get('PUTLR', self.PUTL) # M1012
        self.LUA1R = self.given.get('LUA1R', self.LUA1) # M1013
        self.NUA1R = self.given.get('NUA1R', self.NUA1) # M1014
        self.PUA1R = self.given.get('PUA1R', self.PUA1) # M1015
        self.LUC1R = self.given.get('LUC1R', self.LUC1) # M1016
        self.NUC1R = self.given.get('NUC1R', self.NUC1) # M1017
        self.PUC1R = self.given.get('PUC1R', self.PUC1) # M1018
        self.LUD1R = self.given.get('LUD1R', self.LUD1) # M1019
        self.NUD1R = self.given.get('NUD1R', self.NUD1) # M1020
        self.PUD1R = self.given.get('PUD1R', self.PUD1) # M1021
        self.LATR = self.given.get('LATR', self.LAT) # M1022
        self.NATR = self.given.get('NATR', self.NAT) # M1023
        self.PATR = self.given.get('PATR', self.PAT) # M1024
        self.LVSAT1R = self.given.get('LVSAT1R', self.LVSAT1) # M1025
        self.NVSAT1R = self.given.get('NVSAT1R', self.NVSAT1) # M1026
        self.PVSAT1R = self.given.get('PVSAT1R', self.PVSAT1) # M1027

    # Clamped exponential function
    def lexp(self, x):
        if x > 80.0:
            return 5.540622384e34 * (1.0 + x - 80.0)
        elif x < -80.0:
            return 1.804851387e-35
        else:
            return exp(x)

    # Clamped log function
    def lln(self, x):
        return log(max(x, 1.0e-38))

    # Hyperbolic smoothing function
    def hypsmooth(self, x, c):
        return 0.5 * (x + sqrt(x * x + 4.0 * c * c))

    # Hyperbolic smoothing max Function
    def hypmax(self, x, xmin, c):
        return xmin + 0.5 * (x - xmin - c + sqrt((x - xmin - c) *
            (x - xmin - c) - 4.0 * xmin * c))

    # Temperature dependence type
    def tempdep(self, PARAML, PARAMT, DELTEMP, TEMPMOD):
        if TEMPMOD != 0:
            return PARAML + self.hypmax(PARAMT * DELTEMP, -PARAML, 1.0e-6)
        else:
            return PARAML * self.hypsmooth(1.0 + PARAMT * DELTEMP - 1.0e-6, 1.0e-3)

    def calc(self):
        # Constants
        if self.TYPE == 1:
            devsign = 1
        else:
            devsign = -1

        epssub = self.EPSRSUB * 8.8542e-12
        epssp = self.EPSRSP * 8.8542e-12
        cbox = self.EPSROX * 8.8542e-12 / self.EOTBOX
        epsratio = self.EPSRSUB / self.EPSROX

        # Constants for quantum mechanical effects
        mx = 0.916 * 9.11e-31
        mxprime = 0.190 * 9.11e-31
        md = 0.190 * 9.11e-31
        mdprime = 0.417 * 9.11e-31
        gprime = 4.0
        gfactor = 2.0

        # Effective channel length for I-V/C-V
        Lg = self.L + self.XL
        deltaL = self.LINT + self.LL * pow(Lg, -self.LLN)
        deltaL1 = self.LINT + self.LL * pow(Lg + self.DLBIN, -self.LLN)
        Leff = Lg - 2.0 * deltaL
        Leff1 = Lg + self.DLBIN - 2.0 * deltaL1

        # Total fins
        NFINtotal = self.NFIN * self.NF

        # Binning
        Inv_L = 1.0e-6 / Leff1
        Inv_NFIN = 1.0 / self.NFIN
        Inv_LNFIN = 1.0e-6 / (Leff1 * self.NFIN)

        # NBODY binning equation for UFCM parameters
        NBODY_i = self.NBODY + Inv_L * self.LNBODY + Inv_NFIN * self.NNBODY + Inv_LNFIN * self.PNBODY

        if self.NBODYN1 != 0.0:
            NBODY_i = NBODY_i + 1.0 + self.NBODYN1 / self.NFIN * self.lln(1.0 + self.NFIN / self.NBODYN2)

        # Model parameters for unified FinFET compact model
        if self.GEOMOD == 0:
            # Double gate
            if 'TFIN_TOP' not in self.given or 'TFIN_BASE' not in self.given:
                Weff_UFCM = 2.0 * self.HFIN
                Cins = Weff_UFCM * self.EPSROX * 8.8542e-12 / self.EOT
                Ach = self.HFIN * self.TFIN
                rc = 2.0 * Cins / (Weff_UFCM * Weff_UFCM * epssub / Ach)
                Qdep_ov_Cins = -1.60219e-19 * NBODY_i * Ach / Cins
            else:
                Weff_UFCM = 2.0 * sqrt(self.HFIN * self.HFIN + (self.TFIN_TOP - self.TFIN_BASE) * (self.TFIN_TOP - self.TFIN_BASE) / 4.0)
                Cins = Weff_UFCM * self.EPSROX * 8.8542e-12 / self.EOT
                Ach = self.HFIN * (self.TFIN_TOP + self.TFIN_BASE) / 2.0
                rc = 2.0 * Cins / (Weff_UFCM * Weff_UFCM * epssub / Ach)
                Qdep_ov_Cins = -1.60219e-19 * NBODY_i * Ach / Cins
        elif self.GEOMOD == 1:
            # Triple gate (FinFET)
            if 'TFIN_TOP' not in self.given or 'TFIN_BASE' not in self.given:
                Weff_UFCM = 2.0 * self.HFIN + self.TFIN
                Cins = Weff_UFCM * self.EPSROX * 8.8542e-12 / self.EOT
                Ach = self.HFIN * self.TFIN
                rc = 2.0 * Cins / (Weff_UFCM * Weff_UFCM * epssub / Ach)
                Qdep_ov_Cins = -1.60219e-19 * NBODY_i * Ach / Cins
            else:
                Weff_UFCM = 2.0 * sqrt(self.HFIN * self.HFIN + (self.TFIN_TOP - self.TFIN_BASE) * (self.TFIN_TOP - self.TFIN_BASE) / 4.0) + self.TFIN_TOP
                Cins = Weff_UFCM * self.EPSROX * 8.8542e-12 / self.EOT
                Ach = self.HFIN * (self.TFIN_TOP + self.TFIN_BASE) / 2.0
                rc = 2.0 * Cins /(Weff_UFCM * Weff_UFCM * epssub / Ach)
                Qdep_ov_Cins = -1.60219e-19 * NBODY_i * Ach / Cins
        elif self.GEOMOD == 2:
            # Quadruple gate
            if 'TFIN_TOP' not in self.given or 'TFIN_BASE' not in self.given:
                Weff_UFCM = 2.0 * self.HFIN + 2.0 * self.TFIN
                Cins = Weff_UFCM * self.EPSROX * 8.8542e-12 / self.EOT
                Ach = self.HFIN * self.TFIN
                rc = 2.0 * Cins / (Weff_UFCM * Weff_UFCM * epssub / Ach)
                Qdep_ov_Cins = -1.60219e-19 * NBODY_i * Ach / Cins
            else:
                Weff_UFCM = 2.0 * sqrt(self.HFIN * self.HFIN + (self.TFIN_TOP - self.TFIN_BASE) * \
                    (self.TFIN_TOP - self.TFIN_BASE) / 4.0) + self.TFIN_TOP + self.TFIN_BASE
                Cins = Weff_UFCM * self.EPSROX * 8.8542e-12 / self.EOT
                Ach = self.HFIN * (self.TFIN_TOP + self.TFIN_BASE) / 2.0
                rc = 2.0 * Cins / (Weff_UFCM * Weff_UFCM * epssub / Ach)
                Qdep_ov_Cins = -1.60219e-19 * NBODY_i * Ach / Cins
        elif self.GEOMOD == 3:
            # Cylindrical gate
            Weff_UFCM = 3.14159265358979323846 * self.D
            Cins = 2.0 * 3.14159265358979323846 * self.EPSROX * 8.8542e-12 / log(1.0 + 2.0 * self.EOT / self.D)
            Ach = 3.14159265358979323846 * self.D * self.D / 4.0
            rc = 2.0 * Cins / (Weff_UFCM * Weff_UFCM * epssub / Ach)
            Qdep_ov_Cins = -1.60219e-19 * NBODY_i * Ach / Cins
        elif self.GEOMOD == 4:
            # Unified Model
            Weff_UFCM = self.W_UFCM
            Cins = self.CINS_UFCM
            Ach = self.ACH_UFCM
            rc = 2.0 * Cins / (Weff_UFCM * Weff_UFCM * epssub / Ach)
            Qdep_ov_Cins = -1.60219e-19 * NBODY_i * Ach / Cins

        # Cox definition
        cox = Cins / Weff_UFCM

        # Effective width calculation
        Weff0 = Weff_UFCM - self.DELTAW

        # SCE scaling length
        scl = sqrt(epssub * Ach / Cins * (1.0 + Ach * Cins / (2.0 * epssub * Weff_UFCM * Weff_UFCM)))

        # Binning equations
        PHIG_i = self.PHIG + Inv_L * self.LPHIG + Inv_NFIN * self.NPHIG + Inv_LNFIN * self.PPHIG
        NGATE_i = self.NGATE + Inv_L * self.LNGATE + Inv_NFIN * self.NNGATE + Inv_LNFIN * self.PNGATE
        CIT_i = self.CIT + Inv_L * self.LCIT + Inv_NFIN * self.NCIT + Inv_LNFIN * self.PCIT
        CDSC_i = self.CDSC + Inv_L * self.LCDSC + Inv_NFIN * self.NCDSC + Inv_LNFIN * self.PCDSC
        CDSCD_i = self.CDSCD + Inv_L * self.LCDSCD + Inv_NFIN * self.NCDSCD + Inv_LNFIN * self.PCDSCD
        DVT0_i = self.DVT0 + Inv_L * self.LDVT0 + Inv_NFIN * self.NDVT0 + Inv_LNFIN * self.PDVT0
        DVT1_i = self.DVT1 + Inv_L * self.LDVT1 + Inv_NFIN * self.NDVT1 + Inv_LNFIN * self.PDVT1
        DVT1SS_i = self.DVT1SS + Inv_L * self.LDVT1SS + Inv_NFIN * self.NDVT1SS + Inv_LNFIN * self.PDVT1SS
        PHIN_i = self.PHIN + Inv_L * self.LPHIN + Inv_NFIN * self.NPHIN + Inv_LNFIN * self.PPHIN
        ETA0_i = self.ETA0 + Inv_L * self.LETA0 + Inv_NFIN * self.NETA0 + Inv_LNFIN * self.PETA0
        DSUB_i = self.DSUB + Inv_L * self.LDSUB + Inv_NFIN * self.NDSUB + Inv_LNFIN * self.PDSUB
        K1RSCE_i = self.K1RSCE + Inv_L * self.LK1RSCE + Inv_NFIN * self.NK1RSCE + Inv_LNFIN * self.PK1RSCE
        LPE0_i = self.LPE0 + Inv_L * self.LLPE0 + Inv_NFIN * self.NLPE0 + Inv_LNFIN * self.PLPE0
        DVTSHIFT_i = self.DVTSHIFT + Inv_L * self.LDVTSHIFT + Inv_NFIN * self.NDVTSHIFT + Inv_LNFIN * self.PDVTSHIFT
        K0_i = self.K0 + Inv_L * self.LK0 + Inv_NFIN * self.NK0 + Inv_LNFIN * self.PK0
        K01_i = self.K01 + Inv_L * self.LK01 + Inv_NFIN * self.NK01 + Inv_LNFIN * self.PK01
        K0SI_i = self.K0SI + Inv_L * self.LK0SI + Inv_NFIN * self.NK0SI + Inv_LNFIN * self.PK0SI
        K0SI1_i = self.K0SI1 + Inv_L * self.LK0SI1 + Inv_NFIN * self.NK0SI1 + Inv_LNFIN * self.PK0SI1
        K2SI_i = self.K2SI + Inv_L * self.LK2SI + Inv_NFIN * self.NK2SI + Inv_LNFIN * self.PK2SI
        K2SI1_i = self.K2SI1 + Inv_L * self.LK2SI1 + Inv_NFIN * self.NK2SI1 + Inv_LNFIN * self.PK2SI1
        K0SISAT_i = self.K0SISAT + Inv_L * self.LK0SISAT + Inv_NFIN * self.NK0SISAT + Inv_LNFIN * self.PK0SISAT
        K0SISAT1_i = self.K0SISAT1 + Inv_L * self.LK0SISAT1 + Inv_NFIN * self.NK0SISAT1 + Inv_LNFIN * self.PK0SISAT1
        K2SISAT_i = self.K2SISAT + Inv_L * self.LK2SISAT + Inv_NFIN * self.NK2SISAT + Inv_LNFIN * self.PK2SISAT
        K2SISAT1_i = self.K2SISAT1 + Inv_L * self.LK2SISAT1 + Inv_NFIN * self.NK2SISAT1 + Inv_LNFIN * self.PK2SISAT1
        K2_i = self.K2 + Inv_L * self.LK2 + Inv_NFIN * self.NK2 + Inv_LNFIN * self.PK2
        K21_i = self.K21 + Inv_L * self.LK21 + Inv_NFIN * self.NK21 + Inv_LNFIN * self.PK21
        K2SAT_i = self.K2SAT + Inv_L * self.LK2SAT + Inv_NFIN * self.NK2SAT + Inv_LNFIN * self.PK2SAT
        K2SAT1_i = self.K2SAT1 + Inv_L * self.LK2SAT1 + Inv_NFIN * self.NK2SAT1 + Inv_LNFIN * self.PK2SAT1
        PHIBE_i = self.PHIBE + Inv_L * self.LPHIBE + Inv_NFIN * self.NPHIBE + Inv_LNFIN * self.PPHIBE
        K1_i = self.K1 + Inv_L * self.LK1 + Inv_NFIN * self.NK1 + Inv_LNFIN * self.PK1
        K11_i = self.K11 + Inv_L * self.LK11 + Inv_NFIN * self.NK11 + Inv_LNFIN * self.PK11
        QMFACTOR_i = self.QMFACTOR + Inv_L * self.LQMFACTOR + Inv_NFIN * self.NQMFACTOR + Inv_LNFIN * self.PQMFACTOR
        QMTCENCV_i = self.QMTCENCV + Inv_L * self.LQMTCENCV + Inv_NFIN * self.NQMTCENCV + Inv_LNFIN * self.PQMTCENCV
        QMTCENCVA_i = self.QMTCENCVA + Inv_L * self.LQMTCENCVA + Inv_NFIN * self.NQMTCENCVA + Inv_LNFIN * self.PQMTCENCVA
        VSAT_i = self.VSAT + Inv_L * self.LVSAT + Inv_NFIN * self.NVSAT + Inv_LNFIN * self.PVSAT
        VSAT1_i = self.VSAT1 + Inv_L * self.LVSAT1 + Inv_NFIN * self.NVSAT1 + Inv_LNFIN * self.PVSAT1
        DELTAVSAT_i = self.DELTAVSAT + Inv_L * self.LDELTAVSAT + Inv_NFIN * self.NDELTAVSAT + Inv_LNFIN * self.PDELTAVSAT
        PSAT_i = self.PSAT + Inv_L * self.LPSAT + Inv_NFIN * self.NPSAT + Inv_LNFIN * self.PPSAT
        KSATIV_i = self.KSATIV + Inv_L * self.LKSATIV + Inv_NFIN * self.NKSATIV + Inv_LNFIN * self.PKSATIV
        MEXP_i = self.MEXP + Inv_L * self.LMEXP + Inv_NFIN * self.NMEXP + Inv_LNFIN * self.PMEXP
        PTWG_i = self.PTWG + Inv_L * self.LPTWG + Inv_NFIN * self.NPTWG + Inv_LNFIN * self.PPTWG
        U0_i = self.U0 + Inv_L * self.LU0 + Inv_NFIN * self.NU0 + Inv_LNFIN * self.PU0
        ETAMOB_i = self.ETAMOB + Inv_L * self.LETAMOB + Inv_NFIN * self.NETAMOB + Inv_LNFIN * self.PETAMOB
        UP_i = self.UP + Inv_L * self.LUP + Inv_NFIN * self.NUP + Inv_LNFIN * self.PUP
        UA_i = self.UA + Inv_L * self.LUA + Inv_NFIN * self.NUA + Inv_LNFIN * self.PUA
        UC_i = self.UC + Inv_L * self.LUC + Inv_NFIN * self.NUC + Inv_LNFIN * self.PUC
        EU_i = self.EU + Inv_L * self.LEU + Inv_NFIN * self.NEU + Inv_LNFIN * self.PEU
        UD_i = self.UD + Inv_L * self.LUD + Inv_NFIN * self.NUD + Inv_LNFIN * self.PUD
        UCS_i = self.UCS + Inv_L * self.LUCS + Inv_NFIN * self.NUCS + Inv_LNFIN * self.PUCS
        PCLM_i = self.PCLM + Inv_L * self.LPCLM + Inv_NFIN * self.NPCLM + Inv_LNFIN * self.PPCLM
        PCLMG_i = self.PCLMG + Inv_L * self.LPCLMG + Inv_NFIN * self.NPCLMG + Inv_LNFIN * self.PPCLMG
        A1_i = self.A1 + Inv_L * self.LA1 + Inv_NFIN * self.NA1 + Inv_LNFIN * self.PA1
        A11_i = self.A11 + Inv_L * self.LA11 + Inv_NFIN * self.NA11 + Inv_LNFIN * self.PA11
        A2_i = self.A2 + Inv_L * self.LA2 + Inv_NFIN * self.NA2 + Inv_LNFIN * self.PA2
        A21_i = self.A21 + Inv_L * self.LA21 + Inv_NFIN * self.NA21 + Inv_LNFIN * self.PA21
        RDSW_i = self.RDSW + Inv_L * self.LRDSW + Inv_NFIN * self.NRDSW + Inv_LNFIN * self.PRDSW
        RSW_i = self.RSW + Inv_L * self.LRSW + Inv_NFIN * self.NRSW + Inv_LNFIN * self.PRSW
        RDW_i = self.RDW + Inv_L * self.LRDW + Inv_NFIN * self.NRDW + Inv_LNFIN * self.PRDW
        PRWGD_i = self.PRWGD + Inv_L * self.LPRWGD + Inv_NFIN * self.NPRWGD + Inv_LNFIN * self.PPRWGD
        PRWGS_i = self.PRWGS + Inv_L * self.LPRWGS + Inv_NFIN * self.NPRWGS + Inv_LNFIN * self.PPRWGS
        WR_i = self.WR + Inv_L * self.LWR + Inv_NFIN * self.NWR + Inv_LNFIN * self.PWR
        PDIBL1_i = self.PDIBL1 + Inv_L * self.LPDIBL1 + Inv_NFIN * self.NPDIBL1 + Inv_LNFIN * self.PPDIBL1
        PDIBL2_i = self.PDIBL2 + Inv_L * self.LPDIBL2 + Inv_NFIN * self.NPDIBL2 + Inv_LNFIN * self.PPDIBL2
        DROUT_i = self.DROUT + Inv_L * self.LDROUT + Inv_NFIN * self.NDROUT + Inv_LNFIN * self.PDROUT
        PVAG_i = self.PVAG + Inv_L * self.LPVAG + Inv_NFIN * self.NPVAG + Inv_LNFIN * self.PPVAG
        AIGBINV_i = self.AIGBINV + Inv_L * self.LAIGBINV + Inv_NFIN * self.NAIGBINV + Inv_LNFIN * self.PAIGBINV
        AIGBINV1_i = self.AIGBINV1 + Inv_L * self.LAIGBINV1 + Inv_NFIN * self.NAIGBINV1 + Inv_LNFIN * self.PAIGBINV1
        BIGBINV_i = self.BIGBINV + Inv_L * self.LBIGBINV + Inv_NFIN * self.NBIGBINV + Inv_LNFIN * self.PBIGBINV
        CIGBINV_i = self.CIGBINV + Inv_L * self.LCIGBINV + Inv_NFIN * self.NCIGBINV + Inv_LNFIN * self.PCIGBINV
        EIGBINV_i = self.EIGBINV + Inv_L * self.LEIGBINV + Inv_NFIN * self.NEIGBINV + Inv_LNFIN * self.PEIGBINV
        NIGBINV_i = self.NIGBINV + Inv_L * self.LNIGBINV + Inv_NFIN * self.NNIGBINV + Inv_LNFIN * self.PNIGBINV
        AIGBACC_i = self.AIGBACC + Inv_L * self.LAIGBACC + Inv_NFIN * self.NAIGBACC + Inv_LNFIN * self.PAIGBACC
        AIGBACC1_i = self.AIGBACC1 + Inv_L * self.LAIGBACC1 + Inv_NFIN * self.NAIGBACC1 + Inv_LNFIN * self.PAIGBACC1
        BIGBACC_i = self.BIGBACC + Inv_L * self.LBIGBACC + Inv_NFIN * self.NBIGBACC + Inv_LNFIN * self.PBIGBACC
        CIGBACC_i = self.CIGBACC + Inv_L * self.LCIGBACC + Inv_NFIN * self.NCIGBACC + Inv_LNFIN * self.PCIGBACC
        NIGBACC_i = self.NIGBACC + Inv_L * self.LNIGBACC + Inv_NFIN * self.NNIGBACC + Inv_LNFIN * self.PNIGBACC
        AIGC_i = self.AIGC + Inv_L * self.LAIGC + Inv_NFIN * self.NAIGC + Inv_LNFIN * self.PAIGC
        AIGC1_i = self.AIGC1 + Inv_L * self.LAIGC1 + Inv_NFIN * self.NAIGC1 + Inv_LNFIN * self.PAIGC1
        BIGC_i = self.BIGC + Inv_L * self.LBIGC + Inv_NFIN * self.NBIGC + Inv_LNFIN * self.PBIGC
        CIGC_i = self.CIGC + Inv_L * self.LCIGC + Inv_NFIN * self.NCIGC + Inv_LNFIN * self.PCIGC
        PIGCD_i = self.PIGCD + Inv_L * self.LPIGCD + Inv_NFIN * self.NPIGCD + Inv_LNFIN * self.PPIGCD
        AIGS_i = self.AIGS + Inv_L * self.LAIGS + Inv_NFIN * self.NAIGS + Inv_LNFIN * self.PAIGS
        AIGS1_i = self.AIGS1 + Inv_L * self.LAIGS1 + Inv_NFIN * self.NAIGS1 + Inv_LNFIN * self.PAIGS1
        BIGS_i = self.BIGS + Inv_L * self.LBIGS + Inv_NFIN * self.NBIGS + Inv_LNFIN * self.PBIGS
        CIGS_i = self.CIGS + Inv_L * self.LCIGS + Inv_NFIN * self.NCIGS + Inv_LNFIN * self.PCIGS
        AIGD_i = self.AIGD + Inv_L * self.LAIGD + Inv_NFIN * self.NAIGD + Inv_LNFIN * self.PAIGD
        AIGD1_i = self.AIGD1 + Inv_L * self.LAIGD1 + Inv_NFIN * self.NAIGD1 + Inv_LNFIN * self.PAIGD1
        BIGD_i = self.BIGD + Inv_L * self.LBIGD + Inv_NFIN * self.NBIGD + Inv_LNFIN * self.PBIGD
        CIGD_i = self.CIGD + Inv_L * self.LCIGD + Inv_NFIN * self.NCIGD + Inv_LNFIN * self.PCIGD
        NTOX_i = self.NTOX + Inv_L * self.LNTOX + Inv_NFIN * self.NNTOX + Inv_LNFIN * self.PNTOX
        POXEDGE_i = self.POXEDGE + Inv_L * self.LPOXEDGE + Inv_NFIN * self.NPOXEDGE + Inv_LNFIN * self.PPOXEDGE
        AGIDL_i = self.AGIDL + Inv_L * self.LAGIDL + Inv_NFIN * self.NAGIDL + Inv_LNFIN * self.PAGIDL
        BGIDL_i = self.BGIDL + Inv_L * self.LBGIDL + Inv_NFIN * self.NBGIDL + Inv_LNFIN * self.PBGIDL
        CGIDL_i = self.CGIDL + Inv_L * self.LCGIDL + Inv_NFIN * self.NCGIDL + Inv_LNFIN * self.PCGIDL
        EGIDL_i = self.EGIDL + Inv_L * self.LEGIDL + Inv_NFIN * self.NEGIDL + Inv_LNFIN * self.PEGIDL
        PGIDL_i = self.PGIDL + Inv_L * self.LPGIDL + Inv_NFIN * self.NPGIDL + Inv_LNFIN * self.PPGIDL
        AGISL_i = self.AGISL + Inv_L * self.LAGISL + Inv_NFIN * self.NAGISL + Inv_LNFIN * self.PAGISL
        BGISL_i = self.BGISL + Inv_L * self.LBGISL + Inv_NFIN * self.NBGISL + Inv_LNFIN * self.PBGISL
        CGISL_i = self.CGISL + Inv_L * self.LCGISL + Inv_NFIN * self.NCGISL + Inv_LNFIN * self.PCGISL
        EGISL_i = self.EGISL + Inv_L * self.LEGISL + Inv_NFIN * self.NEGISL + Inv_LNFIN * self.PEGISL
        PGISL_i = self.PGISL + Inv_L * self.LPGISL + Inv_NFIN * self.NPGISL + Inv_LNFIN * self.PPGISL
        ALPHA0_i = self.ALPHA0 + Inv_L * self.LALPHA0 + Inv_NFIN * self.NALPHA0 + Inv_LNFIN * self.PALPHA0
        ALPHA1_i = self.ALPHA1 + Inv_L * self.LALPHA1 + Inv_NFIN * self.NALPHA1 + Inv_LNFIN * self.PALPHA1
        ALPHAII0_i = self.ALPHAII0 + Inv_L * self.LALPHAII0 + Inv_NFIN * self.NALPHAII0 + Inv_LNFIN * self.PALPHAII0
        ALPHAII1_i = self.ALPHAII1 + Inv_L * self.LALPHAII1 + Inv_NFIN * self.NALPHAII1 + Inv_LNFIN * self.PALPHAII1
        BETA0_i = self.BETA0 + Inv_L * self.LBETA0 + Inv_NFIN * self.NBETA0 + Inv_LNFIN * self.PBETA0
        BETAII0_i = self.BETAII0 + Inv_L * self.LBETAII0 + Inv_NFIN * self.NBETAII0 + Inv_LNFIN * self.PBETAII0
        BETAII1_i = self.BETAII1 + Inv_L * self.LBETAII1 + Inv_NFIN * self.NBETAII1 + Inv_LNFIN * self.PBETAII1
        BETAII2_i = self.BETAII2 + Inv_L * self.LBETAII2 + Inv_NFIN * self.NBETAII2 + Inv_LNFIN * self.PBETAII2
        ESATII_i = self.ESATII + Inv_L * self.LESATII + Inv_NFIN * self.NESATII + Inv_LNFIN * self.PESATII
        LII_i = self.LII + Inv_L * self.LLII + Inv_NFIN * self.NLII + Inv_LNFIN * self.PLII
        SII0_i = self.SII0 + Inv_L * self.LSII0 + Inv_NFIN * self.NSII0 + Inv_LNFIN * self.PSII0
        SII1_i = self.SII1 + Inv_L * self.LSII1 + Inv_NFIN * self.NSII1 + Inv_LNFIN * self.PSII1
        SII2_i = self.SII2 + Inv_L * self.LSII2 + Inv_NFIN * self.NSII2 + Inv_LNFIN * self.PSII2
        SIID_i = self.SIID + Inv_L * self.LSIID + Inv_NFIN * self.NSIID + Inv_LNFIN * self.PSIID
        TII_i = self.TII + Inv_L * self.LTII + Inv_NFIN * self.NTII + Inv_LNFIN * self.PTII

        NTGEN_i = self.NTGEN + Inv_L * self.LNTGEN + Inv_NFIN * self.NNTGEN + Inv_LNFIN * self.PNTGEN
        AIGEN_i = self.AIGEN + Inv_L * self.LAIGEN + Inv_NFIN * self.NAIGEN + Inv_LNFIN * self.PAIGEN
        BIGEN_i = self.BIGEN + Inv_L * self.LBIGEN + Inv_NFIN * self.NBIGEN + Inv_LNFIN * self.PBIGEN
        CDSCDR_i = self.CDSCDR + Inv_L * self.LCDSCDR + Inv_NFIN * self.NCDSCDR + Inv_LNFIN * self.PCDSCDR
        CITR_i = self.CITR + Inv_L * self.LCITR + Inv_NFIN * self.NCITR + Inv_LNFIN * self.PCITR
        ETA0R_i = self.ETA0R + Inv_L * self.LETA0R + Inv_NFIN * self.NETA0R + Inv_LNFIN * self.PETA0R
        VSAT1R_i = self.VSAT1R + Inv_L * self.LVSAT1R + Inv_NFIN * self.NVSAT1R + Inv_LNFIN * self.PVSAT1R
        MEXPR_i = self.MEXPR + Inv_L * self.LMEXPR + Inv_NFIN * self.NMEXPR + Inv_LNFIN * self.PMEXPR
        PTWGR_i = self.PTWGR + Inv_L * self.LPTWGR + Inv_NFIN * self.NPTWGR + Inv_LNFIN * self.PPTWGR
        PDIBL1R_i = self.PDIBL1R + Inv_L * self.LPDIBL1R + Inv_NFIN * self.NPDIBL1R + Inv_LNFIN * self.PPDIBL1R
        PDIBL2R_i = self.PDIBL2R + Inv_L * self.LPDIBL2R + Inv_NFIN * self.NPDIBL2R + Inv_LNFIN * self.PPDIBL2R
        PCLMR_i = self.PCLMR + Inv_L * self.LPCLMR + Inv_NFIN * self.NPCLMR + Inv_LNFIN * self.PPCLMR
        DVTSHIFTR_i = self.DVTSHIFTR + Inv_L * self.LDVTSHIFTR + Inv_NFIN * self.NDVTSHIFTR + Inv_LNFIN * self.PDVTSHIFTR
        VSATR_i = self.VSATR + Inv_L * self.LVSATR + Inv_NFIN * self.NVSATR + Inv_LNFIN * self.PVSATR
        KSATIVR_i = self.KSATIVR + Inv_L * self.LKSATIVR + Inv_NFIN * self.NKSATIVR + Inv_LNFIN * self.PKSATIVR
        U0R_i = self.U0R + Inv_L * self.LU0R + Inv_NFIN * self.NU0R + Inv_LNFIN * self.PU0R
        UAR_i = self.UAR + Inv_L * self.LUAR + Inv_NFIN * self.NUAR + Inv_LNFIN * self.PUAR
        UPR_i = self.UPR + Inv_L * self.LUPR + Inv_NFIN * self.NUPR + Inv_LNFIN * self.PUPR
        UCR_i = self.UCR + Inv_L * self.LUCR + Inv_NFIN * self.NUCR + Inv_LNFIN * self.PUCR
        EUR_i = self.EUR + Inv_L * self.LEUR + Inv_NFIN * self.NEUR + Inv_LNFIN * self.PEUR
        UDR_i = self.UDR + Inv_L * self.LUDR + Inv_NFIN * self.NUDR + Inv_LNFIN * self.PUDR
        UTE_i = self.UTE + Inv_L * self.LUTE + Inv_NFIN * self.NUTE + Inv_LNFIN * self.PUTE
        UTL_i = self.UTL + Inv_L * self.LUTL + Inv_NFIN * self.NUTL + Inv_LNFIN * self.PUTL
        EMOBT_i = self.EMOBT + Inv_L * self.LEMOBT + Inv_NFIN * self.NEMOBT + Inv_LNFIN * self.PEMOBT
        UA1_i = self.UA1 + Inv_L * self.LUA1 + Inv_NFIN * self.NUA1 + Inv_LNFIN * self.PUA1
        UC1_i = self.UC1 + Inv_L * self.LUC1 + Inv_NFIN * self.NUC1 + Inv_LNFIN * self.PUC1
        UD1_i = self.UD1 + Inv_L * self.LUD1 + Inv_NFIN * self.NUD1 + Inv_LNFIN * self.PUD1
        UCSTE_i = self.UCSTE + Inv_L * self.LUCSTE + Inv_NFIN * self.NUCSTE + Inv_LNFIN * self.PUCSTE
        PTWGT_i = self.PTWGT + Inv_L * self.LPTWGT + Inv_NFIN * self.NPTWGT + Inv_LNFIN * self.PPTWGT
        AT_i = self.AT + Inv_L * self.LAT + Inv_NFIN * self.NAT + Inv_LNFIN * self.PAT
        ATCV_i = self.ATCV + Inv_L * self.LATCV + Inv_NFIN * self.NATCV + Inv_LNFIN * self.PATCV
        PRT_i = self.PRT + Inv_L * self.LPRT + Inv_NFIN * self.NPRT + Inv_LNFIN * self.PPRT
        KT1_i = self.KT1 + Inv_L * self.LKT1 + Inv_NFIN * self.NKT1 + Inv_LNFIN * self.PKT1
        TSS_i = self.TSS + Inv_L * self.LTSS + Inv_NFIN * self.NTSS + Inv_LNFIN * self.PTSS
        IIT_i = self.IIT + Inv_L * self.LIIT + Inv_NFIN * self.NIIT + Inv_LNFIN * self.PIIT
        TGIDL_i = self.TGIDL + Inv_L * self.LTGIDL + Inv_NFIN * self.NTGIDL + Inv_LNFIN * self.PTGIDL
        IGT_i = self.IGT + Inv_L * self.LIGT + Inv_NFIN * self.NIGT + Inv_LNFIN * self.PIGT
        UTER_i = self.UTER + Inv_L * self.LUTER + Inv_NFIN * self.NUTER + Inv_LNFIN * self.PUTER
        UTLR_i = self.UTLR + Inv_L * self.LUTLR + Inv_NFIN * self.NUTLR + Inv_LNFIN * self.PUTLR
        UA1R_i = self.UA1R + Inv_L * self.LUA1R + Inv_NFIN * self.NUA1R + Inv_LNFIN * self.PUA1R
        UD1R_i = self.UD1R + Inv_L * self.LUD1R + Inv_NFIN * self.NUD1R + Inv_LNFIN * self.PUD1R
        ATR_i = self.ATR + Inv_L * self.LATR + Inv_NFIN * self.NATR + Inv_LNFIN * self.PATR
        UC1R_i = self.UC1R + Inv_L * self.LUC1R + Inv_NFIN * self.NUC1R + Inv_LNFIN * self.PUC1R

        # Geometrical scaling
        # NFIN scaling
        if self.PHIGN1 != 0.0:
            PHIG_i = PHIG_i * (1.0 + self.PHIGN1 / self.NFIN * self.lln(1.0 + self.NFIN / self.PHIGN2))

        if self.ETA0N1 != 0.0:
            ETA0_i = ETA0_i * (1.0 + self.ETA0N1 / self.NFIN * self.lln(1.0 + self.NFIN / self.ETA0N2))

        if self.CDSCN1 != 0.0:
            CDSC_i = CDSC_i * (1.0 + self.CDSCN1 / self.NFIN * self.lln(1.0 + self.NFIN / self.CDSCN2))

        if self.CDSCDN1 != 0.0:
            CDSCD_i = CDSCD_i * (1.0 + self.CDSCDN1 / self.NFIN * self.lln(1.0 + self.NFIN / self.CDSCDN2))

        if self.CDSCDRN1 != 0.0:
            CDSCDR_i = CDSCDR_i * (1.0 + self.CDSCDRN1 / self.NFIN * self.lln(1.0 + self.NFIN / self.CDSCDRN2))

        if self.VSATN1 != 0.0:
            VSAT_i = VSAT_i * (1.0 + self.VSATN1 / self.NFIN * self.lln(1.0 + self.NFIN / self.VSATN2))

        if self.VSAT1N1 != 0.0:
            VSAT1_i = VSAT1_i * (1.0 + self.VSAT1N1 / self.NFIN * self.lln(1.0 + self.NFIN / self.VSAT1N2))

        if self.VSAT1RN1 != 0.0:
            VSAT1R_i = VSAT1R_i * (1.0 + self.VSAT1RN1 / self.NFIN * self.lln(1.0 + self.NFIN / self.VSAT1RN2))

        if self.U0N1 != 0.0:
            U0_i = U0_i * (1.0 + self.U0N1 / self.NFIN * self.lln(1.0 + self.NFIN / self.U0N2))

        if 'NFINNOM' in self.given:
            PHIG_i = PHIG_i * (1.0 + (self.NFIN - self.NFINNOM) * self.PHIGLT * Leff)
            ETA0_i = ETA0_i * (1.0 + (self.NFIN - self.NFINNOM) * self.ETA0LT * Leff)
            U0_i = U0_i * (1.0 + (self.NFIN - self.NFINNOM) * self.U0LT * Leff)

        if self.U0N1R != 0.0:
            U0R_i = U0R_i * (1.0 + self.U0N1R / self.NFIN * self.lln(1.0 + self.NFIN / self.U0N2R))

        # Length scaling
        PHIG_i = PHIG_i + self.PHIGL * Leff
        if self.LPA > 0.0:
            U0_i = U0_i * (1.0 - UP_i * pow(Leff, -self.LPA))
        else:
            U0_i = U0_i * (1.0 - UP_i)
        UA_i = UA_i + self.AUA * self.lexp(-Leff / self.BUA)
        UD_i = UD_i + self.AUD * self.lexp(-Leff / self.BUD)
        EU_i = EU_i + self.AEU * self.lexp(-Leff / self.BEU)
        if self.LPAR > 0.0:
            U0R_i = U0R_i * (1.0 - UPR_i * pow(Leff, -self.LPAR))
        else:
            U0R_i = U0R_i * (1.0 - UPR_i)
        UAR_i = UAR_i + self.AUAR * self.lexp(-Leff / self.BUAR)
        UDR_i = UDR_i + self.AUDR * self.lexp(-Leff / self.BUDR)
        EUR_i = EUR_i + self.AEUR * self.lexp(-Leff / self.BEUR)
        if self.RDSMOD == 1:
            RSW_i = RSW_i + self.ARSW * self.lexp(-Leff / self.BRSW)
            RDW_i = RDW_i + self.ARDW * self.lexp(-Leff / self.BRDW)
        else:
            RDSW_i = RDSW_i + self.ARDSW * self.lexp(-Leff / self.BRDSW)
        PCLM_i = PCLM_i + self.APCLM * self.lexp(-Leff / self.BPCLM)
        PCLMR_i = PCLMR_i + self.APCLMR * pow(Leff, -self.BPCLMR)
        MEXP_i = MEXP_i + self.AMEXP * pow(Leff, -self.BMEXP)
        MEXPR_i = MEXPR_i + self.AMEXPR * pow(Leff, -self.BMEXPR)
        PTWG_i = PTWG_i + self.APTWG * self.lexp(-Leff / self.BPTWG)
        PTWGR_i = PTWGR_i + self.APTWG * self.lexp(-Leff / self.BPTWG)
        VSAT_i = VSAT_i + self.AVSAT * self.lexp(-Leff / self.BVSAT)
        VSAT1_i = VSAT1_i + self.AVSAT1 * self.lexp(-Leff / self.BVSAT1)
        VSAT1R_i = VSAT1R_i + self.AVSAT1 * self.lexp(-Leff / self.BVSAT1)
        PSAT_i = PSAT_i + self.APSAT * self.lexp(-Leff / self.BPSAT)
        DVTP0_i = self.DVTP0 + self.ADVTP0 * self.lexp(-Leff / self.BDVTP0)
        DVTP1_i = self.DVTP1 + self.ADVTP1 * self.lexp(-Leff / self.BDVTP1)

        # Parameter range limiting
        if ETA0_i < 0.0:
            ETA0_i = 0.0
        if ETA0R_i < 0.0:
            ETA0R_i = 0.0
        if LPE0_i < -Leff:
            LPE0_i = 0.0
        if K0SI_i <= 0.0:
            K0SI_i = 0.0
        if K2SI_i <= 0.0:
            K2SI_i = 0.0
        if PHIBE_i < 0.2 and self.BULKMOD != 0:
            PHIBE_i = 0.2
        if PHIBE_i > 1.2 and self.BULKMOD != 0:
            PHIBE_i = 1.2
        if PSAT_i < 2.0:
            PSAT_i = 2.0
        if U0_i < 0.0:
            U0_i = 0.03
        if UA_i < 0.0:
            UA_i = 0.0
        if EU_i < 0.0:
            EU_i = 0.0
        if UD_i < 0.0:
            UD_i = 0.0
        if UCS_i < 0.0:
            UCS_i = 0.0
        if ETAMOB_i < 0.0:
            ETAMOB_i = 0.0
        RDSWMIN_i = self.RDSWMIN
        if RDSWMIN_i < 0.0:
            RDSWMIN_i = 0.0
        if RDSW_i < 0.0:
            RDSW_i = 0.0
        RSWMIN_i = self.RSWMIN
        if RSWMIN_i < 0.0:
            RSWMIN_i = 0.0
        if RSW_i < 0.0:
            RSW_i = 0.0
        RDWMIN_i = self.RDWMIN
        if RDWMIN_i < 0.0:
            RDWMIN_i = 0.0
        if RDW_i < 0.0:
            RDW_i = 0.0
        if PRWGD_i < 0.0:
            PRWGD_i = 0.0
        if PRWGS_i < 0.0:
            PRWGS_i = 0.0
        if U0R_i < 0:
            U0R_i = 0.0
        if UAR_i < 0.0:
            UAR_i = 0.0
        if EUR_i < 0.0:
            EUR_i = 0.0
        if UDR_i < 0.0:
            UDR_i = 0.0
        if MEXP_i < 2.0:
            MEXP_i = 2.0
        if MEXPR_i < 2.0:
            MEXPR_i = 2.0
        if PTWG_i < 0:
            PTWG_i = 0.0
        if CGIDL_i < 0.0:
            CGIDL_i = 0.0
        if CGISL_i < 0.0:
            CGISL_i = 0.0
        if self.LINTIGEN >= (Leff / 2.0):
            LINTIGEN_i = 0.0
        else:
            LINTIGEN_i = self.LINTIGEN

        # Geometry-Depent source/drain resistance
        if self.RGEOMOD == 0:
            RSourceGeo = self.RSHS * self.NRS
            RDrainGeo = self.RSHD * self.NRD
        else:
            # Area and perimeter calculation
            if self.HEPI > 0.0:
                Arsd = self.FPITCH * self.HFIN + (self.TFIN + (self.FPITCH - self.TFIN) * self.CRATIO) * self.HEPI
            else:
                Arsd = self.FPITCH * max(1.0e-9, self.HFIN + self.HEPI)
            Prsd = self.FPITCH + self.DELTAPRSD

            # Resistivity calculation
            if 'RHORSD' in self.given:
                rhorsd = self.RHORSD
            else:
                mu_max = 1417.0 if self.TYPE == 1 else 470.5
                if self.TYPE == 1:
                    mu_rsd = (52.2 + (mu_max - 52.2) / (1.0 + pow(self.NSD / 9.68e22, 0.680)) - 43.4 / (1.0 + pow(3.43e26 / self.NSD, 2.0))) * 1.0e-4
                else:
                    mu_rsd = (44.9 + (mu_max - 44.9) / (1.0 + pow(self.NSD / 2.23e22, 0.719)) - 29.0 / (1.0 + pow(6.10e26 / self.NSD, 2.0))) * 1.0e-4
                rhorsd = 1.0 / (1.60219e-19 * self.NSD * mu_rsd)

            # Component: spreading resistance (extension -> hdd)
            thetarsp = 55.0 * 3.14159265358979323846 / 180.0
            afin = min(Arsd, max(1.0e-18, self.TFIN * (self.HFIN + min(0.0, self.HEPI))))
            T1 = 1.0 / tan(thetarsp)
            Rsp = rhorsd * T1 / (sqrt(3.14159265358979323846) * self.NFIN) * (1.0 / sqrt(afin) - 2.0 / sqrt(Arsd) + sqrt(afin / (Arsd * Arsd)))

            # Component: contact resistance
            arsd_total = Arsd * self.NFIN + self.ARSDEND
            prsd_total = Prsd * self.NFIN + self.PRSDEND
            lt = sqrt(self.RHOC * arsd_total / (rhorsd * prsd_total))
            alpha = self.LRSD / lt
            T0 = self.lexp(alpha + alpha)

            if self.SDTERM == 1.0:
                eta = rhorsd * lt / RHOC
                T1 = T0 * (1.0 + eta)
                T2 = T1 + 1.0 - eta
                T3 = T1 - 1.0 + eta
            else:
                T2  = T0 + 1.0
                T3  = T0 - 1.0
            RrsdTML = rhorsd * lt * T2 / (arsd_total * T3)

            if self.HEPI < -1.0e-10:
                Rrsdside = self.RHOC / (-self.HEPI * self.TFIN * self.NFIN)
                Rrsd = (RrsdTML + Rsp) * Rrsdside / (RrsdTML + Rsp + Rrsdside)
            else:
                Rrsd = RrsdTML + Rsp

            Rdsgeo = Rrsd / self.NF * max(0.0, self.RGEOA + self.RGEOB * self.TFIN + self.RGEOC * self.FPITCH + self.RGEOD * self.LRSD + self.RGEOE * self.HEPI)
            RSourceGeo = Rdsgeo
            RDrainGeo = Rdsgeo

        # Clamping of source/drain resistances
        if RSourceGeo <= 1.0e-3:
            RSourceGeo = 1.0e-3

        if RDrainGeo <= 1.0e-3:
            RDrainGeo = 1.0e-3

        if self.RDSMOD == 1:
            if RSWMIN_i <= 0.0:
                RSWMIN_i = 0.0
            if RDWMIN_i <= 0.0:
                RDWMIN_i = 0.0
            if RSW_i <= 0.0:
                RSW_i = 0.0
            if RDW_i <= 0.0:
                RDW_i = 0.0
        else:
            if RDSWMIN_i <= 0.0:
                RDSWMIN_i = 0.0
            if RDSW_i <= 0.0:
                RDSW_i = 0.0

        # Mobility degradation
        EeffFactor = 1.0e-8 / (epsratio * self.EOT)
        WeffWRFactor = 1.0 / (pow(Weff0 * 1.0e6, WR_i) * NFINtotal)
        litl = sqrt(epsratio * self.EOT * 0.5 * self.TFIN)

        if 'THETASCE' not in self.given:
            tmp = DVT1_i * Leff / scl + 1.0e-6
            if tmp < 40.0:
                Theta_SCE = 0.5 / (cosh(tmp) - 1.0)
            else:
                Theta_SCE = exp(-tmp)
        else:
            Theta_SCE = self.THETASCE

        if 'THETASW' not in self.given:
            tmp = DVT1SS_i * Leff / scl + 1.0e-6
            if tmp < 40.0:
                Theta_SW = 0.5 / (cosh(tmp) - 1.0)
            else:
                Theta_SW = exp(-tmp)
        else:
            Theta_SW = self.THETASW

        if 'THETADIBL' not in self.given:
            tmp = DSUB_i * Leff / scl + 1.0e-6
            if tmp < 40.0:
                Theta_DIBL = 0.5 / (cosh(tmp) - 1.0)
            else:
                Theta_DIBL = exp(-tmp)
        else:
            Theta_DIBL = self.THETADIBL

        Theta_RSCE = sqrt(1.0 + LPE0_i / Leff) - 1.0

        tmp = DSUB_i * Leff / scl + 1.0e-6
        if tmp < 40.0:
            Theta_DITS = 1.0 / max((1.0 + self.DVTP2 * (cosh(tmp) - 2.0)), 1.0e-6)
        else:
            Theta_DITS = exp(-tmp) / max((exp(-tmp) + self.DVTP2), 1.0e-6)

        nbody = NBODY_i
        qbs = 1.60219e-19 * nbody * Ach / Cins

        # Gate Current
        if self.TYPE == 1:
            Aechvb = 4.97232e-7  # NMOS
            Bechvb = 7.45669e11  # NMOS
        else:
            Aechvb = 3.42537e-7  # PMOS
            Bechvb = 1.16645e12  # PMOS

        T0 = self.TOXG * self.TOXG
        T1 = self.TOXG * POXEDGE_i
        T2 = T1 * T1
        Toxratio = self.lexp(NTOX_i * self.lln(self.TOXREF / self.TOXG)) / T0
        Toxratioedge = self.lexp(NTOX_i * self.lln(self.TOXREF / T1)) / T2
        igsd_mult0 = Weff0 * Aechvb * Toxratioedge

        if self.TNOM < -273.15:
            Tnom = 300.15
        else:
            Tnom = self.TNOM + 273.15

        # $temperature = self.temp + self.CONSTCtoK
        DevTemp = self.temp + 273.15 + self.DTEMP
        TRatio = DevTemp / Tnom
        delTemp = DevTemp - Tnom
        Vtm = 8.617087e-5 * DevTemp
        Vtm0 = 8.617087e-5 * Tnom
        Eg = self.BG0SUB - self.TBGASUB * DevTemp * DevTemp / (DevTemp + self.TBGBSUB)
        Eg0 = self.BG0SUB - self.TBGASUB * Tnom * Tnom / (Tnom + self.TBGBSUB)
        T1 = (DevTemp / 300.15) * sqrt(DevTemp / 300.15)
        ni = self.NI0SUB * T1 * self.lexp(self.BG0SUB / (2.0 * 8.617087e-5 * 300.15) - Eg / (2.0 * Vtm))
        Nc = self.NC0SUB * T1
        ThetaSS = self.hypsmooth(1.0 + TSS_i * delTemp - 1.0e-6, 1.0e-3)

        # Quantum mechanical Vth correction
        kT = Vtm * 1.60219e-19
        T0 = 1.05457e-34 * 3.14159265358979323846 / (2.0 * Ach / Weff_UFCM)
        E0 = T0 * T0 / (2.0 * mx)
        E0prime = T0 * T0 / (2.0 * mxprime)
        E1 = 4.0 * E0
        E1prime = 4.0 * E0prime
        T1 = gprime * mdprime / (gfactor * md)
        gam0 = 1.0 + T1 * self.lexp((E0 - E0prime) / kT)
        gam1 = gam0 + self.lexp((E0 - E1) / kT) + T1 * self.lexp((E0 - E1prime) / kT)
        T2 = -Vtm * self.lln(gfactor * md / (3.14159265358979323846 * 1.05457e-34 * 1.05457e-34 * Nc) * kT / (2.0 * Ach / Weff_UFCM) * gam1)
        dvch_qm = QMFACTOR_i * (E0 / 1.60219e-19 + T2)

        # Temperature dependence
        ETA0_t = self.tempdep(ETA0_i, self.TETA0, delTemp, self.TEMPMOD)
        ETA0R_t = self.tempdep(ETA0R_i, self.TETA0R, delTemp, self.TEMPMOD)
        T1 = U0_i * pow(TRatio, UTE_i)
        U0_t = T1 + self.hypmax(UTL_i * delTemp, -0.9 * T1, 1.0e-4)
        u0 = U0_t
        T1 = U0R_i * pow(TRatio, UTER_i)
        u0r = T1 + self.hypmax(UTLR_i * delTemp, -0.9 * T1, 1.0e-4)
        ETAMOB_t = self.tempdep(ETAMOB_i, EMOBT_i, delTemp, self.TEMPMOD)
        UA_t = UA_i + self.hypmax(UA1_i * delTemp, -UA_i, 1.0e-6)
        UAR_t = UAR_i + self.hypmax(UA1R_i * delTemp, -UAR_i, 1.0e-6)
        if self.TEMPMOD == 0:
            UC_t = self.tempdep(UC_i, UC1_i, delTemp, 0)
            UCR_t = self.tempdep(UCR_i, UC1R_i, delTemp, 0)
        else:
            UC_t = UC_i + UC1_i * delTemp
            UCR_t = UCR_i + UC1R_i * delTemp
        UD_t = UD_i * pow(TRatio, UD1_i)
        UDR_t = UDR_i * pow(TRatio, UD1R_i)
        UCS_t = UCS_i * pow(TRatio, UCSTE_i)
        rdstemp = self.hypsmooth(1.0 + PRT_i * delTemp - 1.0e-6, 1.0e-3)
        RSDR_t = self.tempdep(self.RSDR, self.TRSDR, delTemp, self.TEMPMOD)
        RSDRR_t = self.tempdep(self.RSDRR, self.TRSDR, delTemp, self.TEMPMOD)
        RDDR_t = self.tempdep(self.RDDR, self.TRDDR, delTemp, self.TEMPMOD)
        RDDRR_t = self.tempdep(self.RDDRR, self.TRDDR, delTemp, self.TEMPMOD)
        VSAT_t = self.tempdep(VSAT_i, -AT_i, delTemp, self.TEMPMOD)
        if VSAT_t < 1000:
            VSAT_t = 1000
        VSATR_t = self.tempdep(VSATR_i, -ATR_i, delTemp, self.TEMPMOD)
        if VSATR_t < 1000:
            VSATR_t = 1000
        VSAT1_t = self.tempdep(VSAT1_i, -AT_i, delTemp, self.TEMPMOD)
        if VSAT1_t < 1000:
            VSAT1_t = 1000
        VSAT1R_t = self.tempdep(VSAT1R_i, -AT_i, delTemp, self.TEMPMOD)
        if VSAT1R_t < 1000:
            VSAT1R_t = 1000
        MEXP_t = self.hypsmooth(MEXP_i * (1.0 + self.TMEXP * delTemp) - 2.0, 1.0e-3) + 2.0
        MEXPR_t = self.hypsmooth(MEXPR_i * (1.0 + self.TMEXPR * delTemp) - 2.0, 1.0e-3) + 2.0
        PTWG_t = self.tempdep(PTWG_i, -PTWGT_i, delTemp, self.TEMPMOD)
        PTWGR_t = self.tempdep(PTWGR_i, -PTWGT_i, delTemp, self.TEMPMOD)
        dvth_temp = (KT1_i + self.KT1L / Leff) * (TRatio - 1.0)
        BETA0_t = BETA0_i * pow(TRatio, IIT_i)
        SII0_t = SII0_i * (self.hypsmooth(1.0 + TII_i * (TRatio - 1.0) - 0.01, 1.0e-3) + 0.01)
        K0_t = K0_i + K01_i * delTemp
        K0SI_t = K0SI_i + self.hypmax(K0SI1_i * delTemp, -K0SI_i, 1.0e-6)
        K2SI_t = K2SI_i + self.hypmax(K2SI1_i * delTemp, -K2SI_i, 1.0e-6)
        K1_t = K1_i + self.hypmax(K11_i * delTemp, -K1_i, 1.0e-6)
        K2SAT_t = K2SAT_i + K2SAT1_i * delTemp
        A1_t = A1_i + A11_i * delTemp
        A2_t = A2_i + A21_i * delTemp
        K2_t = K2_i + self.hypmax(K21_i * delTemp, -K2_i, 1.0e-6)
        K0SISAT_t = K0SISAT_i + K0SISAT1_i * delTemp
        K2SISAT_t = K2SISAT_i + K2SISAT1_i * delTemp
        AIGBINV_t = AIGBINV_i + self.hypmax(AIGBINV1_i * delTemp, -AIGBINV_i, 1.0e-6)
        AIGBACC_t = AIGBACC_i + self.hypmax(AIGBACC1_i * delTemp, -AIGBACC_i, 1.0e-6)
        AIGC_t = AIGC_i + self.hypmax(AIGC1_i * delTemp, -AIGC_i, 1.0e-6)
        AIGS_t = AIGS_i + self.hypmax(AIGS1_i * delTemp, -AIGS_i, 1.0e-6)
        AIGD_t = AIGD_i + self.hypmax(AIGD1_i * delTemp, -AIGD_i, 1.0e-6)
        BGIDL_t = BGIDL_i * self.hypsmooth(1.0 + TGIDL_i * delTemp - 1.0e-6, 1.0e-3)
        BGISL_t = BGISL_i * self.hypsmooth(1.0 + TGIDL_i * delTemp - 1.0e-6, 1.0e-3)
        ALPHA0_t = ALPHA0_i + self.hypmax(self.ALPHA01 * delTemp, -ALPHA0_i, 1.0e-6)
        ALPHA1_t = ALPHA1_i + self.hypmax(self.ALPHA11 * delTemp, -ALPHA1_i, 1.0e-6)
        ALPHAII0_t = ALPHAII0_i + self.hypmax(self.ALPHAII01 * delTemp, -ALPHAII0_i, 1.0e-25)
        ALPHAII1_t = ALPHAII1_i + self.hypmax(self.ALPHAII11 * delTemp, -ALPHAII1_i, 1.0e-20)
        igtemp = self.lexp(IGT_i * self.lln(TRatio))
        igsd_mult = igsd_mult0 * igtemp
        if self.BULKMOD != 0:
            T0 = Eg0 / Vtm0 - Eg / Vtm
            T1 = self.lln(TRatio)
            T3 = self.lexp((T0 + self.XTIS * T1) / self.NJS)
            JSS_t = self.JSS * T3
            JSWS_t = self.JSWS * T3
            JSWGS_t = self.JSWGS * T3
            T3 = self.lexp((T0 + self.XTID * T1) / self.NJD)
            JSD_t = self.JSD * T3
            JSWD_t = self.JSWD * T3
            JSWGD_t = self.JSWGD * T3
            JTSS_t = self.JTSS * self.lexp(Eg0 * self.XTSS * (TRatio - 1.0) / Vtm)
            JTSD_t = self.JTSD * self.lexp(Eg0 * self.XTSD * (TRatio - 1.0) / Vtm)
            JTSSWS_t = self.JTSSWS * self.lexp(Eg0 * self.XTSSWS * (TRatio - 1.0) / Vtm)
            JTSSWD_t = self.JTSSWD * self.lexp(Eg0 * self.XTSSWD * (TRatio - 1.0) / Vtm)
            JTSSWGS_t = self.JTSSWGS * (sqrt(self.JTWEFF / Weff0) + 1.0) * self.lexp(Eg0 * self.XTSSWGS * (TRatio - 1.0) / Vtm)
            JTSSWGD_t = self.JTSSWGD * (sqrt(self.JTWEFF / Weff0) + 1.0) * self.lexp(Eg0 * self.XTSSWGD * (TRatio - 1.0) / Vtm)
            # All NJT's smoothed to 0.01 to prevent divide-by-zero / negative values
            NJTS_t = self.hypsmooth(self.NJTS * (1.0 + self.TNJTS * (TRatio - 1.0)) - 0.01, 1.0e-3) + 0.01
            NJTSD_t = self.hypsmooth(self.NJTSD * (1.0 + self.TNJTSD * (TRatio - 1.0)) - 0.01, 1.0e-3) + 0.01
            NJTSSW_t = self.hypsmooth(self.NJTSSW * (1.0 + self.TNJTSSW * (TRatio - 1.0)) - 0.01, 1.0e-3) + 0.01
            NJTSSWD_t = self.hypsmooth(self.NJTSSWD * (1.0 + self.TNJTSSWD * (TRatio - 1.0)) - 0.01, 1.0e-3) + 0.01
            NJTSSWG_t = self.hypsmooth(self.NJTSSWG * (1.0 + self.TNJTSSWG * (TRatio - 1.0)) - 0.01, 1.0e-3) + 0.01
            NJTSSWGD_t = self.hypsmooth(self.NJTSSWGD * (1.0 + self.TNJTSSWGD * (TRatio - 1.0)) - 0.01, 1.0e-3) + 0.01

        if 'VFBSD' not in self.given:
            if self.NGATE > 0.0:
                vfbsd = devsign * (self.hypsmooth(0.5 * Eg - Vtm * self.lln(self.NGATE / ni), 1.0e-4) - (0.5 * Eg - devsign * (0.5 * Eg - self.hypsmooth(0.5 * Eg - Vtm * self.lln(self.NSD / ni), 1.0e-4))))
            else:
                vfbsd = devsign * (PHIG_i - (self.EASUB + 0.5 * Eg - devsign * (0.5 * Eg - self.hypsmooth(0.5 * Eg - Vtm * self.lln(self.NSD / ni), 1.0e-4))))
        else:
            vfbsd = self.VFBSD

        if 'VFBSDCV' not in self.given:
            vfbsdcv = vfbsd
        else:
            vfbsdcv = self.VFBSDCV

        phib = Vtm * self.lln(nbody / ni)
        vbi = Vtm * self.lln(nbody * self.NSD / (ni * ni))

        # deltaPhi definition and polysilicon depletion
        # deltaPhi: workfunction difference between the gate and the n+ source.
        deltaPhi = devsign * (PHIG_i - (self.EASUB + (0.0 if self.TYPE == 1 else Eg)))

        # Mobility degradation
        eta_mu = 0.5 * ETAMOB_t
        if self.TYPE != 1:
            eta_mu = 1.0 / 3.0 * ETAMOB_t

        # Junction current and capacitance
        if self.BULKMOD != 0:
            # Source-side junction current
            Isbs = self.ASEJ * JSS_t + self.PSEJ * JSWS_t + self.TFIN * NFINtotal * JSWGS_t
            if Isbs > 0.0:
                Nvtms = Vtm * self.NJS
                XExpBVS = self.lexp(-self.BVS / Nvtms) * self.XJBVS
                T2 = max(self.IJTHSFWD / Isbs, 10.0)
                Tb = 1.0 + T2 - XExpBVS
                VjsmFwd = Nvtms * self.lln(0.5 * (Tb + sqrt(Tb * Tb + 4.0 * XExpBVS)))
                T0 = self.lexp(VjsmFwd / Nvtms)
                IVjsmFwd = Isbs * (T0 - XExpBVS / T0 + XExpBVS - 1.0)
                SslpFwd = Isbs * (T0 + XExpBVS / T0) / Nvtms
                T2 = self.hypsmooth(self.IJTHSREV / Isbs - 10.0, 1.0e-3) + 10.0
                VjsmRev = -self.BVS - Nvtms * self.lln((T2 - 1.0) / self.XJBVS)
                T1 = self.XJBVS * self.lexp(-(self.BVS + VjsmRev) / Nvtms)
                IVjsmRev = Isbs * (1.0 + T1)
                SslpRev = -Isbs * T1 / Nvtms

            # Drain-side junction current
            Isbd = self.ADEJ * JSD_t + self.PDEJ * JSWD_t + self.TFIN * NFINtotal * JSWGD_t
            if Isbd > 0.0:
                Nvtmd = Vtm * self.NJD
                XExpBVD = self.lexp(-self.BVD / Nvtmd) * self.XJBVD
                T2 = max(self.IJTHDFWD / Isbd, 10.0)
                Tb = 1.0 + T2 - XExpBVD
                VjdmFwd = Nvtmd * self.lln(0.5 * (Tb + sqrt(Tb * Tb + 4.0 * XExpBVD)))
                T0 = self.lexp(VjdmFwd / Nvtmd)
                IVjdmFwd = Isbd * (T0 - XExpBVD / T0 + XExpBVD - 1.0)
                DslpFwd = Isbd * (T0 + XExpBVD / T0) / Nvtmd
                T2 = self.hypsmooth(IJTHDREV / Isbd - 10.0, 1.0e-3) + 10.0
                VjdmRev = -self.BVD - Nvtmd * self.lln((T2 - 1.0) / self.XJBVD)
                T1 = self.XJBVD * self.lexp(-(self.BVD + VjdmRev) / Nvtmd)
                IVjdmRev = Isbd * (1.0 + T1)
                DslpRev = -Isbd * T1 / Nvtmd

        # Generation-Recombination Current
        T0 = Eg / Vtm * (TRatio - 1.0)
        T1 = T0 / NTGEN_i
        igentemp = self.lexp(T1)

        # Bias-dependent calculations
        # Load terminal voltages

        vgs_noswap = devsign * (self.vg - self.vs)
        vds_noswap = devsign * (self.vd - self.vs)
        vgd_noswap = devsign * (self.vg - self.vd)
        ves_jct = devsign * (self.vb - self.vs)
        ved_jct = devsign * (self.vb - self.vd)
        vge = devsign * (self.vg - self.vb)

        # Source-drain interchange
        sigvds = 1.0
        if vds_noswap < 0.0:
            sigvds = -1.0
            vgs = vgs_noswap - vds_noswap
            vds = -1.0 * vds_noswap
            ves = ved_jct
        else:
            vgs = vgs_noswap
            vds = vds_noswap
            ves = ves_jct
        vgsfb = vgs - deltaPhi

        # Initialize certain variables to zero to prevent unnecessary update
        etaiv = Qes = Qesj = Qeg = Qed = Qedj = 0.0

        # Vds smoothing
        vdsx = sqrt(vds * vds + 0.01) - 0.1

        # Ves smoothing
        if self.BULKMOD != 0:
            vesx = ves - 0.5 * (vds - vdsx)
            vesmax = 0.95 * PHIBE_i
            T2 = vesmax - vesx - 1.0e-3
            veseff = vesmax - 0.5 * (T2 + sqrt(T2 * T2 + 0.004 * vesmax))

        # Asymmetry model
        T0 = tanh(0.6 * vds_noswap / Vtm)
        wf = 0.5 + 0.5 * T0
        wr = 1.0 - wf
        if self.ASYMMOD != 0:
            CDSCD_a = CDSCDR_i * wr + CDSCD_i * wf
            ETA0_a = ETA0R_t * wr + ETA0_t * wf
            PDIBL1_a = PDIBL1R_i * wr + PDIBL1_i * wf
            PDIBL2_a = PDIBL2R_i * wr + PDIBL2_i * wf
            MEXP_a = MEXPR_t * wr + MEXP_t * wf
            PTWG_a = PTWGR_t * wr + PTWG_t * wf
            VSAT1_a = VSAT1R_t * wr + VSAT1_t * wf
            RSDR_a = RSDRR_t * wr + RSDR_t * wf
            RDDR_a = RDDRR_t * wr + RDDR_t * wf
            PCLM_a = PCLMR_i * wr + PCLM_i * wf
            VSAT_a = VSATR_t * wr + VSAT_t * wf
            KSATIV_a = KSATIVR_i * wr + KSATIV_i * wf
            DVTSHIFT_a = DVTSHIFTR_i * wr + DVTSHIFT_i * wf
            CIT_a = CITR_i * wr + CIT_i * wf
            u0_a = u0r * wr + u0 * wf
            UA_a = UAR_t * wr + UA_t * wf
            UD_a = UDR_t * wr + UD_t * wf
            UC_a = UCR_t * wr + UC_t * wf
            EU_a = EUR_i * wr + EU_i * wf
        else:
            CDSCD_a = CDSCD_i
            ETA0_a = ETA0_t
            PDIBL1_a = PDIBL1_i
            PDIBL2_a = PDIBL2_i
            MEXP_a = MEXP_t
            PTWG_a = PTWG_t
            VSAT1_a = VSAT1_t
            RSDR_a = RSDR_t
            RDDR_a = RDDR_t
            PCLM_a = PCLM_i
            VSAT_a = VSAT_t
            KSATIV_a = KSATIV_i
            DVTSHIFT_a = DVTSHIFT_i
            CIT_a = CIT_i
            u0_a = u0
            UA_a = UA_t
            UD_a = UD_t
            UC_a = UC_t
            EU_a = EU_i

        # Drain saturation voltage
        inv_MEXP = 1.0 / MEXP_a

        # SCE, DIBL, SS degradation effects Ref: BSIM4
        phist = 0.4 + phib + PHIN_i
        T1 = 2.0 * (Cins / Weff_UFCM) / (rc + 2.0)
        cdsc = Theta_SW * (CDSC_i + CDSCD_a * vdsx)

        if 'NVTM' not in self.given:
            nVtm = Vtm * ThetaSS * (1.0 + (CIT_a + cdsc) / T1)
        else:
            nVtm = self.NVTM

        # temp deped UFCM
        qdep = Qdep_ov_Cins / nVtm
        vth_fixed_factor_SI = log(Cins * nVtm / (1.60219e-19 * Nc * 2.0 * Ach))
        vth_fixed_factor_Sub = log((qdep * rc) * (qdep * rc) / ((exp(qdep * rc) - qdep * rc - 1.0))) + vth_fixed_factor_SI
        q0 = 10.0 * nVtm / rc + 2.0 * qbs

        # New QM parameter calculation: fieldnormalizationfactor, auxQMfact, QMFACTORCVfinal
        fieldnormalizationfactor = Vtm * Cins / (Weff_UFCM * epssub)
        auxQMfact = pow(((3.0 / 4.0) * 3.0 * 1.05457e-34 * 2.0 * 3.14159265358979323846 * 1.60219e-19 / (4.0 * sqrt(2.0 * mx))), 2.0 / 3.0)
        QMFACTORCVfinal = self.QMFACTORCV * auxQMfact * pow(fieldnormalizationfactor, 2.0 / 3.0) * (1.0 / (1.60219e-19 * Vtm))

        dvth_vtroll = -DVT0_i * Theta_SCE * (vbi - phist)
        dvth_dibl = -ETA0_a * Theta_DIBL * vdsx + (DVTP0_i * Theta_DITS * pow(vdsx, DVTP1_i))
        dvth_rsce = K1RSCE_i * Theta_RSCE * sqrt(phist)
        dvth_all = dvth_vtroll + dvth_dibl + dvth_rsce + dvth_temp + DVTSHIFT_a
        vgsfb = vgsfb - dvth_all

        # Vgs Clamping for Inversion Region Calculation in Accumulation
        beta0 = u0_a * cox * Weff0 / Leff
        T0 = -(dvch_qm + nVtm * self.lln(2.0 * cox * self.IMIN / (beta0 * nVtm * 1.60219e-19 * Nc * self.TFIN)))
        T1 = vgsfb + T0 + self.DELVTRAND
        vgsfbeff = self.hypsmooth(T1 , 1.0e-4) - T0

        # Core Model Calculation at Source Side
        vch = 0.0 + dvch_qm

        if self.BULKMOD != 0:
            T1 = self.hypsmooth(2.0 * phib + vch - ves, 0.1)
            T3 = (-K1_t / (2.0 * nVtm)) * (sqrt(T1) - sqrt(2.0 * phib))
            T0 = -qdep - T3 + vth_fixed_factor_Sub + QMFACTORCVfinal * pow(-qdep, 2.0/3.0)
            T1 = -qdep - T3 + vth_fixed_factor_SI
        else:
            T0 = -qdep + vth_fixed_factor_Sub + QMFACTORCVfinal * pow(-qdep, 2.0/3.0)
            T1 = -qdep + vth_fixed_factor_SI

        T2 = (vgsfbeff - vch) / nVtm
        F0 = -T2 + T1
        T3 = 0.5 * (T2 - T0)
        qm = exp(T3)
        if qm > 1.0e-7:
            T7 = log(1.0 + qm)
            qm = 2.0 * (1.0 - sqrt(1.0 + T7 * T7))
            T8 = (qm * self.ALPHA_UFCM + qdep) * rc
            T4 = T8 / (exp(T8) - T8 - 1.0)
            T5 = T8 * T4
            e0 = F0 - qm + log(-qm) + log(T5) + QMFACTORCVfinal * pow(-(qm + qdep), 2.0 / 3.0)
            e1 = -1.0 + 1.0 / qm + (2.0 / T8 - T4 - 1.0) * rc - (2.0 / 3.0) * QMFACTORCVfinal * pow(-(qm + qdep), -1.0 / 3.0)
            e2 = -1.0 / (qm * qm) - (2.0 / 9.0) * QMFACTORCVfinal * pow(-(qm + qdep), -4.0/3.0)
            qm = qm - (e0 / e1) * (1.0 + (e0 * e2) / (2.0 * e1 * e1))
            T8 = (qm * self.ALPHA_UFCM + qdep) * rc
            T4 = T8 / (exp(T8) - T8 - 1.0)
            T5 = T8 * T4
            e0 = F0 - qm + log(-qm) + log(T5) + QMFACTORCVfinal * pow(-(qm + qdep), 2.0 / 3.0)
            e1 = -1.0 + 1.0 / qm + (2.0 / T8 - T4 - 1.0) * rc - (2.0 / 3.0) * QMFACTORCVfinal * pow(-(qm + qdep), -1.0 / 3.0)
            e2 = -1.0 / (qm * qm) - (2.0 / 9.0) * QMFACTORCVfinal * pow(-(qm + qdep), -4.0/3.0)
            qm = qm - (e0 / e1) * (1.0 + (e0 * e2) / (2.0 * e1 * e1))
        else:
            qm = -qm * qm
        qis = -qm * nVtm

        # Drain saturation voltage
        Eeffs = EeffFactor * (qbs + eta_mu * qis)
        qb0 = 1.0e-2 / cox
        T2 = pow(0.5 * (1.0 + abs(qis / qb0)), UCS_t)
        if self.BULKMOD != 0:
            T3 = (UA_a + UC_a * veseff) * pow(abs(Eeffs), EU_a) + UD_a / T2
        else:
            T3 = UA_a * pow(abs(Eeffs), EU_a) + UD_a / T2

        Dmobs = 1.0 + T3
        Dmobs = Dmobs / self.U0MULT

        if self.RDSMOD == 1:
            Rdss = 0.0
        elif self.RDSMOD == 0:
            T4 = 1.0 + PRWGS_i * qis
            T1 = 1.0 / T4
            T0 = 0.5 * (T1 + sqrt(T1 * T1 + 0.01))
            Rdss = (RDSWMIN_i + RDSW_i * T0) * WeffWRFactor * NFINtotal * rdstemp
        else:
            T4 = 1.0 + PRWGS_i * qis
            T1 = 1.0 / T4
            T0 = 0.5 * (T1 + sqrt(T1 * T1 + 0.01))
            Rdss = (RSourceGeo + RDrainGeo + RDSWMIN_i + RDSW_i * T0) * WeffWRFactor * NFINtotal * rdstemp
        Esat = 2.0 * VSAT_a / u0_a * Dmobs
        EsatL = Esat * Leff
        T6 = KSATIV_a * (qis +  2 * Vtm)

        if Rdss == 0.0:
            Vdsat = EsatL * T6 / (EsatL + T6)
        else:
            WVCox = Weff0 * VSAT_a * cox
            T0 = WVCox * Rdss
            Ta = 2.0 * T0
            Tb = T6 + EsatL + 3.0 * T6 * T0
            Tc = T6 * (EsatL + 2.0 * T6 * T0)
            Vdsat = (Tb - sqrt(Tb * Tb - 2.0 * Ta * Tc)) / Ta

        Vdsat = self.hypsmooth(Vdsat - 1.0e-3, 1.0e-5) + 1.0e-3
        T7 = pow(vds / Vdsat , MEXP_a)
        T8 = pow(1.0 + T7, inv_MEXP)
        Vdseff = vds / T8

        if Vdseff > vds:
            Vdseff = vds

        # Core model calculation at drain side
        vch = Vdseff + dvch_qm

        if self.BULKMOD != 0:
            T1 = self.hypsmooth(2.0 * phib + vch - ves, 0.1)
            T3 = (-K1_t / (2.0 * nVtm)) * (sqrt(T1) - sqrt(2.0 * phib))
            T0 = -qdep - T3 + vth_fixed_factor_Sub + QMFACTORCVfinal * pow(-qdep, 2.0 / 3.0)
            T1 = -qdep - T3 + vth_fixed_factor_SI
        else:
            T0 = -qdep + vth_fixed_factor_Sub + QMFACTORCVfinal * pow(-qdep, 2.0 / 3.0)
            T1 = -qdep + vth_fixed_factor_SI
        T2 = (vgsfbeff - vch) / nVtm
        F0 = -T2 + T1
        T3 = (T2 - T0) * 0.5
        qm = exp(T3)
        if qm > 1.0e-7:
            T7 = log(1.0 + qm)
            qm = 2.0 * (1.0 - sqrt(1.0 + T7 * T7))
            T8 = (qm * self.ALPHA_UFCM + qdep) * rc
            T4 = T8 / (exp(T8) - T8 - 1.0)
            T5 = T8 * T4
            e0 = F0 - qm + log(-qm) + log(T5) + QMFACTORCVfinal * pow(-(qm + qdep), 2.0 / 3.0)
            e1 = -1.0 + (1.0 / qm) + (2.0 / T8 - T4 - 1.0) * rc - (2.0 / 3.0) * QMFACTORCVfinal * pow(-(qm + qdep), -1.0 / 3.0)
            e2 = -1.0 / (qm * qm) - (2.0 / 9.0) * QMFACTORCVfinal * pow(-(qm + qdep), -4.0 / 3.0)
            qm = qm - (e0 / e1) * (1.0 + (e0 * e2) / (2.0 * e1 * e1))
            T8 = (qm * self.ALPHA_UFCM + qdep) * rc
            T4 = T8 / (exp(T8) - T8 - 1.0)
            T5 = T8 * T4
            e0 = F0 - qm + log(-qm) + log(T5) + QMFACTORCVfinal * pow(-(qm + qdep), 2.0/3.0)
            e1 = -1.0 + (1.0 / qm) + (2.0 / T8 - T4 - 1.0) * rc - (2.0 / 3.0) * QMFACTORCVfinal * pow(-(qm + qdep), -1.0 / 3.0)
            e2 = -1.0 / (qm * qm) - (2.0 / 9.0) * QMFACTORCVfinal * pow(-(qm + qdep), -4.0 / 3.0)
            qm = qm - (e0 / e1) * (1.0 + (e0 * e2) / (2.0 * e1 * e1))
        else:
            qm = -qm * qm
        qid = -qm * nVtm

        qba = 0.0
        if self.BULKMOD != 0:
            T9 = (K1_t / (2.0 * nVtm)) * sqrt(Vtm)
            T0 = T9 / 2.0
            T2 = (vge - (deltaPhi - Eg - Vtm * log(self.NBODY / Nc) + self.DELVFBACC)) / Vtm
            if (T2 * Vtm) > phib + T9 * sqrt(phib * Vtm):
                T1 = sqrt(T2 - 1.0 + T0 * T0) - T0
                T10 = 1.0 + T1 * T1
            else:
                T3 = T2 * 0.5 - 3.0 * (1.0 + T9 / sqrt(2.0))
                T10 = T3 + sqrt(T3 * T3 + 6.0 * T2)
                if T2 < 0.0:
                    T4 = (T2 - T10) / T9
                    T10 = -log(1.0 - T10 + T4 * T4)
                else:
                    T11 = exp(-T10)
                    T4 = sqrt(T2 - 1.0 + T11 + T0 * T0) - T0
                    T10 = 1.0 - T11 + T4 * T4
            T6 = exp(-T10) - 1.0
            T7 = sqrt(T6 + T10)
            if T10 > 1.0e-15:
                e0 = -(T2 - T10) + T9 * T7
                e1 = 1.0 - T9 * 0.5 * T6 / T7
                T8 = T10 - (e0 / e1)
                T11 = exp(-T8) - 1.0
                T12 = sqrt(T11 + T8)
                qba = -T9 * T12 * Vtm
            else:
                if T10 < -1.0e-15:
                    e0 = -(T2 - T10) - T9 * T7
                    e1 = 1.0 + T9 * 0.5 * T6 / T7
                    T8 = T10 - e0 / e1
                    T12 = T9 * sqrt(exp(-T8) + T8 - 1.0)
                else:
                    T12 = 0.0
                    T8 = 0.0
                qba = T12 * Vtm
            qi_acc_for_QM = T9 * exp(-T8 / 2.0) * Vtm

        # Drain side and average potential / charge
        qia = 0.5 * (qis + qid)
        dqi = qis - qid

        T0 = pow(Vdseff, 2.0) / 6.25e-4
        if self.CHARGEWF != 0.0:
            qia2 = 0.5 * (qis + qid) + self.CHARGEWF * (1.0 - self.lexp(-T0)) * 0.5 * dqi
        else:
            qia2 = 0.5 * (qis + qid)

        # Multiplication factor for IV
        beta = u0_a * cox * Weff0 / Leff

        # Mobility degradation
        Eeffm = EeffFactor * (qba + eta_mu * qia2)
        T2 = pow(0.5 * (1.0 + abs(qia2 / qb0)), UCS_t)
        if self.BULKMOD != 0:
            T3 = (UA_a + UC_a * veseff) * pow(abs(Eeffm), EU_a) + UD_a / T2
        else:
            T3 = UA_a * pow(abs(Eeffm), EU_a) + UD_a / T2

        Dmob = 1.0 + T3
        Dmob = Dmob / self.U0MULT
        ueff = u0_a / Dmob

        # Calculate current and capacitance enhancement factors due to CLM and DIBL
        tmp = DROUT_i * Leff / scl + 1.0e-6
        if tmp < 40.0:
            DIBLfactor = 0.5 * PDIBL1_a / (cosh(tmp) - 1.0) + PDIBL2_a
        else:
            DIBLfactor = PDIBL1_a * exp(-tmp) + PDIBL2_a

        if PVAG_i > 0.0:
            PVAGfactor = 1.0 + PVAG_i * qia / EsatL
        else:
            PVAGfactor = 1.0 / (1.0 - PVAG_i * qia / EsatL)

        diffVds = vds - Vdseff
        Vgst2Vtm = qia + 2.0 * Vtm
        if DIBLfactor > 0.0:
            T1 = Vgst2Vtm
            T3 = T1 / (Vdsat + T1)
            VaDIBL = T1 / DIBLfactor * T3 * PVAGfactor
            Moc = 1.0 + diffVds / VaDIBL
        else:
            Moc = 1.0

        if PCLM_a > 0.0:
            if PCLMG_i < 0.0:
                T1 = 1.0 / (1.0 / PCLM_a - PCLMG_i * qia)
            else:
                T1 = PCLM_a + PCLMG_i * qia
            Mclm = 1.0 + T1 * self.lln(1.0 + (vds - Vdseff) / T1 / (Vdsat + EsatL))
        else:
            Mclm = 1.0

        Moc = Moc * Mclm

        # Current degradation Factor Due to Velocity Saturation
        Esat1 = 2.0 * VSAT1_a / ueff
        Esat1L = Esat1 * Leff
        T0 = self.lexp(PSAT_i * self.lln(dqi / Esat1L))
        Ta = (1.0 + self.lexp(1.0 / PSAT_i * self.lln(DELTAVSAT_i)))
        Dvsat = (1.0 + self.lexp(1.0 / PSAT_i * self.lln(DELTAVSAT_i + T0))) / Ta
        Dvsat = Dvsat + 0.5 * PTWG_a * qia * dqi * dqi

        # Non-saturation effect
        T0 = A1_t + A2_t / (qia + 2.0 * nVtm)
        T1 = T0 * dqi * dqi
        T2 = T1 + 1.0 - 0.001
        T3 = -1.0 + 0.5 * (T2 + sqrt(T2 * T2 + 0.004))
        Nsat = 0.5 * (1.0 + sqrt(1.0 + T3))
        Dvsat = Dvsat * Nsat

        # Lateral non-uniform doping effect (IV-CV Vth shift) factor
        if K0_t != 0.0:
            T1 = K0_t / (max(0, K0SI_t + K0SISAT_t * dqi * dqi) * qia + 2.0 * nVtm)
            Mnud = self.lexp(-T1)
        else:
            Mnud = 1.0

        # Body-effect factor for BULKMOD = 2
        if self.BULKMOD == 2:
            T0 = self.hypsmooth((K2_t + K2SAT_t * vdsx), 1.0e-6)
            T1 = T0 / (max(0, K2SI_t + K2SISAT_t * dqi * dqi) * qia + 2.0 * nVtm)
            T3 = sqrt(PHIBE_i - veseff) - sqrt(PHIBE_i)
            Mob = self.lexp(- T1 * T3)
        else:
            Mob = 1.0

        # Current and charge calculation
        # Quasi static I-V model
        etaiv = q0 / (q0 + qia)
        ids0_ov_dqi = qia + (2.0 - etaiv) * nVtm
        ids0 = ids0_ov_dqi * dqi

        # S/D series resistance
        if self.RDSMOD == 0:
            Rsource = RSourceGeo
            Rdrain = RDrainGeo
            T4 = 1.0 + PRWGS_i * qia
            T1 = 1.0 / T4
            T0 = 0.5 * (T1 + sqrt(T1 * T1 + 0.01))
            Rdsi = rdstemp * (RDSWMIN_i + RDSW_i * T0) * WeffWRFactor
            Dr = 1.0 + NFINtotal * beta * ids0_ov_dqi / (Dmob * Dvsat) * Rdsi
        elif self.RDSMOD == 1:
            Rdsi = 0.0
            Dr = 1.0
            T2 = vgs_noswap - vfbsd
            T3 = sqrt(T2 * T2 + 1.0e-1)
            vgs_eff = 0.5 * (T2 + T3)
            T4 = 1.0 + PRWGS_i * vgs_eff
            T1 = 1.0 / T4
            T0 = 0.5 * (T1 + sqrt(T1 * T1 + 0.01))
            # V(si, s) needs to be defined
            T5 = RSW_i * (1.0 + RSDR_a * self.lexp(0.5 * self.PRSDR * self.lln(V(si, s) * V(si, s) + 1.0e-6)))
            Rsource = rdstemp * (RSourceGeo + (RSWMIN_i + T5 * T0) * WeffWRFactor)
            T2 = vgd_noswap - vfbsd
            T3 = sqrt(T2 * T2 + 1.0e-1)
            vgd_eff = 0.5 * (T2 + T3)
            T4 = 1.0 + PRWGD_i * vgd_eff
            T1 = 1.0 / T4
            T0 = 0.5 * (T1 + sqrt(T1 * T1 + 0.01))
            # V(di, d) needs to be defined
            T5 = RDW_i * (1.0 + RDDR_a * self.lexp(0.5 * self.PRDDR * self.lln(V(di, d) * V(di, d) + 1.0e-6)))
            Rdrain = rdstemp * (RDrainGeo + (RDWMIN_i + T5 * T0) * WeffWRFactor)
        elif self.RDSMOD == 2:
            T4 = 1.0 + PRWGS_i * qia
            T1 = 1.0 / T4
            T0 = 0.5 * (T1 + sqrt(T1 * T1 + 0.01))
            Rdsi = rdstemp * (RSourceGeo + RDrainGeo + RDSWMIN_i + RDSW_i * T0) * WeffWRFactor
            Dr = 1.0 + NFINtotal * beta * ids0_ov_dqi / (Dmob * Dvsat) * Rdsi
            Rsource = 0.0
            Rdrain = 0.0

        ids = NFINtotal * beta * ids0 * Moc * Mnud * Mob / (Dmob * Dvsat * Dr)
        ids = ids * self.IDS0MULT

        # Impact ionization current (Ref: IIMOD = 1 from BSIM4 Model, IIMOD = 2 from BSIMSOI Model)
        Iii = 0.0
        if self.IIMOD == 1:
            T0 = (ALPHA0_t + ALPHA1_t * Leff) / Leff
            if T0 <= 0.0 or BETA0_t <= 0.0:
                Iii = 0.0
            else:
                T1 = -BETA0_t / (diffVds + 1.0e-30)
                Iii = T0 * diffVds * ids * self.lexp(T1)
        elif self.IIMOD == 2:
            ALPHAII = (ALPHAII0_t + ALPHAII1_t * Leff) / Leff
            if ALPHAII <= 0.0:
                Iii = 0.0
            else:
                T0 = ESATII_i * Leff
                T1 = SII0_t * T0 / (1.0 + T0)
                T0 = 1.0 / (1.0 + hypsmooth(SII1_i * vgsfbeff, self.IIMOD2CLAMP1))
                T3 = T0 + SII2_i
                T2 = self.hypsmooth(vgsfbeff * T3, self.IIMOD2CLAMP2)
                T3 = 1.0 / (1.0 + SIID_i * vds)
                VgsStep = T1 * T2 * T3
                Vdsatii = VgsStep * (1.0 - LII_i / Leff)
                Vdiff = vds - Vdsatii
                T0 = BETAII2_i + BETAII1_i * Vdiff + BETAII0_i * Vdiff * Vdiff
                T1 = sqrt(T0 * T0 + 1.0e-10)
                Ratio = -self.hypmax(-ALPHAII * lexp(Vdiff / T1), -10.0, self.IIMOD2CLAMP3)
                Iii = Ratio * ids

        # Gate current Ref: BSIM4
        igbinv = igbacc = igcs = igcd = igs = igd = 0.0

        # Igb
        if self.IGBMOD != 0:
            # Igbinv
            T1 = (qia - EIGBINV_i) / NIGBINV_i / Vtm
            Vaux_Igbinv = NIGBINV_i * Vtm * self.lln(1.0 + self.lexp(T1))
            T2 = AIGBINV_t - BIGBINV_i * qia
            T3 = 1.0 + CIGBINV_i * qia
            T4 = -9.82222e11 * self.TOXG * T2 * T3
            T5 = self.lexp(T4)
            T6 = 3.75956e-7
            igbinv = Weff0 * Leff * T6 * Toxratio * vge * Vaux_Igbinv * T5
            igbinv = igbinv * igtemp

            # Igbacc
            vfbzb = deltaPhi - (Eg / 2.0) - phib
            T0 = vfbzb - vge
            T1 = T0 / NIGBACC_i / Vtm
            Vaux_Igbacc = NIGBACC_i * Vtm * self.lln(1.0 + self.lexp(T1))
            if self.BULKMOD != 0:
                Voxacc = qi_acc_for_QM
            else:
                if vfbzb <= 0.0:
                    Voxacc = 0.5 * (T0 - 0.02 + sqrt((T0 - 0.02) * (T0 - 0.02) - 0.08 * vfbzb))
                else:
                    Voxacc = 0.5 * (T0 - 0.02 + sqrt((T0 - 0.02) * (T0 - 0.02) + 0.08 * vfbzb))

            T2 = AIGBACC_t - BIGBACC_i * Voxacc
            T3 = 1.0 + CIGBACC_i * Voxacc
            T4 = -7.45669e11 * self.TOXG * T2 * T3
            T5 = self.lexp(T4)
            T6 = 4.97232e-7
            igbacc = Weff0 * Leff * T6 * Toxratio * vge * Vaux_Igbacc * T5
            igbacc = igbacc * igtemp

        if self.IGCMOD != 0:
            # Igcinv
            T1 = AIGC_t - BIGC_i * qia
            T2 = 1.0 + CIGC_i * qia
            T3 = -Bechvb * self.TOXG * T1 * T2
            T4 = qia * self.lexp(T3)
            T5 = (vge + 0.5 * vdsx + 0.5 * (ves_jct + ved_jct))
            igc0 = Weff0 * Leff * Aechvb * Toxratio * T4 * T5 * igtemp

            # Gate-Current Partitioning
            Vdseffx = sqrt(Vdseff * Vdseff + 0.01) - 0.1
            T1 = PIGCD_i * Vdseffx
            T1_exp = self.lexp(-T1)
            T3 = T1 + T1_exp - 1.0 + 1.0e-4
            T4 = 1.0 - (T1 + 1.0) * T1_exp + 1.0e-4
            T5 = T1 * T1 + 2.0e-4
            igcd = igc0 * T4 / T5
            igcs = igc0 * T3 / T5

            # Igs
            T0 = vgs_noswap - vfbsd
            vgs_eff = sqrt(T0 * T0 + 1.0e-4)
            if self.IGCLAMP == 1:
                T1 = self.hypsmooth((AIGS_t - BIGS_i * vgs_eff), 1.0e-6)
                if CIGS_i < 0.01:
                    CIGS_i = 0.01
            else:
                T1 = AIGS_t - BIGS_i * vgs_eff
            T2 = 1.0 + CIGS_i * vgs_eff
            T3 = -Bechvb * self.TOXG * POXEDGE_i * T1 * T2
            T4 = self.lexp(T3)
            if sigvds > 0.0:
                igs = igsd_mult * self.DLCIGS * vgs_noswap * vgs_eff * T4
            else:
                igd = igsd_mult * self.DLCIGS * vgs_noswap * vgs_eff * T4

            # Igd
            T0 = vgd_noswap - vfbsd
            vgd_eff = sqrt(T0 * T0 + 1.0e-4)
            if self.IGCLAMP == 1:
                T1 = self.hypsmooth((AIGD_t - BIGD_i * vgd_eff), 1.0e-6)
                if CIGD_i < 0.01:
                    CIGD_i = 0.01
            else:
                T1 = AIGD_t - BIGD_i * vgd_eff
            T2 = 1.0 + CIGD_i * vgd_eff
            T3 = -Bechvb * self.TOXG * POXEDGE_i * T1 * T2
            T4 = self.lexp(T3)
            if sigvds > 0.0:
                igd = igsd_mult * self.DLCIGD * vgd_noswap * vgd_eff * T4
            else:
                igs = igsd_mult * self.DLCIGD * vgd_noswap * vgd_eff * T4

        # GIDL/GISL current Ref: BSIM4
        igisl = igidl = 0.0

        if self.GIDLMOD != 0:
            T0 = epsratio * self.EOT
            # GIDL
            if AGIDL_i <= 0.0 or BGIDL_t <= 0.0:
                T6 = 0.0
            else:
                T1 = (-vgd_noswap - EGIDL_i + vfbsd) / T0
                T1 = self.hypsmooth(T1, 1.0e-2)
                T2 = BGIDL_t / (T1 + 1.0e-3)
                T3 = self.lexp(PGIDL_i * self.lln(T1))
            if self.BULKMOD != 0:
                T4 = -ved_jct * ved_jct * ved_jct
                T4a = CGIDL_i + abs(T4) + 1.0e-5
                T5 = self.hypsmooth(T4 / T4a, 1.0e-6) - 1.0e-6
                T6 = AGIDL_i * Weff0 * T3 * self.lexp(-T2) * T5
            else:
                T6 = AGIDL_i * Weff0 * T3 * self.lexp(-T2) * vds_noswap

            if sigvds > 0.0:
                igidl = T6
            else:
                igisl = T6

            # GISL
            if AGISL_i <= 0.0 or BGISL_t <= 0.0:
                T6 = 0.0
            else:
                T1 = (-vgs_noswap - EGISL_i + vfbsd) / T0
                T1 = self.hypsmooth(T1, 1.0e-2)
                T2 = BGISL_t / (T1 + 1.0e-3)
                T3 = self.lexp(PGISL_i * self.lln(T1))
            if self.BULKMOD != 0:
                T4 = -ves_jct * ves_jct * ves_jct
                T4a = CGISL_i + abs(T4) + 1.0e-5
                T5 = self.hypsmooth(T4 / T4a, 1.0e-6) - 1.0e-6
                T6 = AGISL_i * Weff0 * T3 * self.lexp(-T2) * T5
            else:
                T6 = -vds_noswap * AGISL_i * Weff0 * T3 * self.lexp(-T2)

            if sigvds > 0.0:
              igisl = T6
            else:
              igidl = T6

        # Junction current
        if self.BULKMOD != 0:
            # Source-side junction current
            if Isbs > 0.0:
                if ves_jct < VjsmRev:
                    T0 = ves_jct / Nvtms
                    T1 = self.lexp(T0) - 1.0
                    T2 = IVjsmRev + SslpRev * (ves_jct - VjsmRev)
                    Ies = T1 * T2
                elif ves_jct <= VjsmFwd:
                    T0 = ves_jct / Nvtms
                    T1 = (self.BVS + ves_jct) / Nvtms
                    T2 = self.lexp(-T1)
                    Ies = Isbs * (self.lexp(T0) + XExpBVS - 1.0 - self.XJBVS * T2)
                else:
                    Ies = IVjsmFwd + SslpFwd * (ves_jct - VjsmFwd)
            else:
                Ies = 0.0
            # Source-side junction tunneling current
            if JTSS_t > 0.0:
                if self.VTSS - ves_jct < self.VTSS * 1.0e-3:
                    T0 = -ves_jct / Vtm0 / NJTS_t
                    T1 = self.lexp(T0 * 1.0e3) - 1.0
                    Ies = Ies - self.ASEJ * JTSS_t * T1
                else:
                    T0 = -ves_jct / Vtm0 / NJTS_t
                    T1 = self.lexp(T0 * self.VTSS / (self.VTSS - ves_jct)) - 1.0
                    Ies = Ies - self.ASEJ * JTSS_t * T1

            if JTSSWS_t > 0.0:
                if self.VTSSWS - ves_jct < self.VTSSWS * 1.0e-3:
                    T0 = -ves_jct / Vtm0 / NJTSSW_t
                    T1 = self.lexp(T0 * 1.0e3) - 1.0
                    Ies = Ies - self.PSEJ * JTSSWS_t * T1
                else:
                    T0 = -ves_jct / Vtm0 / NJTSSW_t
                    T1 = self.lexp(T0 * self.VTSSWS / (self.VTSSWS - ves_jct)) - 1.0
                    Ies = Ies - self.PSEJ * JTSSWS_t * T1

            if JTSSWGS_t > 0.0:
                if self.VTSSWGS - ves_jct < self.VTSSWGS * 1.0e-3:
                    T0 = -ves_jct / Vtm0 / NJTSSWG_t
                    T1 = self.lexp(T0 * 1.0e3) - 1.0
                    Ies = Ies - Weff0 * NFINtotal * JTSSWGS_t * T1
                else:
                    T0 = -ves_jct / Vtm0 / NJTSSWG_t
                    T1 = self.lexp(T0 * self.VTSSWGS / (self.VTSSWGS - ves_jct)) - 1.0
                    Ies = Ies - Weff0 * NFINtotal * JTSSWGS_t * T1

            # Drain-side junction current
            if Isbd > 0.0:
                if ved_jct < VjdmRev:
                    T0 = ved_jct / Nvtmd
                    T1 = self.lexp(T0) - 1.0
                    T2 = IVjdmRev + DslpRev * (ved_jct - VjdmRev)
                    Ied = T1 * T2
                elif ved_jct <= VjdmFwd:
                    T0 = ved_jct / Nvtmd
                    T1 = (BVD + ved_jct) / Nvtmd
                    T2 = self.lexp(-T1)
                    Ied = Isbd * (self.lexp(T0) + XExpBVD - 1.0 - XJBVD * T2)
                else:
                    Ied = IVjdmFwd + DslpFwd * (ved_jct - VjdmFwd)
            else:
                Ied = 0.0

            # Drain-side junction tunneling current
            if JTSD_t > 0.0:
                if self.VTSD - ved_jct < self.VTSD * 1.0e-3:
                    T0 = -ved_jct / Vtm0 / NJTSD_t
                    T1 = self.lexp(T0 * 1.0e3) - 1.0
                    Ied = Ied - self.ADEJ * JTSD_t * T1
                else:
                    T0 = -ved_jct / Vtm0 / NJTSD_t
                    T1 = self.lexp(T0 * self.VTSD / (self.VTSD - ved_jct)) - 1.0
                    Ied = Ied - self.ADEJ * JTSD_t * T1

            if JTSSWD_t > 0.0:
                if self.VTSSWD - ved_jct < self.VTSSWD * 1.0e-3:
                    T0 = -ved_jct / Vtm0 / NJTSSWD_t
                    T1 = self.lexp(T0 * 1.0e3) - 1.0
                    Ied = Ied - self.PDEJ * JTSSWD_t * T1
                else:
                    T0 = -ved_jct / Vtm0 / NJTSSWD_t
                    T1 = self.lexp(T0 * self.VTSSWD / (self.VTSSWD - ved_jct)) - 1.0
                    Ied = Ied - self.PDEJ * JTSSWD_t * T1

            if JTSSWGD_t > 0.0:
                if self.VTSSWGD - ved_jct < self.VTSSWGD * 1.0e-3:
                    T0 = -ved_jct / Vtm0 / NJTSSWGD_t
                    T1 = self.lexp(T0 * 1.0e3) - 1.0
                    Ied = Ied - Weff0 * NFINtotal * JTSSWGD_t * T1
                else:
                    T0 = -ved_jct / Vtm0 / NJTSSWGD_t
                    T1 = self.lexp(T0 * self.VTSSWGD / (self.VTSSWGD - ved_jct)) - 1.0
                    Ied = Ied - Weff0 * NFINtotal * JTSSWGD_t * T1

        # Generation-recombination component
        idsgen = self.HFIN * self.TFIN * (Leff - 2.0 * LINTIGEN_i) * igentemp * vds * (AIGEN_i + BIGEN_i * vds * vds)

        igidl = NFINtotal * igidl
        igisl = NFINtotal * igisl
        igcd = NFINtotal * igcd
        igcs = NFINtotal * igcs
        igs = NFINtotal * igs
        igd = NFINtotal * igd
        igbinv = NFINtotal * igbinv
        igbacc = NFINtotal * igbacc
        idsgen = NFINtotal * idsgen

        # Gate to body tunneling current empirical partition for BULKMOD = 0
        igbs = igbd = 0.0
        if self.BULKMOD == 0:
            igbs = (igbinv + igbacc) * wf
            igbd = (igbinv + igbacc) * wr

        # Total drain/source currents
        if self.BULKMOD != 0:
            if sigvds > 0.0:
                id_tot = devsign * (ids + idsgen - igd - igcd + Iii + igidl - Ied)
                is_tot = -devsign * (ids + idsgen + igs + igcs - igisl + Ies)
            else:
                id_tot = -devsign * (ids + idsgen + igs + igcs - igisl + Ied)
                is_tot = devsign * (ids + idsgen - igd - igcd + Iii + igidl - Ies)
        else:
            if sigvds > 0.0:
                id_tot = devsign * (ids + idsgen - igd - igcd - igbd + Iii + igidl - igisl)
                is_tot = -devsign * (ids + idsgen + igs + igcs + igbs - igisl + igidl)
            else:
                id_tot = -devsign * (ids + idsgen + igs + igcs + igbd - igisl + igidl)
                is_tot = devsign * (ids + idsgen - igd - igcd - igbs + Iii + igidl - igisl)

        # Total gate current
        if self.BULKMOD == 0:
            ig_tot = devsign * (igs + igd + igcs + igcd + igbs + igbd)
        else:
            ig_tot = devsign * (igs + igd + igcs + igcd + igbacc + igbinv)

        # Total substrate current
        if self.BULKMOD != 0:
            ib_tot = -devsign * (Iii - Ies - Ied + igbinv + igbacc + igisl + igidl)
        else:
            ib_tot = 0.0

        return [id_tot, ig_tot, is_tot, ib_tot]

def read_mdl(file):
    mdl = {}
    with open(file,'r') as f:
        lines = f.read().splitlines()
    for line in lines:
        param, value = re.split('[=\s]+', line)
        mdl[param] = float(value)
    return mdl

filepath = "modelcard.l"
param = read_mdl(filepath)

Id, Ig, Is, Ib = BSIMCMG(**param).calc()

print(f'Id = {Id:>16.9e} A')
print(f'Ig = {Ig:>16.9e} A')
print(f'Is = {Is:>16.9e} A')
print(f'Ib = {Ib:>16.9e} A')