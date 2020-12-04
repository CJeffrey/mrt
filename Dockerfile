FROM python:3

COPY dist/mrt-0.0.3-py3-none-any.whl /opt
WORKDIR /opt
RUN pip install mrt-0.0.3-py3-none-any.whl

CMD ["python", "-m", "mrt.server.mrt_server"]