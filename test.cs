<CsoundSynthesizer>
<CsOptions>
-odac
-o out.wav _W
</CsOptions>
<CsInstruments>
sr=44100
ksmps=10
nchnls=1
instr 1
iamp=p4
ifreq=cpspch(p5)
iatt=p6
idec=p7
islev=p8
irel=p9
kenv adsr p3/iatt, p3/idec, islev, p3/irel
aout oscil iamp*kenv, ifreq, 1
out aout
endin
</CsInstruments>
<CsScore>
f1 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111
i 1 1.50 1.50 10000.00 5.09 1.00 6.00 1.00 1.50
i 1 3.00 1.50 10000.00 6.09 1.00 6.00 1.00 1.50
i 1 4.50 1.50 10000.00 5.09 1.00 6.00 1.00 1.50
i 1 6.00 1.50 10000.00 6.09 1.00 6.00 1.00 1.50
i 1 7.50 1.50 10000.00 7.04 2.00 5.00 1.00 1.00
i 1 7.50 1.50 10000.00 7.00 2.00 5.00 1.00 1.00
i 1 7.50 1.50 10000.00 7.07 2.00 5.00 1.00 1.00
i 1 8.00 0.50 10000.00 7.04 1.00 1.00 1.00 1.00
i 1 8.50 0.50 10000.00 7.00 1.00 1.00 1.00 1.00
i 1 9.00 0.50 10000.00 7.07 1.00 1.00 1.00 1.00
i 1 9.50 0.50 10000.00 8.04 1.00 1.00 1.00 1.00
i 1 10.00 0.50 10000.00 8.00 1.00 1.00 1.00 1.00
i 1 10.50 0.50 10000.00 8.07 1.00 1.00 1.00 1.00
i 1 11.00 0.50 10000.00 9.04 1.00 1.00 1.00 1.00
i 1 11.50 0.50 10000.00 9.00 1.00 1.00 1.00 1.00
i 1 12.00 0.50 10000.00 9.07 1.00 1.00 1.00 1.00
i 1 12.50 0.50 10000.00 10.04 1.00 1.00 1.00 1.00
i 1 13.00 0.50 10000.00 10.00 1.00 1.00 1.00 1.00
i 1 13.50 0.50 10000.00 10.07 1.00 1.00 1.00 1.00
i 1 14.00 0.50 10000.00 11.04 1.00 1.00 1.00 1.00
i 1 14.50 0.50 10000.00 11.00 1.00 1.00 1.00 1.00
i 1 15.00 0.50 10000.00 11.07 1.00 1.00 1.00 1.00
i 1 15.50 0.50 10000.00 12.04 1.00 1.00 1.00 1.00
i 1 16.00 0.50 10000.00 12.00 1.00 1.00 1.00 1.00
i 1 16.50 0.50 10000.00 12.07 1.00 1.00 1.00 1.00
i 1 17.00 0.50 10000.00 13.04 1.00 1.00 1.00 1.00
i 1 17.50 0.50 10000.00 13.00 1.00 1.00 1.00 1.00
i 1 18.00 0.50 10000.00 13.07 1.00 1.00 1.00 1.00
i 1 18.50 0.50 10000.00 14.04 1.00 1.00 1.00 1.00
i 1 19.00 0.50 10000.00 14.00 1.00 1.00 1.00 1.00
i 1 19.50 0.50 10000.00 14.07 1.00 1.00 1.00 1.00
i 1 20.00 0.50 10000.00 7.04 1.00 1.00 1.00 1.00
i 1 20.50 0.50 10000.00 7.00 1.00 1.00 1.00 1.00
i 1 21.00 0.50 10000.00 7.07 1.00 1.00 1.00 1.00
i 1 21.50 0.50 10000.00 6.04 1.00 1.00 1.00 1.00
i 1 22.00 0.50 10000.00 6.00 1.00 1.00 1.00 1.00
i 1 22.50 0.50 10000.00 6.07 1.00 1.00 1.00 1.00
i 1 23.00 0.50 10000.00 5.04 1.00 1.00 1.00 1.00
i 1 23.50 0.50 10000.00 5.00 1.00 1.00 1.00 1.00
i 1 24.00 0.50 10000.00 5.07 1.00 1.00 1.00 1.00
i 1 24.50 0.50 10000.00 4.04 1.00 1.00 1.00 1.00
i 1 25.00 0.50 10000.00 4.00 1.00 1.00 1.00 1.00
i 1 25.50 0.50 10000.00 4.07 1.00 1.00 1.00 1.00
i 1 26.00 0.50 10000.00 3.04 1.00 1.00 1.00 1.00
i 1 26.50 0.50 10000.00 3.00 1.00 1.00 1.00 1.00
i 1 27.00 0.50 10000.00 3.07 1.00 1.00 1.00 1.00
i 1 27.50 0.50 10000.00 2.04 1.00 1.00 1.00 1.00
i 1 28.00 0.50 10000.00 2.00 1.00 1.00 1.00 1.00
i 1 28.50 0.50 10000.00 2.07 1.00 1.00 1.00 1.00
i 1 29.00 0.50 10000.00 1.04 1.00 1.00 1.00 1.00
i 1 29.50 0.50 10000.00 1.00 1.00 1.00 1.00 1.00
i 1 30.00 0.50 10000.00 1.07 1.00 1.00 1.00 1.00
i 1 30.50 0.50 10000.00 0.04 1.00 1.00 1.00 1.00
i 1 31.00 0.50 10000.00 0.00 1.00 1.00 1.00 1.00
i 1 31.50 0.50 10000.00 0.07 1.00 1.00 1.00 1.00
</CsScore>
</CsoundSynthesizer>
