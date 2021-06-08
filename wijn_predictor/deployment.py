import os
import pandas as pd
from github import Github
from sklearn.linear_model import LinearRegression
import datetime
import numpy as np

class Deployment:

    def __init__(self, base_directory, context):
        g = Github(os.environ['git_token'])
        # g = Github('')
        repo = g.get_repo('roelofcoster/ubiops')
        sha = repo.get_contents('mdl.p').sha
                
        coef = repo.get_contents('mdl.p').decoded_content.decode()
        coef = coef.replace('[', '')
        coef = coef.replace(']', '')
        coef = coef.split(',')
        coef = [float(x) for x in coef]
        coef = np.array(coef)
        
        bestand = os.path.join(base_directory, 'winequality-red.csv')
        dat = pd.read_csv(bestand)
        y = dat.quality
        X = dat.drop('quality', axis = 1)
        self.mdl = LinearRegression().fit(X, y)
        self.mdl.coef_ = coef
        
    def request(self, data):
        dat = pd.read_csv(data['bestand'])
        dat = dat[[
            'fixed acidity',
            'volatile acidity',
            'citric acid',
            'residual sugar',
            'chlorides',
            'free sulfur dioxide',
            'total sulfur dioxide',
            'density',
            'pH',
            'sulphates',
            'alcohol']]
        prd = self.mdl.predict(dat)
        prd = np.round(prd)
        uitkomst = dat
        uitkomst['predictie'] = prd
        uitkomst.to_csv('predictie.csv')
        return {'uitkomst': 'predictie.csv'}
