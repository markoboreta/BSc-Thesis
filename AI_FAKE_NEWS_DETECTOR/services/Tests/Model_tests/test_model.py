from ast import Not
import pytest
from prediciton_services_LR.LR import LR, vect_path as vpLR, model_path as mpLR
from prediction_services_NB.NB import NB, model_path as mpNB, vect_path as vpNB
from prediction_services_PA.PA import PA, model_path as mpPA, vect_path as vpPA


model_configs = {
    "LR": {
        "model_path": mpLR,
        "vect_path": vpLR,
        "class": LR
    },
    "NB": {
        "model_path": mpNB,
        "vect_path": vpNB,
        "class": NB
    },
    "PA": {
        "model_path": mpPA,
        "vect_path": mpPA,
        "class": PA
    }
}
@pytest.fixture(scope="module", params=["LR", "NB", "PA"])
def model(request):
    config = model_configs[request.param]
    return config["class"](config["model_path"], config["vect_path"])


def test_model_prediction(model):
    test_article = "Some rana''dom text for testing."
    prediction = model.predict_news_article(test_article)
    assert prediction is not None

def test_model_failure_on_empty_input(model):
    prediction = model.predict_news_article(None)
    assert prediction in "Error: Not good return on verdict"