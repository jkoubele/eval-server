FROM quay.io/jupyter/r-notebook:2026-03-02

USER root
RUN mamba install -y -c conda-forge r-jsonlite r-rjson r-argparse r-gmp && \
    mamba clean -afy
USER ${NB_UID}