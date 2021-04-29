#------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#------------------------------------------------------------------------------

FROM ubuntu:18.04

ARG build_dir
ARG tfm_docker_windows_host

ENV BUILD_DIR=${build_dir}
ENV WIN_HOST=$(tfm_docker_windows_host)

ADD tfm_core_requirements_python3.txt /opt/
ADD tfm_core_dependencies.txt /opt/

COPY install/tfm_core_dependencies.install /tmp/
COPY tfm_entrypoint.sh /opt/

RUN apt-get -y update \
&& apt-get -y install \
git \
sudo \
cmake \
curl \
wget \
build-essential \
libssl-dev \
python3 \
python3-pip \
python3-crypto \
python3-dev \
dos2unix \
&& pip3 install -r /opt/tfm_core_requirements_python3.txt \
&& mkdir -p /home/buildslave/tools \
&& cd /home/buildslave/tools \
&& dos2unix /tmp/tfm_core_dependencies.install /opt/tfm_entrypoint.sh \
&& bash /tmp/tfm_core_dependencies.install \
&& chmod +x /opt/tfm_entrypoint.sh

ENTRYPOINT ["/bin/bash","/opt/tfm_entrypoint.sh"]
CMD [""]