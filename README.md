### How to build it:
1) ```docker build -t <container_name> . ```
### How to run it:
If you need a display output:
1) ```docker run --device /dev/vchiq:/dev/vchiq --privileged=True -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -it <container_name>```

If you don't need display output:
1) ```docker run --device /dev/vchiq:/dev/vchiq --privileged=True -it <container_name>```
   
Inside the container bash:
2) ```./ros_entrypoint.sh ```
3) ```roscore```
4) ```rosrun raspi_camera main.py -n <rpi_number>```

Also you need to connect to the running container (to switch a tab):
* ```docker exec -it <container_id> bash```

To set ip for multimaster:
* ```--add-host <name>:<xxx.xxx.x.xxx> --net host ```
  
It will add new hosts to /etc/hosts