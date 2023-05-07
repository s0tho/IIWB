FROM nikolaik/python-nodejs

ARG BOT_TOKEN
ENV BOT_TOKEN=$BOT_TOKEN
# Add a work directory
WORKDIR /bot
# Cache and Install dependencies
COPY . .
RUN npm install -g nodemon
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Expose port
EXPOSE 3434
# Start the app
# CMD [ "nodemon", "run.py" ]