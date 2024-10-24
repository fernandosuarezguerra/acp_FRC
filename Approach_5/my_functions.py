#!/usr/bin/env python 
import numpy as np
import os
import time

######################################  
######################################  
def extractTwoColumns(filePath, index1, index2):
    """ Returns two lists: x for the data stored in index1 column of the file and y for 
    the data stored in index2 column of the file."""
    data = open(filePath, 'r')
    x = []
    y = []
    for line in data:
        a = line.split()
        x.append(a[index1])
        y.append(a[index2])
    data.close()
    return np.array(x).astype(float), np.array(y).astype(float)
######################################  
######################################  
def extractOneColumn(filePath, index):
    """ Returns one lists x for the data stored in index column of the file """
    data = open(filePath, 'r')
    x = []
    for line in data:
        a = line.split()
        x.append(a[index])
    data.close()
    return np.array(x).astype(float)
######################################  
######################################  
def interpolate_value(x,coords_x, coords_y):
    """ Returns the interpolated value for x in the diagram defined coords_x and coords_y  """
    for i in range(len(coords_x)-1):
        x1=coords_x[i]
        y1=coords_y[i]
        x2=coords_x[i+1]
        y2=coords_y[i+1]
        if x>=x1 and x<=x2:
            return y1+(x-x1)*(y2-y1)/(x2-x1)

######################################  
######################################  
def get_average(y1, y2, y3):
    mylist = [y1,y2,y3]
    mynewlist=[]
    for each in mylist:
        if np.isnan(each):
            pass
        else:
            mynewlist.append(each)
    if len(mynewlist)==0:
        return np.nan
    else:
        return sum(mynewlist) / len(mynewlist)
######################################  
######################################  

def get_max(y1, y2, y3):
    mylist = [y1,y2,y3]
    mynewlist=[]
    for each in mylist:
        if np.isnan(each):
            pass
        else:
            mynewlist.append(each)
    if len(mynewlist)==0:
        return np.nan
    else:
        return max(mynewlist)
######################################  
######################################  
def get_min(y1, y2, y3):
    mylist = [y1,y2,y3]
    mynewlist=[]
    for each in mylist:
        if np.isnan(each):
            pass
        else:
            mynewlist.append(each)
    if len(mynewlist)==0:
        return np.nan
    else:
        return min(mynewlist)
######################################  
######################################  
def compute_desv_factor(x, models_folder_path, x_target, y_target, weights, path_oofem, path_oofem_extractor):
    

    #######################################
    ### SE CREA EL MODELO (ARCHIVO .in) ###
    #######################################
    #Se crea una carpeta auxiliar "model_i"
    totalModels= -1
    
    for base, dirs, files in os.walk(models_folder_path):
        for directories in dirs:
            totalModels += 1
            
    print('Total Number of existing models',totalModels)

    i=totalModels+1
    os.popen("mkdir "+models_folder_path+"/model_"+"{:03}".format(i))
    #Se copia el archivo .in del modelo de oofem en la carpeta base
    os.popen("cp "+models_folder_path+"/base_model/base_model.in"+" "+models_folder_path+"/kk.in")
    #Se abre el archivo (se espera 0.1s a que se cree para que se pueda detectar el archivo recién creado)
    time.sleep(0.1) # Sleep for 0.1 seconds
    file = open(models_folder_path+"/kk.in" , 'r')
    filedata=file.read()
    file.close()
    file = open(models_folder_path+"/kk.in" , 'r')
    for line in file: 
        if "idm1" in line:
            #Convierto la línea en una lista
            oldline=line
            a=line.split()
            #Busco 'e0' y guardo su posición en index
            index = a.index('e0')
            #Modifico el valor de e0 (que está en la siguiente posición a la string 'e0')
            a[index+1]=str(x[0])
            #Busco 'e0' y guardo su posición en index
            index = a.index('w_k')
            #Modifico el valor de e0 (que está en la siguiente posición a la string 'e0')
            a[index+1]=str(x[1])
            #Busco 'e0' y guardo su posición en index
            index = a.index('w_r')
            #Modifico el valor de e0 (que está en la siguiente posición a la string 'e0')
            a[index+1]=str(x[2])
            #Busco 'e0' y guardo su posición en index
            index = a.index('w_f')
            #Modifico el valor de e0 (que está en la siguiente posición a la string 'e0')
            a[index+1]=str(x[3])
            #Busco 'e0' y guardo su posición en index
            index = a.index('f_k')
            #Modifico el valor de e0 (que está en la siguiente posición a la string 'e0')
            a[index+1]=str(x[4])
            #Busco 'e0' y guardo su posición en index
            index = a.index('f_r')
            #Modifico el valor de e0 (que está en la siguiente posición a la string 'e0')
            a[index+1]=str(x[5])
            newline=' '.join(a)+'\n'
    file.close()
    #Se crea un nuevo archivo
    os.popen("touch "+models_folder_path+"/model_"+"{:03}".format(i)+".in")
    newfile=open(models_folder_path+"/model_"+"{:03}".format(i)+".in" , 'w')
    filedata=filedata.replace(oldline,newline)
    newfile.write(filedata)
    newfile.close()
    #Se borra la copia del archivo base
    os.popen("rm "+models_folder_path+"/kk.in")

    #######################################
    ###       SE CALCULA EL MODELO      ###
    #######################################
    #Se ejecuta oofem_release para calcular el modelo
    cmd=path_oofem+' -f '+models_folder_path+'/model_'+"{:03}".format(i)+'.in'
    os.system(cmd)    
    time.sleep(0.1) # Sleep for 0.1 seconds
    cmd=path_oofem_extractor+' -f '+models_folder_path+'/model_'+"{:03}".format(i)+'.in > output.txt'
    os.system(cmd)
    time.sleep(0.1) # Sleep for 0.1 seconds
    
    ###############################################################################
    ### SE ELIMINA EL ARCHIVO .out, PARA EVITAR OCUPAR MUCHO ESPACIO EN MEMORIA ###
    ###############################################################################
    os.popen('rm output.out ')
    ############################################################################
    ###     SE MUEVEN LOS ARCHIVOS A LA CARPETA CORRESPONDIENTE "model_i"    ###
    ############################################################################
    os.popen('mv output.txt '+models_folder_path+'/model_'+"{:03}".format(i))
#    os.popen('mv output.out '+models_folder_path+'/model_'+str(i))
    os.popen('mv '+models_folder_path+'/model_'+"{:03}".format(i)+'.in  '+models_folder_path+'/model_'+"{:03}".format(i))
    
    # Se extraen las ordenadas de los puntos de ajuste y se almacenan en y_comp
    file_num_path = models_folder_path+'/model_'+"{:03}".format(i)+'/output.txt'
    time.sleep(0.1) # Sleep for 0.1 seconds
    x_num=[]
    x_num = extractOneColumn(file_num_path, 0)*(-1)
#    print('x_num')
#    print(x_num)
    y_num_1=[]
    y_num_2=[]
    y_num_1, y_num_2 = extractTwoColumns(file_num_path, 2, 3)
    y_num=[]
    for j in range(len(y_num_1)):
        load=(y_num_1[j]+y_num_2[j])/1000.0 # Aquí se calcula la reacción total en apoyos y se ajustan las unidades a kN, dividiendo por 1000
        y_num.append(load)
#    print('y_num')
#    print(y_num)
    y_comp=[]
    for j in range(len(x_target)):
        y_comp.append(interpolate_value(x_target[j], x_num, y_num))
#    print('y_comp')
#    print(y_comp)
    result = 0
    for j in range(len(y_target)):
        result += abs(y_target[j] - y_comp[j])/sum(y_target) * weights[j]
    
#    print('desv factor=' + result)
#    print(result)
    if os.path.getsize(models_folder_path+"/Summary_of_results.txt") == 0:
        results_file=open(models_folder_path+"/Summary_of_results.txt","a")
        results_file.write("model \t e0 \t w_k \t w_r \t w_f \t f_k \t f_r \n")
        results_file.close()
        
    record = "{:03}".format(i)+ " \t " + str(x[0]) + " \t " + str(x[1]) + " \t " + str(x[2]) + " \t " + str(x[3]) + " \t " + str(x[4]) + " \t " + str(x[5]) + " \t " + str(result) + " \n" 
    results_file=open(models_folder_path+"/Summary_of_results.txt","a")
    results_file.write(record)
    results_file.close()
    print("model \t e0 \t w_k \t w_r \t w_f \t f_k \t f_r \n")
    print(record)
    return result
    

 
