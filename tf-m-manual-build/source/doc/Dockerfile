#------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#------------------------------------------------------------------------------

FROM tfm_core

ARG docs_dir

ENV DEBIAN_FRONTEND=noninteractive
ENV DOCS_DIR=${docs_dir}
ENV PLANTUML_JAR_PATH=/home/buildslave/tools/plantuml.jar

ADD tfm_docs_requirements_python3.txt /opt/
ADD tfm_docs_dependencies.txt /opt/

COPY install/tfm_docs_dependencies.install /tmp/
COPY tfm_entrypoint.sh /opt/

RUN apt-get -y update \
&& apt-get -y install \
doxygen \
graphviz \
default-jre \
texlive-latex-extra \
&& pip3 install -r /opt/tfm_docs_requirements_python3.txt \
&& dos2unix /tmp/tfm_docs_dependencies.install /opt/tfm_entrypoint.sh \
&& bash -ex /tmp/tfm_docs_dependencies.install \
&& chmod +x /opt/tfm_entrypoint.sh

ENTRYPOINT ["/bin/bash","/opt/tfm_entrypoint.sh"]
CMD [""]