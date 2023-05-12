FROM python:3.8

#RUN useradd user

COPY ./ /platoe/

RUN chmod +x /platoe/scripts/*

WORKDIR /platoe/

RUN pip install -r requirements.txt

#USER user

ENV PATH="/platoe/scripts/:${PATH}"

EXPOSE 8000

CMD ["entrypoint.sh"]
