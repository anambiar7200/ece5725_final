import numpy as np
import matplotlib.pyplot as plt
#import scipy.misc
#from scipy import io
import scipy.io.wavfile

rate, ster_data = scipy.io.wavfile.read("/wavs/sample1.wav")
#aud_data = ster_data[:,0]

#aud_data = ster_data[:,1]
aud_data = (ster_data[:,1] + ster_data[:,0])/2

# From here down, everything else can be the same
len_data = len(aud_data)

channel_1 = np.zeros(2**(int(np.ceil(np.log2(len_data)))))
channel_1[0:len_data] = aud_data

fourier = np.fft.fft(channel_1)
w = np.linspace(0, 44000, len(fourier))

# First half is the real component, second half is imaginary
fourier_to_plot = fourier[0:len(fourier)//2]
w = w[0:len(fourier)//2]

plt.figure(1)

plt.plot(w, fourier_to_plot)
plt.xlabel('frequency')
plt.ylabel('amplitude')
plt.show()