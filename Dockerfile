FROM karmaresearch/wdps_assignment

USER root
RUN sudo apt install -y pipenv

USER wdps

# Copy all necessary repo files to the /app/assignment/code directory.
COPY Pipfile /app/assignment/Pipfile
COPY Pipfile.lock /app/assignment/Pipfile.lock
COPY src /app/assignment/src

RUN pipenv install
