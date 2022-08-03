from Reader import Reader
from Regresion import Regresion
import matplotlib.pyplot as pl
import numpy as np
from tabulate import tabulate

# empezar con objeto de clase regresion con set training al 100%, sin set de testeo
reader = Reader('ex2data1.txt')
data = reader.get_data()
regresion = Regresion(training_data = data)

print(f'\n----------------------------------------------\n')

# 1.- grafico dispersion
group0, group1 = reader.get_groups()
def scatter_plot(func = lambda: None):
    # func es una funcion parametro pasa por referencia
    #en caso de no pasar ninguna como en la linea 28, se crea una, usando lambda, y no retorna nada
    pl.scatter(x=group0[:,1], y=group0[:,2], color='red', marker = 'o', label='No admitido')
    pl.scatter(x=group1[:,1], y=group1[:,2], color='blue', marker = '*', label='Admitido')
    pl.xlabel('Examen 1')
    pl.ylabel('Examen 2')
    pl.title('Clasificador Binario')
    func()
    pl.legend()
    pl.show()

scatter_plot()

# 2.- funcion sigmoidal
x = [0,0,0]
prediccion = regresion.hipotesis(x=x)
print(f'Testeo Hipotesis')
print(f'\tx: {x}')
print(f'\tresultado: {round(prediccion, 3)}')

# 3.- funcion costo
costo = regresion.cost()
print(f'Testeo Costo')
print(f'\ttheta utilizado: {regresion.theta}')
print(f'\tresultado: {round(costo, 3)}')

# 4.- optimizacion
theta_inicial = [0,0,0]
costo, theta = regresion.optimize(theta=theta_inicial)
print(f'Testeo Optimizacion')
print(f'\tTheta inicial: {theta_inicial}')
print(f'\tTheta optimo: {theta}')
print(f'\tCosto: {round(costo, 3)}')
# 4.1- grafico
def graph_boundary():
    x_boundary = np.array([np.min(data[:,1]), np.max(data[:,1])])
    y_boundary = -(theta[0] + theta[1]*x_boundary)/theta[2]
    pl.axline(x_boundary, y_boundary, color='mediumpurple' ,label='Limite de decision')
scatter_plot(graph_boundary)

# 5.- prediccion
x = [1, 45., 85.]
probabilidad, prediction = regresion.predict(x=x, theta=theta)
print(f'Testeo Prediccion')
print(f'\tx: {x}')
print(f'\ttheta utilizado: {theta}')
print(f'\tprobabilidad: {round(probabilidad, 3)}')
print(f'\tresultado: {prediction}')
# 5.1- grafico
def graph_prediction():
    graph_boundary()
    pl.plot(x[1], x[2], 'o:g',label='Prediccion')
scatter_plot(graph_prediction)

print(f'\n----------------------------------------------\n')

# 6.- desempeño
#6.1- separar los datos
np.random.shuffle(data)
training_data = data[0:80,:]
test_data = data[80:,:]
regresion = Regresion(training_data=training_data, test_data=test_data)
#6.2- optimizacion
costo, theta = regresion.optimize()
print(f'Optimizacion (80% training / 20% testing)')
print(f'\tTheta inicial: {theta_inicial}')
print(f'\tTheta minimo: {theta}')
print(f'\tCosto: {round(costo, 3)}')
#6.3- grafico
def graph_boundary2():
    x_boundary = np.array([np.min(training_data[:,1]), np.max(training_data[:,1])])
    y_boundary = -(theta[0] + theta[1]*x_boundary)/theta[2]
    pl.axline(x_boundary, y_boundary, color='mediumpurple' ,label='Limite de decision')
scatter_plot(graph_boundary2)
#6.4- rendimiento
recall, precision, fmeasure = regresion.perfomance()
print('Rendimiento (80% training / 20% testing)')
print(f'\trecall: {recall}')
print(f'\tprecision: {precision}')
print(f'\tf-measure: {fmeasure}')
#6,5- matriz confusion
print('\n-------------- Matriz de Confusion ---------------')

mconfusion = [
    [
        0,
        regresion.true_negative,
        regresion.false_negative,
        round(regresion.true_negative/(regresion.true_negative + regresion.false_negative), 3),
        round(regresion.true_negative/(regresion.true_negative + regresion.false_positive), 3),
        #falta fmeasure
    ],
    [
        1,
        regresion.false_positive,
        regresion.true_positive,
        round(precision, 3),
        round(recall,3),
        round(fmeasure, 3)
    ]
    
]

mconfusion[0].append(
    round(2*(mconfusion[0][4]*mconfusion[0][3])/ (mconfusion[0][4] + mconfusion[0][3]), 3)
)

mconfusion.append(
    [
        '',
        '',
        'Promedio Total:',
        round((mconfusion[0][3] + mconfusion[1][3])/2 ,3), #promedio precision
        round((mconfusion[0][4] + mconfusion[1][4])/2, 3), #promedio recall
        round((mconfusion[0][5] + mconfusion[1][5])/2, 3) #promedio fmeasure
    ]
)

print(tabulate(
    mconfusion,
    headers = ['Y\YP', 0, 1, 'Precision', 'Recall', 'F-Measure'],
    # showindex=True,
    tablefmt='fancy_grid'
))