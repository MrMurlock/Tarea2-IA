import numpy as np
from typing import Optional

class Regresion:

    def __init__(self, data, theta=None, alpha=None):
        self.theta = np.array(theta) if theta else np.array(np.zeros(data.shape[1]))
        self.alpha = alpha or 0.01
        self.m = len(data)

        self.x = np.append(np.ones((self.m, 1)), np.reshape(np.array(data[:, 0]), (self.m, 1)), axis=1)
        self.y = np.array(data[:, 1])
    
    def hipotesis(self, x):
        if type(x) != np.ndarray: x = np.array(x)
        if x.shape != (2,): x = np.append([1], x)
        return np.sum(x.dot(self.theta))

    def costo(self, theta: Optional[np.array] = None):
        if type(theta) != np.ndarray: theta = self.theta
        return np.sum((self.x.dot(theta).transpose() - self.y)**2)/(2*self.m)

    def _calculo_gradiente(self, theta: Optional[np.array] = None):
        if type(theta) != np.ndarray: theta = self.theta
        _theta = np.array(self.theta)
        aux = self.x.dot(theta)
        
        for i in range(_theta.shape[0]):
            _theta[i] = float(_theta[i] - self.alpha*np.array((aux - self.y)*self.x[:, i]).sum()/self.m)
        return self.costo(_theta),_theta
    
    def gradiente(self, itr):
        # este metodo no debe existir aqui, su codigo debe ejecutarse al presionar un boton start
        # por ende debe estar en el metodo del boton

        for i in range(itr):
            costo, theta = self._calculo_gradiente()
            #print(f'[{i+1}] J:{costo} \n\t {theta}')
            self.theta = np.array(theta)
    
    def normal(self):
        x_t = self.x.transpose()
        return np.linalg.inv(np.float_(x_t.dot(self.x))).dot(x_t).dot(self.y)