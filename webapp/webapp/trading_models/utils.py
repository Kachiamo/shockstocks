import logging

from backtesting.utils import backtest
from .ml_models import train_logistic_regression

logging.basicConfig()
log = logging.getLogger(__name__)


ML_MODEL_CHOICES = [
    ("logistic_regression", "logistic regression")
]

ML_MODELS = {
    "logistic_regression": train_logistic_regression,
}

def train_trading_model(trading_model, train=0.3, period="1y"):
    # probably not the best name, but returns a strategy with df, signals, actions, and plotting
    strategy = backtest(trading_model.strategy, trading_model.symbol, period)

    # get X_train and y_train
    # Get the length for training data size
    train_length = round(len(strategy.df.keys())*train)

    # Clean the data for training
    df = strategy.df.dropna()

    # Get the training dataframe
    train = df[:train_length]

    # Get the name of the action column
    y_column = f"{strategy.strategy}_Action"
    y_train = train[y_column]
    X_train = train.drop(columns=[y_column])

    # Get the model class
    model_class = ML_MODELS.get(trading_model.ml_model)

    # Instantiate the model with the X and y train data
    model_instance = model_class(X_train, y_train)

    # Save the model and its score
    log.critical(f"{trading_model.symbol} {trading_model.strategy} Training Data Score: {model_instance.score(X_train, y_train)}")
