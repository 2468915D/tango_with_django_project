from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category
from rango.models import Page
from rango.forms import UserForm, UserProfileForm
from rango.forms import CategoryForm, PageForm

def index(request):
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by the number of likes in descending order.
	# Retrieve the top 5 only -- or all if less than 5.
	# Place the list in our context_dict dictionary (with our boldmessage!) # that will be passed to the template engine.
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {}
	context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
	context_dict['categories'] = category_list
	context_dict['pages'] = page_list

	# Render the response and then send it back!
	return render(request, 'rango/index.html', context=context_dict)

def about(request):
	context_dict = {'boldmessage': 'This tutorial has been put together by Aidan!'}
	return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
	context_dict = {}

	try:
		# Can we find a category name slug with the given name?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# The .get() method returns one model instance or raises an exception.
		category = Category.objects.get(slug=category_name_slug)

		# Retrieve all of the associated pages.
		# The filter() will return a list of page objects or an empty list.
		pages = Page.objects.filter(category=category)

		# Adds our results list to the template context under name pages.
		context_dict['pages'] = pages

		# We also add the category object from
		# the database to the context dictionary.
		# We'll use this in the template to verify that the category exists.
		context_dict['category'] = category

	except Category.DoesNotExist:
		# We get here if we didn't find the specified category.
		# Don't do anything -
		# the template will display the "no category" message for us.

		context_dict['pages'] = None
		context_dict['category'] = None

	# Go render the response and return it to the client.
	return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_category(request):
	form = CategoryForm()

	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

	if form.is_valid():
		form.save(commit=True)
		return redirect('/rango/')

	else:
		# Form had errors, print to terminal
		print(form.errors)

	return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	if not category:
		return redirect(reverse(''))

	form = PageForm()

	if request.method == 'POST':
		form = PageForm(request.POST)

	if form.is_valid():
		if category:

			page = form.save(commit=False)
			page.category = category
			page.views = 0
			page.save()

			return redirect(reverse('rango:show_category',
									kwargs={'category_name_slug':
											category_name_slug}))
	else:
		print(form.errors)

	context_dict = {'form': form, 'category': category}
	return render(request, 'rango/add_page.html', context=context_dict)

	


def register(request):
	registered = False

	# If it's a http POST, process form data
	if request.method == 'POST':
		# Retrieve data from the forms
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			# Save the form data to the database
			user = user_form.save()

			# set_password hashes the password, then we save the user
			user.set_password(user.password)
			user.save()

			# commit=False delays saving the model to avoid integrity issues
			# Create the one-to-one relationship between the profile and user
			profile = profile_form.save(commit=False)
			profile.user = user

			# If user uploaded a picture, add it, then save profile to db
			if 'picture' in request.FILES:
				profile_picture = request.FILES['picture']

				profile.save()
				# At this point, user is registered
			registered = True
		else:
			# Display errors
			print(user_form.errors, profile_form.errors)

	else:
		# Render using Blank forms ready for user input
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,
			'rango/register.html',
			context = {'user_form': user_form,
					   'profile_form': profile_form,
					   'registered': registered})



def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Check if username/password combination is valid, returns a User obj
		user = authenticate(username=username, password=password)

		# If above was valid
		if user:
			if user.is_active:
				login(request, user)
				return redirect(reverse('rango:index'))
			else:
				return HttpResponse('Your Rango account is disabled.')
		else:
			# Bad login details were provided
			print(f'Invalid login details {username}, {password}')
			return HttpResponse('Invalid login details supplied.')
	else:
		return render(request, 'rango/login.html')



@login_required
def restricted(request):
	return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('rango:index'))




