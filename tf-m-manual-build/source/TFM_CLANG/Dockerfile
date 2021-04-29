#------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#------------------------------------------------------------------------------

FROM tfm_core:latest

ARG  license
ARG  build_dir

ENV ARMLMD_LICENSE_FILE=${license}
ENV BUILD_DIR=${build_dir}
ENV PATH=/home/buildslave/tools/ARM_CLANG/bin:${PATH}

ADD tfm_clang_dependencies.txt /opt/

COPY install/tfm_clang_dependencies.install /tmp/
COPY tfm_entrypoint.sh /opt/

RUN dos2unix /tmp/tfm_clang_dependencies.install /opt/tfm_entrypoint.sh \
&& bash -ex /tmp/tfm_clang_dependencies.install \
&& chmod +x /opt/tfm_entrypoint.sh

ENTRYPOINT ["/bin/bash","/opt/tfm_entrypoint.sh"]
CMD [""]