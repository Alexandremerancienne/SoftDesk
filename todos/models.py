from django.conf import settings
from django.db import models


class Project(models.Model):
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

    def __str__(self):
        return self.title


class Contributor(models.Model):

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

    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} ({self.project.title})'


class Issue(models.Model):

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

    description = models.CharField(max_length=2000)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue,
                              on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description




