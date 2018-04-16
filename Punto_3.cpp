#include "iostream"
#include "fstream"
#include "math.h"

using namespace std;

void do_a_linspace(double *x, int N, double *x_new)
{
	int i;
	//Double x_new[N];

	x_new[0] = x[0]; 

	x_new[N-1] = x[N-1];

	double step = (x[N-1]-x[0])/((double)N-1);

	for (i = 1; i < N-1; ++i)
	{
		x_new[i] = x_new[0] + i*step;
	}

	//return x_new;
}

double polinomio_lj(double *Xoriginal, double x, int N, int j)
{
	// Calcula los polinomios li para x
	// Hace la multiplicatoria y devulve el valor lj
	int i;

	double l;

	l = 1.0;

	for (i = 0; i < N; ++i)
	{
		if (i!=j) // Solo si j es diferente de i entra en la multiplicatoria
		{
			l = l*(x-Xoriginal[i])/(Xoriginal[j]-Xoriginal[i]);
		}
	}

	return l;
}

double real_DFT(double *x, int k, int N)
{
	double Xk_real=0.0;

	for (int n = 0; n < N; ++n)
	{

		Xk_real = Xk_real + x[n]*cos(2*3.14*k*n/N);

	}
	return Xk_real;
}

double img_DFT(double *x, int k, int N)
{
	double Xk_real=0.0;

	for (int n = 0; n < N; ++n)
	{

		Xk_real = Xk_real + x[n]*sin(2*3.14*k*n/N);

	}
	return Xk_real;
}



int main(int argc, char const *argv[])
{
	cout << "Leyendo archivo " << argv[1] << "\n";
	//ifstream in(argv[1]);

	ifstream in(argv[1]);

	int test;

	double f, fnyq;

	int i, j, k; // Contadores en for

	// Cargar datos
	int n0 = 20, n=0; // Maximo 20 datos porque polinomio es inestable

	double x[n0], y[n0];

	for (i = 0; i < n0; ++i)
	{
		in >> x[i] >> y[i];

		if (test != EOF)
		{
			n = n + 1;	
		}
		else
		{
			 x[i] = 0.0;

			 y[i] = 0.0;
		}
		//cout << "%f-%f\n", x[i],y[i]);
	}


	if (n<n0) // Realocar memoria
	{
		double x[n];

		double y[n];
	}
	
	// x linealmente espaciado
	double x_new[n];

	do_a_linspace(x, n, x_new);


	// Interpolar con Lagrange
	double L[n];

	
	for (i = 0; i < n; ++i)
	{
		L[i] = 0.0;

		for (j = 0; j < n; ++j)
		{

			L[i] = L[i] + y[j]*polinomio_lj(x, x_new[i], n, j);
		}
		// Imprimir datos para verificarlos
		//cout << x[i] << y[i] << x_new[i] << L[i]) << "\n";
	}

	fnyq = 0.5*1.0/(x_new[2]-x_new[1]);

	for (k = 0; k < n;++k)
	{
		if (k<(int)n/2+1)
		{

			f = (double)(k)/(double)(n/2)*fnyq;
		}
		else
		{

			f = -fnyq + (double)(k-n/2)/(double)(n/2)*fnyq;	
		}

		cout << f << " " << real_DFT(x_new, k, n) << " " << img_DFT(x_new, k, n) << "\n";
	}



	return 0;
}
