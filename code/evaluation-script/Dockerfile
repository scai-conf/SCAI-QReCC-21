FROM nvidia/cuda:11.3.1-base

RUN apt update && apt install -y \
    python3-pip

RUN mkdir /app
WORKDIR /app
ADD scai-qrecc21-evaluator.py /app
ADD requirements.txt /app

RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm
RUN pip3 install torch==1.9.1+cu111 -f https://download.pytorch.org/whl/torch_stable.html
