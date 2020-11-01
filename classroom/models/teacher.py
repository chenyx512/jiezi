from django.db import models

from accounts.models import User
from jiezi.utils.mixins import StrDefaultReprMixin


class Teacher(StrDefaultReprMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='teacher')
    school = models.CharField(max_length=200, blank=True,
        help_text=""" Please enter your school name, region, and country. E.g.
        "St. Mark's School, Massachusetts, United States." """)
    school_description = models.TextField(max_length=2000, blank=True,
        verbose_name="Your curriculum",
        help_text="""Please describe the textbook / curriculum you use. E.g. 
        “Integrated Chinese,” “HSK Standard Course,” or “a self-written IB 
        curriculum.” You may also add any other relevant information.""")
    wechat_id = models.CharField(max_length=40, blank=True,
        verbose_name="Wechat account id",
        help_text="Optional. Used for us to contact you, if you’d like.")

    @property
    def display_name(self):
        return self.user.display_name

    def __repr__(self):
        return f"<teacher {self.display_name}>"

    @classmethod
    def of(cls, user):
        """convenient get_or_create"""
        return cls.objects.get_or_create(user=user)[0]
