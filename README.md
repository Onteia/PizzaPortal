# Overview

Pizza Portal is a pizza shop management web-app made with the Django web framework. 

It allows the user, after account creation, to manage various aspects of managing pizza shops.
On sign up, users must choose whether they are a pizza shop owner or a pizza chef. Owners are able to add, modify, and delete toppings whereas chefs are able to add, modify, and 
delete pizzas. Each topping and pizza must be unique to ensure an intuitive experience with the portal.

With this project I wanted to take the time to learn Django and further develop my Python skills. I made the deliberate decision to move as much logic away from the django html templates
to the forms. I figured that the templates should only be reserved for displaying the content rather than also processing that very same content. If, in the future, the website were 
to be changed, those modifications would be easier to make without worrying about breaking the underlying app. Throughout the construction of the portal, I was indecisive about the 
behavior when an owner deletes a topping that belongs to pizzas on the menu. In the end, I decided the most straightforward behavior from the perspective of the owners and chefs would be to
delete the pizzas that contained the topping as well. I chose to implement the relationship between Pizzas and Toppings as a ManyToMany relationship because I wanted to give chefs
as much freedom as possible to create many different pizzas. However, I quickly learned that ManyToMany relationships didn't have a constraint for unique sets of these relationships.
So, in order to satisfy the conditions of unique pizzas with unique toppings, I overrode the `clean()` method of the PizzaForm---the method that validates forms. Lastly, I added 
extra fields such as description and costs to further learn how Django works and to gather any additional knowledge as I reasonably can with this project.

---
# Setup

Ensure you have the following:

- [python3](https://www.python.org/downloads/)
- pip (Should come with python3)

# Building & Installing

1. Clone the repository

	```bash
	git clone https://github.com/Onteia/PizzaPortal
	cd PizzaPortal
	```

2. Create a virtual environment (OPTIONAL, but recommended) 

	**Unix & macOS**

	```bash
	python -m venv .venv	
	source .venv/bin/activate
	```

	**Windows**

	```powershell
	python -m venv .venv
	.venv/Scripts/activate
	```

3. Install dependencies

	```bash
	python -m pip install -r requirements.txt
	```

4. Generate secret key

	**Unix & macOS**

	```bash
	echo "SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env
	```

	**Windows**

	```powershell
	echo | set /p=SECRET_KEY=> .env
	python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" >> .env
	```

5. Create and migrate database data

	```bash
	python manage.py migrate
	```

# Running

1. Start the server

	```bash
	python manage.py runserver
	```

2. Visit the local site by navigating to 127.0.0.1/8000. If the page isn't available, you may need to allow port 8000 in your firewall.

# Testing the portal

Tests can be run with the following command:

```bash
python manage.py test
```

## More specific testing

Additionally, a module, file, class, or method may be provided to run a specific subset of tests.

Note that not all of these specifiers are required.

```bash
python manage.py test <module>.tests.<file>.<class>.<method>
```

Module test files can be found in the `tests` directory of the following modules:

- [pages](pages/tests/)
- [portal](portal/tests/)




