# Base image
FROM skprot/picamera_ros_kinetic:master

# The default shell is sh, switching to bash makes it easier to work with ros
SHELL ["/bin/bash", "-c"]

# Set the environment variables
ENV READTHEDOCS True \
    CATKIN_WS=/root/catkin_ws \
    PKG_CONFIG_PATH=/opt/ros/melodic/lib/pkgconfig \
    ROS_PACKAGE_PATH=/opt/ros/melodic/share \
    ROS_ETC_DIR=/opt/ros/kinetic/etc/ros \
    CMAKE_PREFIX_PATH=/opt/ros/melodic \
    PYTHONPATH=/opt/ros/melodic/lib/python3/dist-packages \
    LD_LIBRARY_PATH=/opt/ros/melodic/lib \
    PATH=/opt/ros/melodic/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    ROS_ROOT=/opt/ros/melodic/share/ros


RUN mkdir -p $CATKIN_WS/src && \
	mkdir $CATKIN_WS/src/raspi_camera


COPY ros_package_files/ $CATKIN_WS/src/raspi_camera
COPY scripts/ $CATKIN_WS/src/raspi_camera


RUN source /opt/ros/kinetic/setup.bash && \
	cd $CATKIN_WS/src && \
	catkin_init_workspace && \
	cd $CATKIN_WS && \
	catkin_make && \
	source $CATKIN_WS/devel/setup.bash && \
	echo "source $CATKIN_WS/devel/setup.bash" >> ~/.bashrc && \
	chmod +x $CATKIN_WS/src/raspi_camera/main.py


# Source ros package from entrypoint
RUN sed --in-place --expression \
      '$isource "$CATKIN_WS/devel/setup.bash"' \
      /ros_entrypoint.sh

