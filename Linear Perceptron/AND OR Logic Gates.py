import numpy as np
import matplotlib.pyplot as plt

## CHART

### chart title is missing logic gate type name

def plot_chart(X, w, attempt_counter):
    
    # Find point coordinates 
    
    x_coordinates = X[:, 1]
    y_coordinates = X[:, 2]
    
    # Adjust function domain display
    
    x = np.linspace(-np.max(X), np.max(X))
    
    # Obtain coefficients
    
    w1, w2, w3 = np.split(w, w.shape[0])
    
    # In case y coefficient equals zero (i.e. x = n)
    
    if w3.item() == 0:
        print('Not a function!')
       
    else:
        y = (-w2.item() * x - w1.item()) / w3.item()
        y2 = (-w2.item() * x - w1.item() + 1) / w3.item()
        y3 = (-w2.item() * x - w1.item() - 1) / w3.item()
        a = w2.item()
        b = w3.item()
        c = w1.item()
    
        # Coefficient formatting
        
        if a - int(a) == 0:
            a = int(a)
        else:
            a = round(a, 2)
        
        if b - int(b) == 0:
            b = int(b)
        else:
            b = round(b, 2)
        
        if c - int(c) == 0:
            c = int(c)
        else:
            c = round(c, 2)
        
        # Obtain and format slope-intercept form of a line
        
        graph_equation = '{0}x {1}y {2}=0'.format(a, b, c)        
        graph_equation_margin_plus1 = '{0}x {1}y {2}=0'.format(a, b, c - 1)
        graph_equation_margin_minus1 = '{0}x {1}y {2}=0'.format(a, b, c + 1)
        
        #print(graph_equation_margin_minus1)
        
        thisdict = {'0x': '',
                    'x ': 'x+',
                    '0y': '',
                    'y 0': 'y',
                    'y ': 'y+',
                    '+-': '-',
                    #' ': ''
                    }

        def get_value(k): 
            for key, value in thisdict.items(): 
                 if k == key: 
                     return value
        
        for i in thisdict.keys():
            if i in graph_equation:
                graph_equation = graph_equation.replace(i, get_value(i))      
                graph_equation_margin_plus1 = graph_equation_margin_plus1.replace(i, get_value(i))      
                graph_equation_margin_minus1 = graph_equation_margin_minus1.replace(i, get_value(i))    
       
        # Plot graph
        
        plt.plot(x, y2, label=graph_equation_margin_plus1, color='green', linestyle='dashed')
        plt.plot(x, y, label=graph_equation, color='blue')
        plt.plot(x, y3, label=graph_equation_margin_minus1, color='red', linestyle='dashed')
        plt.title('Weight adjustment, step {}'.format(attempt_counter))
        plt.xlabel('x axis')
        plt.ylabel('y axis')
        plt.legend(loc='upper right')
        plt.grid(alpha=.4,linestyle='--')
        
        # Coordinate colour labeling
        
        coordinate_colors = []
        
        for i in range(Y.shape[0]):
            if Y[i] == -1:
                coordinate_colors.append('Red')
            if Y[i] == 1:
                coordinate_colors.append('Green')
                
        plt.scatter(x_coordinates, y_coordinates, color=coordinate_colors)
        plt.show()
  
   
## DATASET IMPORT

dataset_path = r'D:\ML\SVM\AND_GATE.csv'
dataset = np.genfromtxt(dataset_path, delimiter=',', skip_header=1)

# Input values

X_inputs = dataset[:, :-1]

# Input classes

Y = dataset[:, -1:]

# Add inputs for bias

bias_inputs = np.ones((X_inputs.shape[0], 1), dtype=int)
X = np.concatenate((bias_inputs, X_inputs), axis=1)

# Input scaling (incl. bias)

def min_max_scale(X, range=(0, 1)):
    mi, ma = range
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std * (ma - mi) + mi
    return X_scaled

#X = min_max_scale(X)

# Split input matrix into vectors to update weights (bias incorporated into weights)

chunks = np.split(X, 4)

# Initialise weights

w = np.zeros((X.shape[1], 1), dtype=int)

### TRAINING

### soft-margin loss function (currently not in use)
def hinge_loss(inputs, label, weights):
    hinge = np.max([0, 1 - label * np.dot(inputs, weights)])
    print(hinge)

attempt_counter = 0
    
while np.any(np.matmul(X, w) * Y <= 0):
    for i in range(X.shape[0]):
        if np.matmul(chunks[i], w) * Y[i] <= 0:
            w = np.add(w.T, chunks[i] * Y[i])
            w = w.T
            attempt_counter += 1
            #plot_chart(X, w, attempt_counter)
            #print(w, "step {}".format(i + 1))

# Measure Distance
            
w_mag = np.linalg.norm(w)

for i in range(X.shape[0]):
    d = np.matmul(chunks[i], w) / w_mag
    print("Decision boundary distance to point {} is: ".format(i + 1), round(d.flatten().tolist()[0], 2), sep='')
  
print("Final weights are {}, {} training steps taken".format(w.flatten().tolist(), attempt_counter))
plot_chart(X, w, attempt_counter)