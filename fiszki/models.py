from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta

class FlashcardSet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcard_sets')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Flashcard(models.Model):
    set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name='flashcards')
    question = models.TextField()
    answer = models.TextField()
    next_review = models.DateTimeField(default=now)
    interval = models.IntegerField(default=1)
    ease_factor = models.FloatField(default=2.5)
    repetitions = models.IntegerField(default=0)

    def schedule_next_review(self, quality):
        if quality < 3:
            self.repetitions = 0
            self.interval = 1
        else:
            self.repetitions += 1
            self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
            if self.repetitions == 1:
                self.interval = 1
            elif self.repetitions == 2:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)
        self.next_review = now() + timedelta(days=self.interval)
        self.save()
