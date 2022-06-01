FROM python:3.10

ADD . /app
WORKDIR /app

RUN \
    set -e \
    && apt update \
    && apt install libsm6 libgl1 libgl1-mesa-glx python3-pyqt5.qtwebengine python3-pyqt5.qtmultimedia -y

RUN \
    pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install .

COPY . .
CMD ["python", "-m", "kalaha", "server"]
