# base image
FROM ubuntu

# ubuntu installing - python, pip, graphviz
RUN apt-get update &&\
    apt-get install python3-setuptools -y&&\
    apt-get install python3-pip -y &&\
    apt-get install graphviz -y && \
    apt-get install --upgrade cython3 -y

# exposing default port for streamlit
EXPOSE 8501

# Make a directory of the app
WORKDIR /trivia-streamlit-app/

# copy over requirements
COPY requirements.txt ./requirements.txt

# install pip then packages
RUN pip3 install -r requirements.txt

# copying all files over
COPY streamlit_trivia_app.py ./streamlit_trivia_app.py

# cmd to launch the app when the container is run
CMD streamlit run streamlit_trivia_app.py

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'
