from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg

from extra_apps.DjangoUeditor.models import UEditorField

DEGREE_CHOICES = (("cj", "初级"), ("zj", "中级"), ("gj", "高级"))


class Course(BaseModel):
    """
    讲师
    """
    teacher = models.ForeignKey(Teacher, verbose_name="讲师", on_delete=models.CASCADE)
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True, on_delete=models.CASCADE,)
    name = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述", max_length=300)
    learn_times = models.IntegerField(verbose_name="学习时长(分钟数)", default=0,)
    degree = models.CharField(verbose_name="难度", choices=DEGREE_CHOICES, max_length=2)
    students = models.IntegerField(verbose_name='学习人数', default=0,)
    fav_nums = models.IntegerField(verbose_name='收藏人数', default=0, )
    click_nums = models.IntegerField(verbose_name="点击数", default=0,)
    notice = models.CharField(verbose_name="课程公告", max_length=300, default="")
    category = models.CharField(verbose_name="课程类别", default="公开课", max_length=20, )
    tag = models.CharField(verbose_name="课程标签", default="", max_length=10)
    youneed_know = models.CharField(verbose_name="课程须知", default="", max_length=300, )
    teacher_tell = models.CharField(verbose_name="老师告诉你", default="", max_length=300, )
    is_classics = models.BooleanField(verbose_name="是否经典", default=False, )
    detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath="courses/ueditor/images/",
                          filePath="courses/ueditor/files/", default="")
    is_banner = models.BooleanField(verbose_name="是否广告位", default=False, )
    image = models.ImageField(verbose_name="封面图", upload_to="courses/%Y/%m", max_length=100)

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name
        db_table = "course"

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()

    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<img src='{}'>".format(self.image.url))
    show_image.short_description = "图片"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/course/{}'>跳转</a>".format(self.id))
    go_to.short_description = "跳转"


class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True


class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    tag = models.CharField(max_length=100, verbose_name="标签")

    class Meta:
        verbose_name = "课程标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    url = models.CharField(max_length=1000, verbose_name=u"访问地址")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="下载地址", max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
