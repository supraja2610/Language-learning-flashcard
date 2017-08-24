from django.db import models
from django.contrib.auth.models import User

# User for membership
# class User(models.Model):
# 	email = models.CharField(max_length=256, primary_key=True, null=False)
# 	name = models.CharField(max_length=256, null=False)
# 	password = models.CharField(max_length=128, null=False)
# 	def __str__(self):
# 		return self.email + "|" + self.name

# We might decide to drop this later if deemed superfluous
class Language(models.Model):
	name = models.CharField(max_length=256, primary_key=True, null=False)
	def __str__(self):
		return self.name

# Represents a particular class. For eg: German A1, French C2 etc.
# class Class(models.Model):
# 	name = models.CharField(max_length=256, null=False)
# 	user = models.ForeignKey(User)
# 	class Meta:
# 		unique_together = ('name', 'user')
# 	def __str__(self):
# 		return self.name + "|" + str(self.user)

# Represents a Set of cards, no card can be created that does not exist in a set
class Set(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=256, null=False)
	description = models.CharField(max_length=256, null=True)
	language_from = models.ForeignKey(Language, related_name="language_from")
	language_to = models.ForeignKey(Language, related_name="language_to")
	class Meta:
		unique_together = ('user', 'title')
	def __str__(self):
		return str(self.user) + "|" + self.title

# Represents each card that belongs to a set. Weak Entity.
class Card(models.Model):
	set = models.ForeignKey(Set)
	term = models.CharField(max_length=256, null=False)
	definition = models.CharField(max_length=256, null=False)
	class Meta:
		unique_together = ('set', 'term', 'definition')
	def __str__(self):
		return str(self.set) + "|" + self.term + "|" + self.definition

# identifies the user has class/set representation
# class Has(models.Model):
# 	class_name = models.ForeignKey(Class)
# 	set = models.ForeignKey(Set)
# 	class Meta:
# 		unique_together = ('class_name', 'set')
# 	def __str__(self):
# 		return str(self.class_name) + " has " + str(self.set)