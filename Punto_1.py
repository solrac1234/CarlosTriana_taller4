import numpy as np
import matplotlib.pyplot as plt
from sys import argv

def fourier_2d(x):
	# Transformada de Fourier
    Xr = np.zeros(np.shape(x))
    Xi = np.zeros(np.shape(x))
    
    S = np.shape(x)
    D0 = S[0]
    D1 = S[1]
    
    m,n = np.meshgrid(np.arange(D1),np.arange(D0))
    
    for k in range(D0):
        for l in range(D1):
            Xr[k,l] = np.sum( x[:,:]*np.cos(-1*2*np.pi*(n*k/D0+m*l/D1)) , (0,1) )
            Xi[k,l] = np.sum( x[:,:]*np.sin(-1*2*np.pi*(n*k/D0+m*l/D1)) , (0,1) )
    return Xr + 1j*Xi # devolver parte real + parte imaginaria

def i_fourier_2d(Xr,Xi):
	# Transformada inversa de Fourier
    xr = np.zeros(np.shape(Xr))
    
    S = np.shape(xr)
    D0 = S[0]
    D1 = S[1]
    
    m,n = np.meshgrid(np.arange(D1),np.arange(D0))
    
    for k in range(D0):
        for l in range(D1):
            xr[k,l] = np.sum( Xr[:,:]*np.cos(2*np.pi*(n*k/D0+m*l/D1)) , (0,1) )
            xr[k,l] = xr[k,l] - np.sum( Xi[:,:]*np.sin(2*np.pi*(n*k/D0+m*l/D1)) , (0,1) )
	# Devolver solo parte real            
    return xr

def shift_fft(X):
	# Girar datos como se indicaba en referencia del taller
    D0,D1 = np.shape(X)
    Y = np.roll(X,int(D0/2),0)
    X = np.roll(Y,int(D1/2),1)
    return X

# Cargar imagen en numpy
I = plt.imread(argv[1]) # Cargar la imagen que se especifica cuando se ejecuta
I = I[50:100,:200] # La imagen es muy grande. Recorto una parte pequena para no demorarme
FI2 = fourier_2d(I)


# kernel
nkernel = float(argv[2])

x = np.linspace(-nkernel,nkernel,int(0.8*2*nkernel))
n = len(x)
x1 = np.reshape(x,(n,1))
x2 = np.reshape(x,(1,n))
k = np.exp(-nkernel/2.35*x1**2)*np.exp(-nkernel/4*x2**2)

# Expandir kernel
m0,n0 = np.shape(k)
K = np.zeros(np.shape(I))
K[:m0,:n0] = k

# transformada del kernel
K_ft = fourier_2d(K) 

# Aplicar kernel
gauss_f = K_ft*FI2

# transformada inversa
gauss_I = i_fourier_2d(gauss_f.real, gauss_f.imag)

#plt.imshow(I,cmap='gray')
plt.figure(); plt.imshow(gauss_I.real, cmap='gray')
plt.savefig('suave.png')
