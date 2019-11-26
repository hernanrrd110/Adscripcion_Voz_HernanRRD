%{
===========================================================================
===========================================================================
         BASE DE DATOS DE REGISTROS ASOCIADOS A LA ACTIVIDAD VOCAL
           LABORATORIO DE SEÑALES Y DINÁMICAS NO LINEALES - IBB
                              CONICET - UNER
===========================================================================
         SCRIPT PARA REVISAR LOS REGISTROS AL FINAL DE UNA JORNADA
===========================================================================
'Juan Felipe Restrepo <jrestrepo@ingenieria.uner.edu.ar>'
2019-10-09
---------------------------------------------------------------------------
revisar_registros()




===========================================================================
===========================================================================
%}
clear;
clc;


% Leer archivos en carpeta del sujeto

[filename,pathname,~] = uigetfile();

