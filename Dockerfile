FROM karmaresearch/wdps_assignment

USER root
RUN sudo apt install -y pipenv

USER wdps

# Copy all necessary repo files
COPY requirements.txt /app/assignment/requirements.txt
COPY src /app/assignment/src

RUN pip install -r requirements.txt
