FROM karmaresearch/wdps_assignment

USER root
RUN sudo apt install -y libcairo2-dev

USER wdps
WORKDIR /app/assignment

# Copy all necessary repo files
COPY requirements.txt /app/assignment/requirements.txt
COPY src /app/assignment/src

RUN pip3 install -r requirements.txt

# Install nltk data
RUN python3 -m nltk.downloader all
