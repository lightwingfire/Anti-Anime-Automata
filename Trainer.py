from imageai.Classification.Custom import ClassificationModelTrainer
#https://github.com/OlafenwaMoses/ImageAI/blob/master/imageai/Classification/CUSTOMTRAINING.md
model_trainer = ClassificationModelTrainer()
model_trainer.setModelTypeAsInceptionV3()
model_trainer.setDataDirectory(data_directory ="C:\\Users\\endri\\Desktop\\Git\\AAA\\Anime2",
                               train_subdirectory = "C:\\Users\\endri\\Desktop\\Git\\AAA\\Anime2\\train",
                               test_subdirectory = "C:\\Users\\endri\\Desktop\\Git\\AAA\\Anime2\\test")
model_trainer.trainModel(num_objects=3, num_experiments=150, enhance_data=True, batch_size=32, show_network_summary=True)