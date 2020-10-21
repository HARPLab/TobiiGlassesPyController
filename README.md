# TobiiGlassesPyController: A Python controller for Tobii Pro Glasses 2

The TobiiGlassesPyController is an open-source controller for accessing eye-tracking data and for managing recordings,
participants and calibrations using the mobile Tobii Pro Glasses 2 eye-tracker.
The controller is based on the [Tobii Pro Glasses 2 API](https://www.tobiipro.com/product-listing/tobii-pro-glasses-2-sdk/).

### ROS data collection branch
This branch is for using the Tobii eye tracker in online streaming mode with ROS. This branch contains publishers for the ego-centric video feed and associated `vts` timestamps for video frames.

One diffculty is that to get the `vts` timestamps, we must use PyAV (only compatible with Python3) while a lot of lab ROS infrastructure is based on ROS kinetic (doesn't support Python3). Currently we use `imagezmq` for sending frames and timestamps from PyAV reader (Python3) to a [publisher](https://github.com/ajdroid/tobii_ros/blob/master/gaze_api/scripts/vidPub.py) (Python2)

### Future TODOs
- [ ] C++ publisher for video
- [ ] in-proc communication via subprocess for imgzmq communication
- [ ] change imagezmq transport to `ipc` http://api.zeromq.org/2-1:zmq-ipc


# Citation

Davide De Tommaso and Agnieszka Wykowska. 2019. TobiiGlassesPySuite: An open-source suite for using the Tobii Pro Glasses 2 in eye-tracking studies. In 2019 Symposium on Eye Tracking Research and Applications (ETRA ’19), June 25–28, 2019, Denver , CO, USA. ACM, New York, NY, USA, 5 pages. https://doi.org/10.1145/3314111.3319828


```
@inproceedings{DeTommaso:2019:TOS:3314111.3319828,
 author = {De Tommaso, Davide and Wykowska, Agnieszka},
 title = {TobiiGlassesPySuite: An Open-source Suite for Using the Tobii Pro Glasses 2 in Eye-tracking Studies},
 booktitle = {Proceedings of the 11th ACM Symposium on Eye Tracking Research \& Applications},
 series = {ETRA '19},
 year = {2019},
 isbn = {978-1-4503-6709-7},
 location = {Denver, Colorado},
 pages = {46:1--46:5},
 articleno = {46},
 numpages = {5},
 url = {http://doi.acm.org/10.1145/3314111.3319828},
 doi = {10.1145/3314111.3319828},
 acmid = {3319828},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {Tobii Pro Glasses 2, eye-tracking, human-computer interaction, open-source, wearable computing, wearable eye-tracker},
} 
```


