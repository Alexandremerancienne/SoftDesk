from django.conf import settings
from django.db import models


class Contributor(models.Model):

    class Meta:
        verbose_name_plural = "contributors"

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    ROLE = (
        ('Author', 'Author'),
        ('Contributor', 'Contributor'),
    )

    role = models.CharField(
        max_length=100,
        choices=ROLE,
        help_text='Role (Author, Contributor)',
    )

    PERMISSIONS = (
        ('All', 'All'),
        ('Restricted', 'Restricted'),
    )

    permissions = models.CharField(max_length=100,
                                   choices=PERMISSIONS,
                                   help_text='Permissions (All, Restricted)',
                                   )

    def __str__(self):
        return self.user.username


class Project(models.Model):

    class Meta:
        verbose_name_plural = "projects"

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

    TYPE = (
        ('Back', 'Back-end'),
        ('Front', 'Front-end'),
        ('Android', 'Android'),
        ('iOS', 'iOS'),
    )

    type = models.CharField(
        max_length=50,
        choices=TYPE,
        blank=True,
        help_text='Type (Front, Back, Android, iOS)',
    )

    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)

    contributors = models.ManyToManyField(Contributor)

    def __str__(self):
        return self.title


class Issue(models.Model):

    class Meta:
        verbose_name_plural = "issues"

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

    TAG = (
        ('Bug', 'Bug'),
        ('Improvement', 'Improvement'),
        ('Task', 'Task'),
    )

    tag = models.CharField(
        max_length=50,
        choices=TAG,
        blank=True,
        help_text='Tag (Bug, Improvement, Task)',
    )

    PRIORITY = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )

    priority = models.CharField(
        max_length=50,
        choices=PRIORITY,
        blank=True,
        help_text='Priority (Low, Medium, High)',
    )

    STATUS = (
        ('Todo', 'To Do'),
        ('Ongoing', 'Ongoing'),
        ('Done', 'Done'),
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS,
        blank=True,
        help_text='Status (Todo, Ongoing, Done)',
    )

    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE)

    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               related_name='author',
                               on_delete=models.CASCADE)

    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                 related_name='assignee',
                                 on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):

    class Meta:
        verbose_name_plural = "comments"

    description = models.CharField(max_length=2000)

    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)

    issue = models.ForeignKey(Issue,
                              on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description




