FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#RUN pip install -U g4f
RUN pip install g4f==0.2.0.2


# Install Chrome and Chromedriver
RUN apt-get update && \
    apt-get install -y \
        chromium \
        chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chromedriver
ENV CHROMEDRIVER_PATH /usr/lib/chromium/chromedriver
ENV CHROME_BIN /usr/bin/chromium-browser


# Install Pandoc
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
	texlive-xetex \
	lmodern \
	texlive-fonts-recommended \
	texlive-fonts-extra \
    && rm -rf /var/lib/apt/lists/*


# Install Pandoc
RUN wget https://github.com/jgm/pandoc/releases/download/2.14/pandoc-2.14-1-amd64.deb && \
    dpkg -i pandoc-2.14-1-amd64.deb && \
    rm pandoc-2.14-1-amd64.deb

RUN pandoc --version


# Install Amiri font
RUN wget https://github.com/alif-type/amiri-font/archive/refs/tags/1.000.zip && \
    unzip 1.000.zip -d /usr/share/fonts/ && \
    fc-cache -fv && \
    rm 1.000.zip


# Install Eisvogel template
RUN wget https://github.com/Wandmalfarbe/pandoc-latex-template/releases/download/v2.0.0/Eisvogel-2.0.0.tar.gz && \
    tar -xzvf Eisvogel-2.0.0.tar.gz && \
    mkdir -p /usr/share/pandoc/templates/ && \
    mv eisvogel.latex /usr/share/pandoc/templates/ && \
    rm -rf Eisvogel-2.0.0.tar.gz


# Create a user
RUN useradd -m -u 1000 user

USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app
USER root
RUN chown -R user /usr/bin/chromedriver

# Switch back to the non-root user
USER user
CMD [ "python", "randai/manage.py", "runserver", "0.0.0.0:7860", "--settings=randai.settings" ]
