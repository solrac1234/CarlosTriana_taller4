Todo: transformada.txt altas.png suave.png

transformada.txt: fourier datos.txt
	./fourier datos.txt | tail -n +2  > transformada.txt
	cat transformada.txt

fourier: Punto_3.cpp
	c++ Punto_3.cpp -o fourier

altas.png: Punto_2.py
	python Punto_2.py old.png altas
	python Punto_2.py old.png bajas

suave.png: Punto_1.py
	python Punto_1.py old.png 17
