FROM python:3.8-buster
# Create app directory
WORKDIR /usr/src/configs

# Install app dependencies
COPY . .

RUN rm /usr/src/configs/static/anomalies.json
RUN rm /usr/src/configs/static/mychart.png

RUN ["pip3", "install", "-U","flask"]
RUN ["pip3", "install", "-U","requests"]
RUN ["pip3", "install", "-U","bigml"]
RUN ["pip3", "install", "-U","quickchart.io"]
RUN ["chmod", "+x", "./start.sh"]
CMD ["./start.sh"]
