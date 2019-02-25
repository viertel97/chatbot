from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

training_data = load_data('data/nlu.md')
trainer = Trainer(RasaNLUConfig("nlu_model_config.json"))
trainer.train(training_data)
model_directory = trainer.persist('./projects/default/')  # Returns the directory the model is stored in


from rasa_core.domain import TemplateDomain
domain = TemplateDomain.load("restaurant_domain.yml")