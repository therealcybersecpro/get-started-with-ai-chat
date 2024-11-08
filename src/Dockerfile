# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /code

COPY requirements.txt .

#Remove in production
ADD api api

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 50505

CMD ["gunicorn", "api.main:app"]

# Configure the IPython kernel
#RUN ipython kernel install --name "python3" --user

# Install daily version of azd for latest changes
# See: https://github.com/Azure/azure-dev/tree/main/cli/installer#download-from-daily-builds
RUN curl -fsSL https://aka.ms/install-azd.sh | bash -s -- --version daily