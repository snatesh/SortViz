from random import random, randint
import matplotlib.pyplot as plt
import pylab
from matplotlib.animation import FuncAnimation
import math
from pyaudio import PyAudio

def sin_tone(freq,dur,vol=1,sample_rate=22050):
	n_samples = int(sample_rate * duration)
	restframes = n_samples % sample_rate
	
	p = PyAudio()
	stream = p.open(format=p.get_format_from_width(1), # 8bit
	                channels=1, # mono
	                rate=sample_rate,
	                output=True)
	s = lambda t: vol * math.sin(2 * math.pi * freq * t / sample_rate)
	samples = (int(s(t) * 0x7f + 0x80) for t in range(n_samples)) 
	stream.write(bytes(bytearray(samples)))
	
	# fill remainder of frameset with silence
	stream.write(b'\x80' * restframes)
	
	stream.stop_stream()
	stream.close()
	p.terminate()

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
num_elm = 50
factor = 2
ax.set_xlim(0,num_elm)
ax.set_ylim(0,factor*num_elm)
indices = [j for j in range(0,num_elm)]

# see http://www.phy.mtu.edu/~suits/notefreqs.html
#frequency=500 # Hz, waves per second A4
duration=.07 # seconds to play sound
volume=.5 # 0..1 how loud it is
# see http://en.wikipedia.org/wiki/Bit_rate#Audio
sample_rate=22050 # number of samples per second
lo_freq = 200
hi_freq = 5000
#sin_tone(frequency,duration,volume,sample_rate)

def rescale(x,a,b):
	I = abs(max(x) - min(x))
	x_scale = [a + (x[j]/I)*(b-a) for j in range(len(x))]
	print(x_scale[20])
	return x_scale

def quicksort(A,indices,p,r):
	if p < r:
		q = partition(A,indices,p,r)
		quicksort(A,indices,p,q-1)
		quicksort(A,indices,q+1,r)

def partition(A,indices,p,r):
	plt.show()
	piv = randint(p,r)
	swap(A, r, piv)
	if r != piv:
		frequency = rescale(A,lo_freq,hi_freq)
		sin_tone(frequency[r],duration,volume,sample_rate)
		ax.scatter(indices,A,40,A,'o','viridis')
		fig.canvas.draw()
		fig.canvas.flush_events()
		ax.clear()
	x = A[r]
	i = p-1
	for j in range(p,r):
		if A[j] <= x:
			i = i+1
			if A[i] != A[j]:
				swap(A,i,j)
				if i != j:
					frequency = rescale(A,lo_freq,hi_freq)
					sin_tone(frequency[i],duration,volume,sample_rate)
					ax.scatter(indices,A,40,A,'o','viridis')
					fig.canvas.draw()
					fig.canvas.flush_events()
					ax.clear()
	swap(A,i+1,r)
	if i+1 != r:
		frequency = rescale(A,lo_freq,hi_freq)
		sin_tone(frequency[i+1],duration,volume,sample_rate)
		ax.scatter(indices,A,40,A,'o','viridis')
		fig.canvas.draw()
		fig.canvas.flush_events()
		ax.clear()
	return i+1	

def swap(A,p,r):
	tmp = A[p]
	A[p] = A[r]
	A[r] = tmp

A = [0 for j in range(0,num_elm)]
for j in range(0,num_elm):
	A[j] =  randint(0,factor*num_elm)

#A.sort(reverse=True)
quicksort(A,indices,0,len(A)-1)
ax.scatter(indices,A,40,A,'o','viridis')
plt.show()
