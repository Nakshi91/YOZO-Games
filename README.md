
YOZO-Games
========

This git repository contains solution for each of the problems from YOZO games. 

Install
-------

    $ pip install -r requirements.txt

    
Problem 1.1
----

Find a suitable way to transform image1 to image 2 

(hints: contrast and transformation)


Image 1             |  Image 2
:-------------------------:|:-------------------------:
![Alt text](img/1.jpg "Image 1")  |  ![Alt text](img/2.jpg? "Image 2")

I think the possible transformation used for getting image2 from image 1 are as follow

    1. Contrast Enhancement 
    2. Perspective Correction/Transformation
    3. Cropping/Zooming

Problem 1.2
-------------------------

The following images are produced by a thermal camera, please find an appropriate way to eliminate the distortion created by the camera.
![Alt text](img/temp.jpg) 

To remove the distortion for these images created by thermal camera we need to do perspective correction for each of them.

#### Perspective Correction
In perspective correction a source image is transformed into a desired perspective view by computing the homography that maps the source points into the desired points. 

In this example, all the images are captured by a thermal camera and distorted. So we need a reference checkerboard image and need to transform each of the example images using homography.
 

Problem 2
-----------------------------------------
Develop a system that can track eye gaze, emotion, and faces from a video source near real time. The system should distinguish between real faces and faces from photos.  

##### Tasks and requirements:
* Based on existing techniques, build a system that can track eye gaze and human facial emotion.
* Backend will take the webcam or integrated camera from laptop as input source.
* Backend should be able to handle the detection task while displaying the video source from the frontend.
* Backend should be able to handle eye gaze tracking showing where the eyes are focusing on the screen in the frontend.
* Emotions should include at least 6 out of Neutral, Anger, Surprise, Sleepy, Boredom, Fearful, Distressed, Frustration, Happy, Excited, Sadness, Relax.
* Frontend should show detected face(s), expressions, and detected emotions clearly.
* Frontend should distinguish between a real face and face from a photo.
* Accuracy is not main consideration for this task.

##### Solution
Problem 2 needs multiple AI models. Basically we need models for
* `Eye Gaze Detection and Tracking`
* `Emotion Detection` (classification Model)
* `Liveliness Detection` (Classification Model)

For each of the above models, the base task is face detection. Once we detect a face we can pass it to each of the downstream task. So we can use a single model for face detection and pass it to each of the downstream task.
There are a lot of open source model for face detection (`MTCNN`, `RetinaFace` etc.) with a good accuracy. For the simplicity of the project and to run the system in near real time using laptop camera I used face detection using `Haar Cascades` from opencv. 



![](img/1.gif)
![](img/face_detection.jpg)


    cd ~/Projects/$1;

If you save it as a short name like `p`, you can just do a simple little:

    p FOSS

to get to your FOSS project. Ohhh yeahhh!

You can even make it autocomplete!

    #compdef p
    _files -W ~/Projects -/

Copyright
---------

See the LICENSE for details.
