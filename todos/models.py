from django.db import models

from accounts.models import Users


class Projects(models.Model):

    """A class to represent projects.
    Attributes:
    - Title;
    - Description;
    - Type (back-end, front-end, iOS, Android);
    - Issues reported for this project;
    - Author User ID"""

    class Meta:
        verbose_name_plural = "projects"

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

    TYPE = (
        ('back', 'Back-end'),
        ('front', 'Front-end'),
        ('android', 'Android'),
        ('ios', 'iOS'),
    )

    type = models.CharField(
        max_length=50,
        choices=TYPE,
        blank=True,
        help_text='Type (front, back, android, ios)',
    )

    author_user_id = models.ManyToManyField(Users,
                                            through='Contributors')

    def __str__(self):
        return self.title


class Issues(models.Model):

    """A class to represent project issues.
    Attributes:
    - Title;
    - Tag (bug, improvement, task);
    - Priority (low, medium, high);
    - Status (To do, ongoing, done);
    - Author User ID;
    - Assignee User ID;
    - Date of creation"""

    class Meta:
        verbose_name_plural = "issues"

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

    TAG = (
        ('bug', 'Bug'),
        ('improvement', 'Improvement'),
        ('task', 'Task'),
    )

    tag = models.CharField(
        max_length=50,
        choices=TAG,
        blank=True,
        help_text='Tag (bug, improvement, task)',
    )

    PRIORITY = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    priority = models.CharField(
        max_length=50,
        choices=PRIORITY,
        blank=True,
        help_text='Priority (low, medium, high)',
    )

    STATUS = (
        ('todo', 'To Do'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS,
        blank=True,
        help_text='Status (todo, ongoing, done)',
    )

    assignee_user_id = models.ForeignKey(Users,
                                         on_delete=models.SET_NULL,
                                         null=True)

    project_id = models.ForeignKey(Projects,
                                   on_delete=models.SET_NULL,
                                   null=True)

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comments(models.Model):

    """A class to represent issue comments.
    Attributes:
    - Description;
    - Author User ID;
    - Issue ID;
    - Date of creation"""

    class Meta:
        verbose_name_plural = "comments"

    description = models.CharField(max_length=2000)

    author_user_id = models.ForeignKey(Users,
                                       on_delete=models.SET_NULL,
                                       null=True)

    issue_id = models.ForeignKey(Issues,
                                 on_delete=models.SET_NULL,
                                 null=True)

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Contributors(models.Model):

    """A class to represent contributors.
    Attributes:
    - User ID;
    - Project ID;
    - Role (Author, Contributor, Other);
    - Permission (Allowed, None)"""

    class Meta:
        verbose_name_plural = "contributors"

    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)

    ROLE = (
        ('author', 'Author'),
        ('contributor', 'Contributor'),
        ('other', 'Other'),
    )

    role = models.CharField(
        max_length=100,
        choices=ROLE,
        help_text='Role (author, contributor, other)',
    )

    PERMISSIONS = (
        ('allowed', 'allowed'),
        ('none', 'None'),
    )

    permissions = models.CharField(max_length=100,
                                   choices=PERMISSIONS,
                                   help_text='Permissions (allowed, none)',
                                   )

    def __str__(self):
        return f'Contributor {self.project_id}: {self.user_id}'
