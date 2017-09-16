from django.db import models

# Basic resort model
class Resort(models.Model):

    # Basic resort information
    name = models.CharField(max_length=200, default = '')
    address = AddressField(blank = True)
    website = models.URLField(default = '')

    # Prices for lift and rentals
    adult_lift_ticket = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    combo_rental = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)

    # Season information
    opening_date = models.DateField(auto_now = True)

    # Slope information
    num_slopes = models.IntegerField(default = 0)
    num_beginner = models.IntegerField(default = 0)
    num_intermediate = models.IntegerField(default = 0)
    num_advanced = models.IntegerField(default = 0)
    num_expert = models.IntegerField(default = 0)
    num_terrain = models.IntegerField(default = 0)

    # Short 'our take' description
    our_take = models.CharField(max_length = 1000, default = "This resort is great! Yay, skiing!")

    def __str__(self):
        return self.name

