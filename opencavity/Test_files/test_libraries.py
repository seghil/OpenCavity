# -*- coding: utf-8 -*-
'''
Created on 26 mars 2014

@author: Mohamed
'''
import ctypes
import os 

chemin=os.getcwd()+"\libpropagator_c.dll"
mydll = ctypes.cdll.LoadLibrary(chemin)
a=ctypes.c_int() #pointeur sur un c_int
a.value=4
mydll.greet(a)

taille=5;
tab= ctypes.c_double*taille #(ctypes.c_int*taille)()  �quivalente aux 2 lignes
U1_real=tab()            #pointeur sur la table (tab c'est le type seulement)

tab2= ctypes.c_double*taille #(ctypes.c_int*taille)()  �quivalente aux 2 lignes
U1_imag=tab2() 

for i in range(taille):
    U1_real[i]=i
    U1_imag[i]=i

tab3= ctypes.c_double*taille #(ctypes.c_int*taille)()  �quivalente aux 2 lignes
U2_real=tab3()            #pointeur sur la table (tab c'est le type seulement)

tab4= ctypes.c_double*taille #(ctypes.c_int*taille)()  �quivalente aux 2 lignes
U2_imag=tab4()   


