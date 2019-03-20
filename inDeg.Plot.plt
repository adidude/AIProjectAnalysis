#
# Descriptiom of the plot. G(5881, 35592). 552 (0.0939) nodes with in-deg > avg deg (12.1), 260 (0.0442) with >2*avg.deg (Tue Mar 12 15:52:50 2019)
#

set title "Descriptiom of the plot. G(5881, 35592). 552 (0.0939) nodes with in-deg > avg deg (12.1), 260 (0.0442) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "In-degree"
set ylabel "Count"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'inDeg.Plot.png'
plot 	"inDeg.Plot.tab" using 1:2 title "" with linespoints pt 6
