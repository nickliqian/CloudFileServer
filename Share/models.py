from django.db import models
from datetime import datetime


class Upload(models.Model):
    # 下载次数记录
    DownloadDocount = models.IntegerField(verbose_name=u"下载次数", default=0)
    # 文件代号
    code = models.CharField(max_length=8, verbose_name=u"code")
    # 上传时间
    Datatime = models.DateTimeField(default=datetime.now)
    # 下载路径
    path = models.CharField(max_length=32, verbose_name=u"下载路径")
    # 文件名称
    name = models.CharField(max_length=32, verbose_name=u"文件名", default="")
    # 文件大小
    Filesize = models.CharField(max_length=10, verbose_name=u"文件大小")
    # IP地址
    PCIP = models.CharField(max_length=32, verbose_name=u"IP地址", default="")

    # 元选项
    class Meta():
        verbose_name = "download"
        verbose_name_plural = verbose_name
        db_table = "download"

    # 对象名称
    def __str__(self):
        return self.name
