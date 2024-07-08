FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies required for libpostal
RUN apt-get update && apt-get install -y \
    curl \
    autoconf \
    automake \
    libtool \
    python3-dev \
    pkg-config \
    git \
    build-essential

# Clone and build libpostal
RUN git clone https://github.com/openvenues/libpostal \
    && cd libpostal \
    && ./bootstrap.sh \
    && ./configure --datadir=/var/libpostal_data \
    && make -j4 \
    && make install \
    && ldconfig

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ./main.py /usr/src/app/main.py
COPY ./util/mappings.py /usr/src/app/util/mappings.py
COPY ./util/get_env.py /usr/src/app/util/get_env.py

# Make port 80 available to the world outside this container
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
