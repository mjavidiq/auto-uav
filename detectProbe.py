from detecto import visualize, core, utils
import pickle
import torch
# print(torch.cuda.is_available())
loaded_model = torch.load('finalized_model1.sav',map_location=lambda storage, loc: storage)
# loaded_model = torch.load('finalized_model1.sav')

# loaded_model = pickle.load(open('finalized_model.sav','rb'))
for i in range(2 ,3):
    image = utils.read_image('Images/fg.jpg')
    labels, boxes, scores = loaded_model.predict_top(image)
    visualize.show_labeled_image(image, boxes, labels)
    print(scores)
    print(boxes)