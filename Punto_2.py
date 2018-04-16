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


# smooth Filter 
# Pasa bajas
# El filtro es una matriz
# La idea es generar unos en el centro de la matriz
# hacia afuera decae hasta cero como mostraba la pagina de referencia en el taller
# En la periferia son ceros
#
# El pasa altas es al contrario, por eso solo hago 1-bajas
#
D1 = np.size(FI2,1)
D0 = np.size(FI2,0)

m,n = np.meshgrid(np.arange(D1)-D1/2, np.arange(D0)-D0/2)

f = (m**2 + n**2)**0.5
F = np.zeros(np.shape(FI2))
cutOff = 20
w = 5
F[f<cutOff-w] = 1
ii = np.logical_and(f>cutOff-w, f<cutOff+w)
F[ii] = 0.5*(1-np.sin(np.pi*(f[ii]-cutOff)/(2*w)))

F_low = F
F_high = 1.0 - F


altas = argv[2]=='altas'
bajas = argv[2]=='bajas'

# Dependiendo de lo que entra en la terminal, 
# Procesar pasa bajas o pasa altas
if altas:
	# Aplicar los filtros y las rotaciones
	# correspondientes para altas y bajas
	FI2_high = shift_fft(shift_fft(FI2)*F_high)
	IF_high = i_fourier_2d(FI2_high.real, FI2_high.imag)
	

	# Guardar imagenes
	plt.figure()
	plt.imshow(IF_high,cmap='gray')
	plt.savefig('altas.png')
if bajas:
	# Aplicar los filtros y las rotaciones
	# correspondientes para altas y bajas
	FI2_low = shift_fft(shift_fft(FI2)*F_low)
	IF_low = i_fourier_2d(FI2_low.real, FI2_low.imag)
	
	# Guardar imagenes
	plt.figure()
	plt.imshow(IF_low,cmap='gray')
	plt.savefig('bajas.png')

