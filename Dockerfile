FROM debian@sha256:a9c958be96d7d40df920e7041608f2f017af81800ca5ad23e327bc402626b58e

USER root

# Install all OS dependencies for fully functional notebook server
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -yq --no-install-recommends \
    git \
    vim \
    jed \
    emacs \
    wget \
    build-essential \
    python-dev \
    ca-certificates \
    bzip2 \
    unzip \
    libsm6 \
    pandoc \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    sudo \
    locales \
    libxrender1 \
    nano \
    openssh-server \
    mysql-server mysql-client libmysqlclient-dev \
    php5 libapache2-mod-php5 php5-mcrypt \
    fasttree

RUN mkdir /var/run/sshd

RUN mysqld &
RUN service mysql start

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.9.0/tini && \
    echo "faafbfb5b079303691a939a747d7f60591f2143164093727e870b289a44d9872 *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

# Configure environment
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
ENV SHELL /bin/bash
ENV NB_USER pa
ENV NB_UID 1000
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Create user with UID=1000 and in the 'users' group
RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    mkdir -p /opt/conda && \
    chown pa /opt/conda

USER pa

# Setup home directory
RUN mkdir /home/$NB_USER/work && \
    mkdir /home/$NB_USER/.jupyter && \
    mkdir /home/$NB_USER/.local && \
    echo "cacert=/etc/ssl/certs/ca-certificates.crt" > /home/$NB_USER/.curlrc

# Install conda
RUN cd /tmp && \
    mkdir -p $CONDA_DIR && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-3.19.0-Linux-x86_64.sh && \
    echo "9ea57c0fdf481acf89d816184f969b04bc44dea27b258c4e86b1e3a25ff26aa0 *Miniconda3-3.19.0-Linux-x86_64.sh" | sha256sum -c - && \
    /bin/bash Miniconda3-3.19.0-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-3.19.0-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda install --quiet --yes conda==3.19.1 && \
    $CONDA_DIR/bin/conda config --system --add channels conda-forge && \
    conda clean -tipsy

# Install Jupyter
RUN conda install --quiet --yes \
    'notebook=4.1*' \
    terminado \
    && conda clean -tipsy

# Install JupyterHub to get the jupyterhub-singleuser startup script
RUN pip install 'jupyterhub==0.5'

USER root

RUN pip install biopython \
&& conda install basemap \
&& pip install pandas

RUN pip install scipy

RUN pip install PyMySQL \
&& pip install termcolor

RUN pip install -U scikit-learn

RUN pip install xlrd

#RUN pip install cpickle

EXPOSE 3306
RUN ls
# Configure container startup as root
EXPOSE 8888
WORKDIR /home/$NB_USER/work
ENTRYPOINT ["tini", "--"]
CMD ["start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
# Start notebook server
COPY start-notebook.sh /usr/local/bin/
# Start single-user notebook server for use with JupyterHub
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /home/$NB_USER/.jupyter/
RUN chown -R $NB_USER:users /home/$NB_USER/.jupyter

ADD muscle3.8.31_i86linux64 ./


ADD sea.sql /tmp/sea.sql

