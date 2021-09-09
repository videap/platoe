FROM python:3

RUN useradd user


RUN mkdir -p ./vol/media
RUN mkdir -p ./vol/static
RUN mkdir ./platoe

RUN chown -R user:user /vol
RUN chown -R 755 /vol

RUN chown -R user:user /platoe
RUN chown -R 755 /platoe



COPY ./ /platoe/

RUN chmod +x /platoe/scripts/*

WORKDIR /platoe/

RUN pip install -r requirements.txt

#USER user

ENV PATH="/platoe/scripts/:${PATH}"

CMD ["entrypoint.sh"]
