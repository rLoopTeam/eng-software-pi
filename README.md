# eng-software-pi
eng-software team repo for raspberry pi code

ZMQ Instructions

1. Download the tarball from zeromq.org/areadownload
2. Follow their guide
3. Use ./configure --without-libsodium to skip the annoyance (We don't need it at this point)

For Python

4. install pip if not already there
5. use pip install pyzmq to get the language binding

For C++

6. git clone https://github.com/zeromq/cppzmq
7. move the two .hpp files to /usr/local/include
8. compile your .cpp with the -lzmq flag
