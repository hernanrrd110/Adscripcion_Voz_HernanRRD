clear all;
% ............ Lectura de archivo .............

% Cuadro de diálogo para abrir archivos, guarda nombre de archivo y dirección
[filename,pathname,~] = uigetfile();
 
% Concatena dirección y nombre de archivo
file_datos = strcat(pathname,filename);
load(file_datos);

% Reemplazo de variable isi (en milisegundos) por ts
ts = isi/1000; clear isi;clear isi_units;

%% .......... Armado de datos

close all; clc;
fprintf('* ................. Archivo seleccionado ................. *\n')
fprintf('%s\n',file_datos)

% Quitamos la media
data_voz = data(:,1) - mean(data(:,1));
data_egg = data(:,2) - mean(data(:,2));
data_vpc = data(:,3) - mean(data(:,3));
data_dB = data(:,4) - mean(data(:,4));

% Dividimos por desvio estandar

data_voz = data_voz/std(data_voz );
data_egg = data_egg/std(data_egg);
data_vpc = data_vpc/std(data_vpc);
data_dB = data_dB/std(data_dB);

fs = round(1/ts);
N = length(data);

% Declaracion de variables del eje x
vector_temp = linspace(0,N-1,N)*ts;
vector_frec = linspace(0,fs/2,floor(N/2));

% Calculo de modulos de FFTs
Modulo_voz = abs(fft(data_voz))/N; 
Modulo_voz = Modulo_voz (1:floor(N/2));

Modulo_egg = abs(fft(data_egg))/N;
Modulo_egg = Modulo_egg (1:floor(N/2));

Modulo_vpc = abs(fft(data_vpc))/N;
Modulo_vpc = Modulo_vpc (1:floor(N/2));

Modulo_dB = abs(fft(data_dB))/N;
Modulo_dB = Modulo_dB (1:floor(N/2));

% ..................... Graficas de Seniales ...................

figure('NumberTitle','off','Name','Señales');

subplot(2,2,1)
plot(vector_temp, data_voz);
title('Senial Voz')
xlabel('Tiempo [s]')
ylabel('Amplitud')

subplot(2,2,2)
plot(vector_temp, data_egg);
title('Senial EGG')
xlabel('Tiempo [s]')
ylabel('Amplitud')

subplot(2,2,3)
plot(vector_temp, data_vpc);
title('Senial VPC')
xlabel('Tiempo [s]')
ylabel('Amplitud')

subplot(2,2,4)
plot(vector_temp, data_dB);
title('Senial dB')
xlabel('Tiempo [s]')
ylabel('Amplitud')

%  ..................... Graficas de FTTs ..................... 

extremo_x = 100;

figure('NumberTitle','off','Name','FFTs');

subplot(2,2,1)
plot(vector_frec, Modulo_voz);
title('FFT Voz')
xlabel('Frecuencia [Hz]')
ylabel('Amplitud')
% xlim([0 extremo_x])

subplot(2,2,2)
plot(vector_frec, Modulo_egg);
title('FFT EGG')
xlabel('Frecuencia [Hz]')
ylabel('Amplitud')
% xlim([0 extremo_x])

subplot(2,2,3)
plot(vector_frec, Modulo_vpc);
title('FFT VPC')
xlabel('Frecuencia [Hz]')
ylabel('Amplitud')
% xlim([0 extremo_x])

subplot(2,2,4)
plot(vector_frec, Modulo_dB);
title('FFT dB')
xlabel('Frecuencia [Hz]')
ylabel('Amplitud')
% xlim([0 extremo_x])


%% ............ Guardado de audio 

% Pide una direccion donde guardar el archivo de audio. Luego guarda el
% archivo de audio con el nombre que tenia el archivo .mat

folder_name = uigetdir;
audio_guardado = strcat(folder_name,'\',filename);
audio_guardado = replace(audio_guardado,'.mat','.wav')
% audiowrite(audio_guardado, data(:,1) , fs)


