FROM ubuntu:20.04
SHELL ["/bin/bash", "-c"]

RUN mkdir /code
WORKDIR /code

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install --yes     \
	build-essential       \
	cython3               \
	doxygen               \
	git                   \
	gfortran              \
	libblitz0-dev         \
	libboost-filesystem1.71-dev \
	libhdf5-dev           \
	libsaxonhe-java       \
	openjdk-8-jre-headless\
	openjdk-8-jdk-headless\
	pkg-config            \
	python3               \
	python3-setuptools    \
	python3-numpy         \
	python3-pip           \
	python3-wheel         \
	python-is-python3     \
	xsltproc              \
	automake              \
	flex                  \
	bison                 \
	gperf                 \
	libxml2-dev           \
	libreadline-dev       \
	libmotif-dev          \
	rsync

RUN apt-get clean all

RUN git clone -b stable_release-7-84-8 --depth 1 https://github.com/MDSplus/mdsplus.git

RUN cd mdsplus && \
    ./bootstrap && \
    mkdir build && \
    cd build && \
    ../configure --prefix=/usr && \
    make && \
    make install

ENV MDSPLUS_DIR /usr

COPY access-layer access-layer
COPY data-dictionary data-dictionary

ENV CLASSPATH /usr/share/java/Saxon-HE.jar:/usr/java/classes/jTraverser.jar
ENV SAXONJARFILE Saxon-HE.jar
ENV HDF5_DIR /usr/lib/x86_64-linux-gnu/hdf5/serial

ENV IMAS_INSTALL_DIR /usr
ENV IMAS_VERSION 3.34.0

ENV IMAS_UDA no
ENV IMAS_JAVA no
ENV IMAS_MATLAB no
ENV IMAS_MEX no

RUN cd data-dictionary && make install

RUN ln -s /usr/include /code/access-layer/xml

RUN cd access-layer && make -j12
RUN cd access-layer && make install

RUN cd access-layer/pythoninterface/imasloader && \
    python -m pip install .

RUN rm -r access-layer data-dictionary

ENV IMAS_PREFIX /usr

RUN python -c "import imas; print(imas.names[0])"

RUN python -m pip install ipsframework

COPY IPS/* ./

RUN gfortran -I${IMAS_PREFIX}/include/gfortran -o imas imas.f90 -L${IMAS_PREFIX}/lib -limas-gfortran

CMD ["bash", "-c", "ips.py --config=ips.imas.config --platform=platform.conf"]
