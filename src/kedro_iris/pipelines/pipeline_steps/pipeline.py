from kedro.pipeline import Pipeline, node

from .nodes import preprocess_data, target_creation, split_data, train_model, eval_model


def create_pipeline(**kwargs):
    return Pipeline([
        node(
            preprocess_data,
            inputs=['iris_data', 'params:cols_num'],
            # To-Do: Serialize preprocessing pipeline
            outputs=['iris_data_processed', 'sk_pipeline'],
            name="preprocessing"
        ),
        node(
            target_creation,
            inputs=['iris_data_processed'],
            outputs='iris_data_targeted',
            name="target_creation"
        ),
        node(
            split_data,
            inputs=['iris_data_targeted'],
            outputs=['train', 'valid', 'test'],
            name="split_data"
        ),
        node(
            train_model,
            inputs=['train', 'valid', 'params:cols_feat', 'params:model_params'],
            outputs=['model', 'val_metrics'] ,
            name="train_model"
        ),
        node(
            eval_model,
            inputs=['model', 'test', 'params:cols_feat', 'params:baseline'],
            outputs='results',
            name="eval_model"
        )
    ])
