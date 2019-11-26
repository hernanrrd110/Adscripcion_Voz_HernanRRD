#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
===============================================================================
===============================================================================
         BASE DE DATOS DE REGISTROS ASOCIADOS A LA ACTIVIDAD VOCAL
           LABORATORIO DE SEÑALES Y DINÁMICAS NO LINEALES - IBB
                              CONICET - UNER
===============================================================================
         SCRIPT PARA REVISAR LOS REGISTROS AL FINAL DE UNA JORNADA
===============================================================================
'Juan Felipe Restrepo <jrestrepo@ingenieria.uner.edu.ar>'
2019-10-09
-------------------------------------------------------------------------------
'''
import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.io import loadmat
from scipy.fftpack import fft
from scipy.signal import decimate
import sounddevice as sd
import pandas as pd
# from simpleaudio import play_buffer

sep = '/'
if os.name == 'nt':
    sep = '\\'
registros = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']


def rev_registros(file_list):
    # Revisar que esten todos los archivos
    print(file_list)
    # n = 0
    # archivos_faltantes = []
    # for reg in registros:
        # archivo = '{0}/{1}_{2}.mat'.format(path, sujeto, reg)
        # if os.path.isfile(archivo):
            # n += 1
        # else:
            # archivos_faltantes.append(archivo)
    # if n == len(registros):
        # return 'Los registros están completos'
    # else:
        # return ['Falta el registo: ' + f + '\n' for f in archivos_faltantes]


def series_fft(file_,  f1=45, f2=55):
    # cargar señales
    data = loadmat(file_)
    # Decimar
    ts = 5 * data['isi'] / 1000
    fs = 1 / ts
    data['data'] = decimate(data['data'], 5, axis=0)
    time_ = pd.DataFrame(data['data'], columns=('voz', 'egg', 'vpc', 'db'))

    N = time_['voz'].shape[0]
    f = np.linspace(0, 1 / 2, int(N / 2)) * fs
    f = np.reshape(f, (int(N / 2),))

    fft_ = pd.DataFrame({'f': f})
    snr_ = {'voz': 0, 'egg': 0, 'vpc': 0, 'db': 0}

    for label in time_.columns:
        serie = time_[label]
        serie = (serie - np.mean(serie)) / np.std(serie)
        # FFT
        modulo = abs(fft(serie)) / N
        fft_[label] = modulo[0: int(N / 2)]
        # Calcular snr
        indf = np.where((f >= f1) * (f <= f2))[0]
        snr_[label] = - 10 * np.log10(2 * np.sum(modulo[indf]**2))
    return time_, fft_, snr_


    # revisar_registros(serie, ts, 1, 'registro a')

    # fs = 1 / ts
    # fig1, axis1 = plt.subplots(2, 2, num=i, sharex=True)
    # fig2, axis2 = plt.subplots(2, 2, num=i + 20, sharex=True)
    # for i, tipo, ax1, ax2 in zip(range(0, len(tipos)), tipos, axis1.flat,
                                 # axis2.flat):
        # # FFT
        # s = serie[:, i]
        # s = (s - np.mean(s)) / np.std(s)
        # N = s.shape[0]
        # print(N)
        # f = np.linspace(0, 1 / 2, int(N / 2)) * fs
        # f = np.reshape(f, (int(N / 2),))
        # Modulo = abs(fft(s)) / N
        # # Calcular snr
        # indf = np.where((f >= f1) * (f <= f2))[0]

        # snr = - 10 * np.log10(2 * np.sum(Modulo[indf]**2))
        # print('registro {0} SNR {1}= {2:.2f}'.format(titulo, tipo, snr))

        # # Graficar serie temporal
        # ax1.plot(s)
        # ax1.set_title(titulo)
        # ax1.set_title(titulo + ' ' + tipo)
        # if i > 2:
            # ax1.set_xlabel('n')
        # # Graficar espectro
        # ax2.plot(f, Modulo[0:round(N / 2)])
        # ax2.set_title(titulo + ' ' + tipo + ' FFT')
        # if i > 2:
            # ax2.set_xlabel('f [Hz]')
        # ax2.set_xlim(-10, 500)
    # sd.play(serie[:, 0], fs)


if __name__ == '__main__':
    pass
    # path = '/home/jrestrepo/Documents/Registros_adscripcion_2019/' + \
           # 'grabaciones_06_09_19/Sujeto01'
    # check_files(path)
    # sujeto = path.split(sep)[-1][-2:]
    # reg = registros[3]
    # # for i, reg in enumerate(registros):
    # archivo = '{0}/{1}_{2}.mat'.format(path, sujeto, reg)
    # data = loadmat(archivo)
    # ts = 5 * data['isi'] / 1000
    # serie = data['data']
    # serie = decimate(serie, 5, axis=0)
    # revisar_registros(serie, ts, 1, 'registro a')


# plt.show()
