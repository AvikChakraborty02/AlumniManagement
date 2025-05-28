from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
def validate_image(file):
    valid_mime_types = ['image/jpeg', 'image/png', 'image/jpg',]
    file_mime_type = file.file.content_type
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Only .png, .jpg, and .jpeg files are allowed.')

    if file.size > 1 * 1024 * 1024:  # 1MB
        raise ValidationError('File size must be less than 1MB.')
    
def validate_pdf(file):
    # Validate file type
    if not file.name.endswith('.pdf'):
        raise ValidationError('Only .pdf files are allowed.')
    
    # Validate file size (1MB = 1 * 1024 * 1024 bytes)
    if file.size > 1 * 1024 * 1024:
        raise ValidationError('File size must be less than 1MB.')

class OTP(models.Model):
    email=models.EmailField(primary_key=True,max_length=100)
    otp=models.IntegerField()

class Coordinator(models.Model):
    id=models.AutoField(primary_key=True)
    fullname=models.CharField(max_length=70)
    email=models.EmailField(unique=True,null=False,max_length=100)
    password=models.CharField(max_length=30)

class Application(models.Model):
    #Personal Details
    application_id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=70)
    dob=models.DateField()
    phno=models.BigIntegerField(unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    #Educational Details
    profile_picture=models.ImageField(null=True,blank=True,upload_to='images/',validators=[validate_image])
    qualification=models.CharField(max_length=50)
    course=models.CharField(max_length=50)
    year_of_passing=models.IntegerField()
    percentage=models.IntegerField()
    certificate=models.FileField(null=True,blank=False,upload_to='certificates/', validators=[validate_pdf])
    #Work Experience
    organization_name=models.CharField(max_length=50)
    doj_month=models.IntegerField()
    doj_year=models.IntegerField()
    job_profile=models.CharField(max_length=50)
    job_location=models.CharField(max_length=50)
    linked_in_url=models.URLField()

class Alumni(models.Model):
    #Personal Details
    alumni_id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=70)
    dob=models.DateField()
    phno=models.BigIntegerField(unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    #Educational Details
    profile_picture=models.ImageField(null=True,blank=True,upload_to='images/',validators=[validate_image])
    qualification=models.CharField(max_length=50)
    course=models.CharField(max_length=50)
    year_of_passing=models.IntegerField()
    percentage=models.IntegerField()
    certificate=models.FileField(null=True,blank=False,upload_to='certificates/', validators=[validate_pdf])
    #Work Experience
    organization_name=models.CharField(max_length=50)
    doj_month=models.IntegerField()
    doj_year=models.IntegerField()
    job_profile=models.CharField(max_length=50)
    job_location=models.CharField(max_length=50)
    linked_in_url=models.URLField()

class Posts(models.Model):
    post_id=models.BigAutoField(primary_key=True)
    email= models.EmailField()
    posted_on=models.DateField()
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=3000)
    link1=models.URLField(null=True)
    link2=models.URLField(null=True)
    link3=models.URLField(null=True)

class Events(models.Model):
    event_id=models.BigAutoField(primary_key=True)
    description=models.CharField(max_length=200)
    posted_on=models.DateField()
    is_new=models.CharField(max_length=3)
    event=models.FileField(null=True,blank=False,upload_to='events/',validators=[validate_pdf])

class Transactions(models.Model):
    id=models.BigAutoField(primary_key=True)
    email=models.EmailField()
    order_id=models.CharField(max_length=3000)
    payment_id=models.CharField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    amount=models.BigIntegerField()
    status=models.CharField(max_length=10,default='Failure')

