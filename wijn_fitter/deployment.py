import os
import pandas as pd
from github import Github
from sklearn.linear_model import LinearRegression
import datetime

class Deployment:
    def __init__(self, base_directory, context):        
        pass
       
    def request(self, data):
        dat = pd.read_csv(data['bestand'])
        X = dat[[
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
        y = dat['quality']
        mdl = LinearRegression().fit(X, y)
        coef = str(list(mdl.coef_))
        
        g = Github(os.environ['git_token'])
        repo = g.get_repo('roelofcoster/ubiops')
        sha = repo.get_contents('mdl.p').sha
        repo.update_file('mdl.p', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), coef, sha, branch = 'main')       

        return {'uitkomst': True}
