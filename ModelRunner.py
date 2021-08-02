from imageai.Classification.Custom import CustomImageClassification
import os

filepath = os.getcwd()

detector = CustomImageClassification()
detector.setModelTypeAsInceptionV3()

detector.setModelPath(filepath + "\\Anime3\\models\\model_ex-073_acc-0.996815.h5")
detector.setJsonPath(filepath+ "\\Anime3\\json\\model_class.json")

detector.loadModel(num_objects=2)

predictions, probabilities = detector.classifyImage(filepath + "\\pfp\\pfp\\i.png", result_count=2)

print("results:")
for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction , " : " , eachProbability)
