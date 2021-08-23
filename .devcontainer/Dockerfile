# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.166.1/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version: bionic, focal
ARG VARIANT="focal"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# アップデート
RUN sudo apt-get update
 
# JDKインストール
RUN sudo apt-get install -y openjdk-8-jdk
 
# Sparkインストール　※リンクが消えていることがある。その時は、http://ftp.riken.jp/net/apache/spark/にアクセスしてバージョンを確認し、指定を変える。
RUN wget http://ftp.riken.jp/net/apache/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz
RUN tar zxvf spark-3.1.1-bin-hadoop3.2.tgz
RUN sudo mv spark-3.1.1-bin-hadoop3.2 /usr/local/
RUN sudo ln -s /usr/local/spark-3.1.1-bin-hadoop3.2 /usr/local/spark

# pipのインストール
RUN sudo apt install -y python3-pip
 
# jupyter-notebookをインストール
RUN sudo apt install -y jupyter-notebook

# 環境変数の設定
ENV SPARK_HOME /usr/local/spark 
ENV PATH $PATH:$SPARK_HOME/bin
ENV PYSPARK_PYTHON /usr/bin/python3
ENV PYSPARK_DRIVER_PYTHON jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS 'notebook --ip=0.0.0.0 --NotebookApp.token='
