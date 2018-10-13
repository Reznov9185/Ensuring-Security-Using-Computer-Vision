# Ensuring Security with Computer Vision

Architecture
![System Architecture](https://drive.google.com/file/d/0BxRmf_2nNqHOVWwtRk9DeUZwdTg/view?usp=sharing)

In our implementation, we have used devices and computers which are general in terms
of computation, performance and efficiency. The results would be more satisfactory if
devices and computers with higher computational ability could be used. In the next
iteration, such devices can be used. Considering computation for better computational
time and efficiency, we could reduce the number of recognition performed on the same
person while they are in our observation window. We can achieve this by tracking a
recognized person while they are in our observation window.
We have proposed and implemented a security system considering the scenario of an
organizational security. Our aim was to derive data in real time so that extracted data
can be helpful as a tool to ensure and enhance security.

Programming Language and modules:

Language: Python .

Modules: OpenCV, imutils, datetime, MySQLdb, Image from PIL, OS, numpy.

Database:

Database: mysql server version- 5.5.46.

Algorithms

Training:

1. Haar Cascade frontal face classifier
2. Local Binary Pattern Histogram.

Motion detecting:

1. Background subtraction
2. Dilate
3. Find Contour

Face recognition:

1. Haar Cascade frontal face classifier
2. Predict with Local Binary Pattern Histogram.
