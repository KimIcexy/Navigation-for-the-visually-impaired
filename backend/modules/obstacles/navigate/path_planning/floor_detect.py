from roboflow import Roboflow
rf = Roboflow(api_key="rhADRHQ1t9je2cWjdWgW")
project = rf.workspace().project("floor-detection-btxc3")
model = project.version(2).model

# infer on a local image
test_image = './test1.jpg'
print(model.predict(test_image, confidence=40, overlap=30).json())

# visualize your prediction
model.predict(test_image, confidence=40, overlap=30).save("prediction.jpg")

# infer on an image hosted elsewhere
# print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())