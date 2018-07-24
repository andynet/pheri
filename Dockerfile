FROM ubuntu:latest
MAINTAINER Andrej Baláž <andrejbalaz001@gmail.com>

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install software
## Install prokka, blastp, python and other dependencies
RUN apt-get update
RUN apt-get install -y make git python3-pip libdatetime-perl libxml-simple-perl libdigest-md5-perl bioperl default-jre
RUN cpan Bio::Perl
RUN git clone https://github.com/tseemann/prokka.git $HOME/prokka
RUN $HOME/prokka/bin/prokka --setupdb
RUN pip3 install sklearn pandas numpy scipy
