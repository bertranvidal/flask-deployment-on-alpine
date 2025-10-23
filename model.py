import pandas as pd
from sklearn.datasets import load_iris, load_wine, load_breast_cancer, make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib
import matplotlib.pyplot as plt
from static.utils import figures_path
import os
from typing import Tuple, List
import numpy as np
import seaborn as sns
from memory_profiler import memory_usage, profile
import time
import multiprocessing as mp
from multiprocessing import Pool

matplotlib.use('agg')

DATASETS = {
    'iris': load_iris,
    'wine': load_wine,
    'breast_cancer': load_breast_cancer,
}

MODELS = {
    'RandomForest': RandomForestClassifier,
    'SVC': SVC,
    'LogisticRegression': LogisticRegression
}


def load_dataset(name: str) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Load a dataset by name.

    Parameters:
        name (str): The name of the dataset to load.

    Returns:
        Tuple[pd.DataFrame, pd.Series]: A tuple containing the features DataFrame and target Series.

    Raises:
        ValueError: If the dataset name is not found.
    """
    if name in DATASETS:
        dataset = DATASETS[name]()
        return pd.DataFrame(dataset.data, columns=dataset.feature_names), dataset.target, dataset.target_names
    else:
        raise ValueError(f"Dataset {name} not found.")


def train_and_evaluate(dataset_name: str, model_name: str, train_size: float, test_size: float, file_result: str) -> \
        Tuple[float, float]:
    """
    Train and evaluate a RandomForestClassifier on the specified dataset.

    Parameters:
        dataset_name (str): The name of the dataset to use.
        train_size (float): The proportion of the dataset to include in the train split.
        model_name (str): the name of the model
        test_size (float): The proportion of the dataset to include in the test split.
        file_result (str): path of the file to store the rests

    Returns:
        Tuple[float, float]: A tuple containing the accuracy and error rate of the model.
    """
    X, y, target_names = load_dataset(dataset_name)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size, test_size=test_size)

    model = MODELS[model_name]()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    error = 1 - accuracy

    plot_results(y_test, y_pred, file_result, target_names)

    return accuracy, error


def plot_results(y_test: pd.Series, y_pred: pd.Series, file_result: str, target_names: pd.Series) -> None:
    """
    Plot the results of the model predictions.

    Parameters:
        y_test (pd.Series): The true labels.
        y_pred (pd.Series): The predicted labels.
        file_result (str): Name of the file to store the results
        target_names (pd.Series): The names of the target classes.

    Returns:
        None
    """
    '''
    plt.figure(figsize=(10, 6))
    plt.hist([y_test, y_pred], label=['True', 'Predicted'], bins=len(target_names), alpha=0.7)
    plt.legend(loc='upper right')
    plt.xticks(ticks=range(len(target_names)), labels=target_names)
    plt.xlabel('Classes')
    plt.ylabel('Frequency')
    plt.title('True vs Predicted Classes')
    plt.savefig(os.path.join(figures_path, file_result))
    plt.close()
    '''

    # Count occurrences
    classes = np.unique(y_test)
    true_counts = [np.sum(y_test == cls) for cls in classes]
    pred_counts = [np.sum(y_pred == cls) for cls in classes]

    x = np.arange(len(target_names))
    width = 0.35  # Width of the bars

    plt.figure(figsize=(10, 6))
    plt.bar(x - width / 2, true_counts, width, label='True')
    plt.bar(x + width / 2, pred_counts, width, label='Predicted')

    plt.xlabel('Classes')
    plt.ylabel('Frequency')
    plt.title('True vs Predicted Classes')
    plt.xticks(ticks=x, labels=[str(cls) for cls in classes])
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(figures_path, file_result))
    plt.close()


def get_dataset_statistics(dataset_name: str) -> pd.DataFrame:
    """
    Get descriptive statistics for a dataset.

    Parameters:
        dataset_name (str): The name of the dataset to analyze.

    Returns:
        pd.DataFrame: A DataFrame containing the descriptive statistics of the dataset features.
    """
    X, y, target_names = load_dataset(dataset_name)
    stats = X.describe()
    return stats


def perform_eda(dataset_name: str) -> List[str]:
    """
    Perform exploratory data analysis for a dataset and save plots.

    Parameters:
        dataset_name (str): The name of the dataset to analyze.

    Returns:
        List[str]: A list of file paths to the generated images.
    """
    X, y, _ = load_dataset(dataset_name)
    images = []

    for column in X.columns:
        plt.figure(figsize=(10, 6))
        X[column].hist(bins=30)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        c_string = column.replace(" ", "")
        result_name = f'{dataset_name}_{c_string}_dist.png'
        image_path = os.path.join(figures_path, result_name)
        plt.savefig(image_path)
        plt.close()
        images.append('../static/' + result_name)

    # Correlation matrix heatmap
    correlation_matrix = X.corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix')
    correlation_image_path = os.path.join(figures_path, f'{dataset_name}_correlation_matrix.png')
    plt.savefig(correlation_image_path)
    plt.close()

    images.append('../static/' + f'{dataset_name}_correlation_matrix.png')

    return images


@profile
def generate_synthetic_dataset(n_rows: int, n_cols: int, n_classes: int, model_name: str, train_size: float,
                               test_size: float) -> Tuple[float, float, str]:
    """
    Generate a synthetic dataset and train a model on it.

    Parameters:
        n_rows (int): Number of rows in the synthetic dataset.
        n_cols (int): Number of columns in the synthetic dataset (maximum 10).
        n_classes (int): Number of classes in the synthetic dataset.
        model_name (str): The name of the model to use for training.
        train_size (float): The proportion of the dataset to include in the train split.
        test_size (float): The proportion of the dataset to include in the test split.

    Returns:
        Tuple[float, float, str]: A tuple containing the accuracy, error rate of the model, and the path to the saved figure.
    """
    if n_cols > 10:
        raise ValueError("Number of columns cannot exceed 10.")

    X, y = make_classification(n_samples=n_rows, n_features=n_cols, n_classes=n_classes, n_informative=n_cols,
                               n_redundant=0, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size, test_size=test_size,
                                                        random_state=42)

    model = MODELS[model_name]()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    error = 1 - accuracy

    final_file = f'Synthetic_Samples{n_rows}_Columns{n_cols}_Classes{n_classes}_Columns{n_cols}.png'
    img_url = '../static/' + f'{final_file}'

    plot_results(y_test, y_pred, final_file, list(range(n_classes)))

    return accuracy, error, img_url


def train_model_on_data(model_name: str, X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray,
                        y_test: np.ndarray) -> Tuple[float, float]:
    """
    Train a specified model on the given data.

    Parameters:
        model_name (str): The name of the model to use.
        X_train (np.ndarray): Training features.
        X_test (np.ndarray): Testing features.
        y_train (np.ndarray): Training labels.
        y_test (np.ndarray): Testing labels.

    Returns:
        Tuple[float, float]: A tuple containing the accuracy and error rate of the model.
    """
    model = MODELS[model_name]()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    error = 1 - accuracy
    return accuracy, error




class ErrorDimension(Exception):
    pass

def multiplica_matrices_ef(A: np.ndarray, B: np.ndarray) ->np.ndarray:
    # Assuming A is a m $\times$ n matrix represented as np.ndarray
    # Assuming B is a n $\times$ p matrix represented as np.ndarray
    # Rest of your code
    m_a = len(A[0])
    n_a = len(A[1])
    n_b = len(B[0])
    p_b = len(B[1])
  
    if n_a == n_b:
        C = np.empty((m_a, n_a))
        for i in range(0, m_a):
            c_i = C[i]
            for k in range(0, n_a):
                b_k = B[k]
                a_i_k = A[i][k]
                for j in range(0, p_b):
                    c_i[j] += a_i_k*b_k[j]

        return C
    else:
        raise ErrorDimension('Las matrices A y B no se pueden multiplicar')


def genera_matriz_aleatoria(filas: int, columnas: int) ->np.ndarray:
    return np.random.random((filas, columnas))

def puente(tamano: list) ->str:
    filas = tamano[0]
    columnas = tamano[1]
    try:
        A = genera_matriz_aleatoria(filas, columnas)
        B = genera_matriz_aleatoria(filas, columnas)
        C = multiplica_matrices_ef(A, B)
        print(f'Finalizada la multiplicacion de dimensiones [{filas}, {columnas}]')
    except ErrorDimension as error:
        print(error)

 
    
def compare_execution() -> Tuple[float, float]:
    """
    Compare execution time of sequential vs parallel processing for training models on a synthetic dataset.

    Returns:
        Tuple[float, float]: A tuple containing the execution times for sequential and parallel processing.
    """
    sequential_time = 0
    parallel_time = 0
    matrix_sizes = [310, 210, 400, 160]

    ##CODE FOR STUDENTS
    tamanos = ([310, 310], [400, 400], [160, 160], [210, 210])

    print('Version monoprocesador')
    inicio1 = time.time()
    for tamano in tamanos:
        puente(tamano)
    final1 = time.time()
    tiempo_monoprocesador = final1 - inicio1

    print('Version multiprocesador')

    inicio2 = time.time()
    p = Pool(2)
    p.map(puente, tamanos)
    fin2 = time.time()
    tiempo_multiprocesador = fin2-inicio2

    return tiempo_monoprocesador, tiempo_multiprocesador


