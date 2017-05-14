FROM docker.io/mrjogo/scrapy 
ENV PATH /usr/local/bin:$PATH
ENV PATH /home:$PATH
ADD . /home
WORKDIR /home
RUN pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
CMD python ipproxytool.py