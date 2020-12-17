from django.db              import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models            import User
from product.models         import Product

class Review(models.Model):
    rate                = models.FloatField(validators=[MinValueValidator(0.5),MaxValueValidator(5.0)])
    contents            = models.TextField()
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True, blank=True)
    is_monthly_reviewed = models.BooleanField(default=True)

    class Meta:
        db_table ="reviews"

class ReviewImage(models.Model):
    review    = models.ForeignKey(Review, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=200)

    class Meta:
        db_table ="review_images"

class Question(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    contents   = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "questions"

class Answer(models.Model):
    contents   = models.TextField()
    question   = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "answers"
