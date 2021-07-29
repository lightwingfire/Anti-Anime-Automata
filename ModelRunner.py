from imageai.Classification.Custom import CustomImageClassification

detector = CustomImageClassification()
detector.setModelTypeAsInceptionV3()

detector.setModelPath("C:\\Users\\endri\\Desktop\\Git\\AAA\\Anime2\\models\\model_ex-074_acc-0.994175.h5")
detector.setJsonPath("C:\\Users\\endri\\Desktop\\Git\\AAA\\Anime2\\json\\model_class.json")

detector.loadModel(num_objects=3)

#print(detector.classifyImage("C:\\Users\\endri\\Desktop\\Git\\AAA\\pfp-anime\\Solo34071115.jpg"))

predictions, probabilities = detector.classifyImage("C:\\Users\\endri\\Desktop\\Git\\AAA\\pfp\\original (3).jpg", result_count=3)

print("HELP")
for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction , " : " , eachProbability)
