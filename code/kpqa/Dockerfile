FROM nvidia/cuda:11.3.1-base

RUN apt update && apt install -y \
    git \
    python3-pip \
    unzip

RUN mkdir /app
WORKDIR /app
RUN git clone https://github.com/hwanheelee1993/KPQA.git
WORKDIR /app/KPQA
RUN git checkout bb4b0a5
ADD KPQA.diff .
RUN git apply KPQA.diff
ADD ckpt.zip .
RUN unzip ckpt.zip
RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader stopwords
# RUN python3 compute_KPQA.py --model_path . --num_ref 1 --data sample.csv --out_file result-new.csv
ENTRYPOINT python3 compute_KPQA.py --model_path . 
