# Semantic Segmentation
### Introduction
Training segmentation networks, which paint each pixel of the image a different color, based on its class and use the segmented images to find free space on the road.

Labelling the pixels of a road in images using a Fully Convolutional Network (FCN) with the FCN-8 architecture developed at Berkeley based on [Long et al.: Fully Convolutional Networks for Semantic Segmentation](https://github.com/dvu4/CarND-Semantic-Segmentation/blob/master/long_shelhamer_fcn.pdf).

### Architecture
Pre-trained VGG-16 is converted to a FCN by converting the fully connected layer to 1x1 convolution and setting the depth of layer to the number of classes (i.e 2 for road and non-road). The performance of the network is enhanced by the skip connections through performing 1x1 convolutions on previous VGG-16 layers (i.e layer 3 and 4) and adding them element-wise to upsampled lower-level layers (i.e 1x1 convolved layer 7 is upsampled, then added to 1x1 convolved layer 4 and repeat for layer 4 and layer 3). 

![alt text](https://raw.githubusercontent.com/dvu4/CarND-Semantic-Segmentation/master/runs/skipConnections.png)

### Optimizer
 - The loss function used is cross entropy 
 - AdamOptimizer is used for optimization

### Training
The hyperparameters for the training
 - epochs : 50
 - batch_size : 5
 - keep_prob : 0.5
 - learning_rate : 0.0001

### Results
---
 - Average loss per batch is below 0.2 after 2 epoches 
 - Average loss per batch is below 0.1 after 9 epoches
 - Average loss per batch is below 0.05 after 20 epoches 
 - Average loss per batch is below 0.039 after 30 epoches
 - Average loss per batch is below 0.031 after 40 epoches 
 - Average loss per batch is below 0.022 at 50 epoches 

Sample output images for road classification with the segmentation class overlaid upon the input images in green.

![alt text](https://raw.githubusercontent.com/dvu4/CarND-Semantic-Segmentation/master/runs/1512112488.417907/um_000003.png)

![alt text](https://raw.githubusercontent.com/dvu4/CarND-Semantic-Segmentation/master/runs/1512112488.417907/um_000010.png)

![alt text](https://raw.githubusercontent.com/dvu4/CarND-Semantic-Segmentation/master/runs/1512112488.417907/um_000016.png)

![alt text](https://raw.githubusercontent.com/dvu4/CarND-Semantic-Segmentation/master/runs/1512112488.417907/uu_000000.png)

![alt text](https://raw.githubusercontent.com/dvu4/CarND-Semantic-Segmentation/master/runs/1512112488.417907/uu_000007.png)

![alt text](https://raw.githubusercontent.com/dvu4/CarND-Semantic-Segmentation/master/runs/1512112488.417907/umm_000062.png)

![alt text](https://raw.githubusercontent.com/dvu4/CarND-Semantic-Segmentation/master/runs/1512112488.417907/uu_000095.png)

![alt text](https://raw.githubusercontent.com/dvu4/CarND-Semantic-Segmentation/master/runs/1512112488.417907/umm_000006.png)

![alt text](https://raw.githubusercontent.com/dvu4/CarND-Semantic-Segmentation/master/runs/1512112488.417907/umm_000081.png)

![alt text](https://raw.githubusercontent.com/dvu4/CarND-Semantic-Segmentation/master/runs/1512112488.417907/umm_000035.png)

---

### Setups
##### Frameworks and Packages
Make sure you have the following is installed:
 - [Python 3](https://www.python.org/)
 - [TensorFlow](https://www.tensorflow.org/)
 - [NumPy](http://www.numpy.org/)
 - [SciPy](https://www.scipy.org/)
##### Dataset
Download the [Kitti Road dataset](http://www.cvlibs.net/datasets/kitti/eval_road.php) from [here](http://www.cvlibs.net/download.php?file=data_road.zip).  Extract the dataset in the `data` folder.  This will create the folder `data_road` with all the training a test images.

### Start
##### Implement
Implement the code in the `main.py` module indicated by the "TODO" comments.
The comments indicated with "OPTIONAL" tag are not required to complete.
##### Run
Run the following command to run the project:
```
python main.py
```
**Note** If running this in Jupyter Notebook system messages, such as those regarding test status, may appear in the terminal rather than the notebook.

### Submission
1. Ensure you've passed all the unit tests.
2. Ensure you pass all points on [the rubric](https://review.udacity.com/#!/rubrics/989/view).
3. Submit the following in a zip file.
 - `helper.py`
 - `main.py`
 - `project_tests.py`
 - Newest inference images from `runs` folder
 


 ## How to write a README
A well written README file can enhance your project and portfolio.  Develop your abilities to create professional README files by completing [this free course](https://www.udacity.com/course/writing-readmes--ud777).
