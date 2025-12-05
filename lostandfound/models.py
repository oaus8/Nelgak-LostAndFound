from django.db import models
from django.contrib.auth.models import User


class LostItem(models.Model):
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Jewelry', 'Jewelry'),
        ('Clothing', 'Clothing'),
        ('Bags', 'Bags'),
        ('Keys', 'Keys'),
        ('Documents', 'Documents'),
        ('Pets', 'Pets'),
        ('Sports Equipment', 'Sports Equipment'),
        ('Other', 'Other'),
    ]

    LOCATION_CHOICES = [
        ('CCSIT Building A60', 'CCSIT Building A60'),
        ('CCSIT Building A61', 'CCSIT Building A61'),
    ]

    STATUS_CHOICES = [
        ('not_found', 'Not Found'),
        ('found', 'Found'),
    ]

    item_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    building_number = models.CharField(max_length=10, default='A60')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location_lost = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    date_lost = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_found'
    )

    college = models.CharField(
        max_length=50,
        default='CCIS',
        blank=True
    )

    reported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lost_items'
    )

    # REQUIRED security fields (no null, no blank)
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)

    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} ({self.category})"


class ClaimVerification(models.Model):
    VERIFICATION_STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    report = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='claims')
    claimer_name = models.CharField(max_length=100)
    claimer_email = models.EmailField()
    claimer_answer = models.CharField(max_length=255)
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report.item_name} – {self.verification_status}"
