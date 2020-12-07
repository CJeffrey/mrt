FROM python:3

COPY dist/mrt-0.1.0-py3-none-any.whl /opt
WORKDIR /opt
RUN pip install mrt-0.1.0-py3-none-any.whl
ENTRYPOINT ["mrt"]