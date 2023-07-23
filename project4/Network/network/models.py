from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image


# Allow pre-existing User model to have profile-picture functionality
class User(AbstractUser):
    pfp = models.ImageField(blank=False, null=True, upload_to='pfp/')

    # Reduce size of saved image
    def save(self, *args, **kwargs):
        super().save()  # saving image first
        
        # Checking first whether the user uploaded a profile pic or not
        if (self.pfp):
            img = Image.open(self.pfp.path) # Open image using self

            
            x = 0
            if img.height > 600 or img.width > 600:
                if img.height > img.width :
                    x = img.height/600
                else:
                    x = img.width/600
                new_img = (img.height/x, img.width/x)
                img.thumbnail(new_img)
                img.save(self.pfp.path)  # saving image at the same path


# Data associated with every post 
class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(blank=False, null=True, upload_to="posts/")
    info = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

    # Reduce size of saved image
    def save(self, *args, **kwargs):
        super().save()  # saving image first
        
        # Check first whether the user uploaded an image or not
        if(self.image):
            img = Image.open(self.image.path) # Open image using self

            x = 0
            if img.height > 1200 or img.width > 1200:
                if img.height > img.width :
                    x = img.height/1200
                else:
                    x = img.width/1200
                new_img = (img.height/x, img.width/x)
                img.thumbnail(new_img)
                img.save(self.image.path)  # saving image at the same path
            
    def __str__(self):
        return f"{self.id}: {self.content} by {self.owner} with {self.image} on {self.info}"

# Like data of who liked what
class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker")
    liked = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked")

# Follow data of who follows whom
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows")

    # Function to validate whether a user folllows themselves
    def clean(self):
        if self.follower == self.follows:
            raise ValidationError("Users can't follow themselves")

    # Validate before saving
    def save(self, *args, **kwargs):
        
        # Running full_clean to validate before saving
        self.full_clean()
        super().save(*args, **kwargs)