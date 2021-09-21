import pandas as pd
import numpy as np
from typing import Any, Dict, Tuple, List

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted
from sklearn.metrics import f1_score

# To-Do: Refactor sklearn transformer
class CastingTransformer(BaseEstimator, TransformerMixin):
    """
        Sklearn class helper to preprocess data
    """
    def __init__(self, cols_cat: list=[], cols_num: list=[]):
        assert len(cols_cat) or len(cols_num)
        self.cols_cat = cols_cat
        self.cols_num = cols_num
    
    def fit(self, X: pd.DataFrame, y=None):
        return self
    
    def transform(self, X: pd.DataFrame):
        X = X.copy()
        for col in self.cols_cat:
            X[col] = pd.Categorical(X[col])
            X[col] = X[col].cat.codes.astype(int)
            
        for col in self.cols_num:
            X[col] = pd.to_numeric(X[col], errors='coerce', downcast='float')
        
        return X

def preprocess_data(data: pd.DataFrame, cols_num: List) -> List:
    # Applying basic preprocessing step
    sk_pipeline = Pipeline(
        [
            ('casting', CastingTransformer(cols_num=cols_num))
        ])
    sk_pipeline.fit(data)
    data_prec = sk_pipeline.transform(data)

    # To-Do: Serialize data statistics for drift detection

    # Serializing preprocessing pipeline
    return [data_prec, sk_pipeline]

def target_creation(data: pd.DataFrame) -> pd.DataFrame:
    """
        Generate target column
    """

    target_to_number = {'setosa': 0, 'versicolor': 1, 'virginica': 2}
    data['target'] = data['species'].replace(target_to_number)

    return data.drop('species', axis=1)

def split_data(data: pd.DataFrame) -> List:
    """
        Split data to generate val, test and train partitions
    """

    rest, train = train_test_split(data, test_size=0.2)
    valid, test = train_test_split(data, test_size=0.5)

    return [train, valid, test]

def train_model(train: pd.DataFrame, valid: pd.DataFrame, cols_feat: List, model_params: Dict) -> List:
    """
        Training a simple random forest
    """

    train_x, train_y = train[cols_feat], train[['target']]
    valid_x, valid_y = valid[cols_feat], valid[['target']]

    clf = RandomForestClassifier(**model_params)
    clf.fit(train_x, train_y)

    val_pred = clf.predict(valid_x)
    trn_pred = clf.predict(train_x)

    # Validation metrics
    trn_metric = f1_score(train_y, trn_pred, average='macro')
    val_metric = f1_score(valid_y, val_pred, average='macro')

    val_metrics = {
        'f1_trn': trn_metric, 
        'f1_val': val_metric, 
    }

    # Serializing parameters, model and validation metrics
    return [clf, val_metrics] 

def eval_model(model, test: pd.DataFrame, cols_feat: List, baseline: float) -> Dict:
    """
        Evaluate model performance
    """

    test_x, test_y = test[cols_feat], test.target
    test_pred = model.predict(test_x)
    test_metric = f1_score(test_y, test_pred, average='macro')

    results = {
        'f1_test': test_metric,
        # Conditions to realease a new model
        'baseline_condition': test_metric > baseline
    }

    return results
