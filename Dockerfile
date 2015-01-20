FROM python:2.7

# Install Virtuoso
RUN \
	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y virtuoso-opensource && \
	rm -rf /var/lib/apt/lists/*

# Configure Virtuoso for 4GB of memory
RUN \
  sed -i "s/^\(NumberOfBuffers\s*= \)[0-9]*/\1340000/" /etc/virtuoso-opensource-6.1/virtuoso.ini && \
  sed -i "s/^\(MaxDirtyBuffers\s*= \)[0-9]*/\1250000/" /etc/virtuoso-opensource-6.1/virtuoso.ini

# Copy Python app
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

# Expose Virtuoso ports
EXPOSE 8890 1111

# Set command to run Virtuoso
CMD ./run.sh
