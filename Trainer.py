from imageai.Classification.Custom import ClassificationModelTrainer
import os
#https://github.com/OlafenwaMoses/ImageAI/blob/master/imageai/Classification/CUSTOMTRAINING.md

filepath = os.getcwd()

model_trainer = ClassificationModelTrainer()
model_trainer.setModelTypeAsInceptionV3()
model_trainer.setDataDirectory(data_directory = filepath + "\\Anime3",
                               train_subdirectory = filepath + "\\Anime3\\train",
                               test_subdirectory = filepath + "\\Anime3\\test")
model_trainer.trainModel(num_objects=2, num_experiments=150, enhance_data=True, batch_size=32, show_network_summary=True)