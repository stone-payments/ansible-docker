#!/bin/bash
while [ ! -S /var/run/docker.sock ]; do sleep 1; done
chown root.docker /var/run/docker.sock
echo Fixed Docker group!
exit 0
