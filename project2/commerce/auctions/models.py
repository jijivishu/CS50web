from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class List(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=200)
    min_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_link = models.URLField( blank="true" )
    status = models.BooleanField(default=True)
    listed_on = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lists")

    def __str__(self):
        return f"{self.id}: {self.title} by {self.owner} with {self.min_bid} listed price. Currently {self.status}"

class Comment(models.Model):
    title = models.ForeignKey(List, on_delete=models.CASCADE, related_name="com_title")
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    comment = models.TextField(max_length=200)
    comment_time = models.DateTimeField()

    def __str__(self):
        return f"Comment id {self.id} was {self.commentator} commenting on {self.title}"
    
class Watchlist(models.Model):
    holder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="holder")
    holding = models.ForeignKey(List, on_delete=models.CASCADE, related_name="holding")

    def __str__(self):
        return f"{self.holder} has {self.holding} in watchlist"

class Category(models.Model):
    post = models.ForeignKey(List, on_delete=models.CASCADE, related_name="cat_post")
    category = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.post} falls in {self.category} category"

class Bid(models.Model):
    post = models.ForeignKey(List, on_delete=models.CASCADE, related_name="bid_post")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bidder} has bid of {self.bid} on {self.post}"