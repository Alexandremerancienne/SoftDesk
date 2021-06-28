from rest_framework import serializers

from todos.models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        exclude = ("created_time",)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "description", "author"]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "role"]
