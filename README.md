# Workflow

## 1. Set up virtual enviornment

- uv init
- uv venv
- .venv/Scripts/activate.ps1
- uv add -r requirements.txt

# 2. migrate the models initially

- python manage.py migrate

# 3. AbstractUser setup for more flexibility rather using django's User model

- in models.py initiate User with inherit AbstractUser (see in models.py)
- in settings.py add AUTH_USER_MODEL='contacts.User'
- this allows to add ore fields in authenticating an user (email, location whatever)

# 4. define django models

- create Contact model (see in models.py)
- once you created the model do the <'python manage.py makemigrations'> after that <'python manage.py migrate'>
- connect this Contact model with django admin (see admin.py)
- to view these create superuser by <'python manage.py createsuperuser'>
- run the server <'python manage.py runserver'>
- on the url add http://127.0.0.1/admin

# 5. build the user interface

- go to views.py and set login_required decorator on index() (see in views.py)
- get the contacts of the user
- create partials inside templates folder

# 6. build active search with htmx (contacts.html input element)

- we want hx-get (perform get req to a given url)
- hx-trigger (can be a click event, key up event etc)
- hx-target (target that html dom element to be swapped)
- go to urls.py and create a url called search (see in project urls.py)
- go to views.py and create a new view there called search_contacts
- use of hx-indicator attribute (used for showing spinners aka feedback of something running on the backend etc.)

  - create a partial called spinner.html and paste daisy ui code (see spinner.html)
  - contacts.html file add the hx-indicator attr (see contacts.html)
  - we can also use hx-on for more ux (see on contacts.html)

# 7. build contact form

- go to forms.py and create ContactForm class (see in forms.py)
- go to views.py and attach this form to the index method so that this form available in template (see in views.py)
- include this form in contacts.html design with daisy ui (see in contact.html)
- include this form inside of a modal so create add-contact-modal.html as a partial

# 8. submitting form with htmx

- use hx-post attribute
- go to urls.py and create a view for post requset (see in urls.py)
- go to views.py add do the business logic (see views.py [create_contact])
- go to add-contact-modal and add the hx-post attribute
- in views.py create logic for add data into the db ( see views.py [create_contact])
- create contact-row.html partial for add a new row on the contact list after conact created
- make the newly created contact comes at top (using hx-target, hx-swap in addd-contact-modal.html)
- make the modal closes after submit the form
  - for that go to views.py and send a header with response in the create_contact view (see views.py)
  - then go to add-contact-modal.html and see for that header with hx-on:success and close that modal with 'contact_modal.close()'[this is daisy ui method] & reset the form (see add-contact-modal.html)

# 9. Showing form errors in the front end

- for that in forms.py we create a method for validation for email address (see forms.py ContactForm class)
- and in create_contact method in views.py we modify with an else statement (views.py)
  and we change the target of the error response (add-contact-modal.html)

# 10. upload files with amazon s3

- to integrate with amazon s3 we use django-storages library
- in models.py add the document field (see in models.py)
- then do makemigration, migrate command
- go to forms.py add the file field (see forms.py)
- add this field to the template (add-contact-modal.html)
- in views.py setup for the file upload (see create_contact method in views.py)
- setup the media backend (https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)
- uv add django-storages[s3]
- create a bucket (video in the asset folder)
- add config in settings.py
- after that we decide how to authenticate with the s3 client
- create the access key (video in the assets folder)
- now in the powershell terminal '$Env:AWS_S#_ACCESS_KEY_ID = <paste your access key>' and '$Env:AWS_S3_SECRET_ACCESS_KEY = <paste your secret access key>'
- now in settings.py add these access keys (look end of settings.py)
  AWS_S3_ACCESS_KEY_ID = os.environ.get('AWS_S3_ACCESS_KEY_ID')
  AWS_S3_SECRET_ACCESS_KEY_ID = os.environ.get('AWS_S3_SECRET_ACCESS_KEY_ID')
  AWS_STORAGE_BUCKET_NAME = 'contacthub2-media'
  AWS_S3_REGION_NAME = 'us-east-1'
- use hx-encoding attribute for the file upload in htmx (add-contact-modal.html's form)
- you might want to install boto3
- show the files uploaded by user in the display
- create a column in contact-list.html, then in contact-row.html retrieve the document
- research about signed urls to access & amazon cloud front

# 11. prepare tailwind, daisyui, htmx for deployment

- ### set up htmx
- in base.html copy the link for htmx and paste on the browser --> copy the htmx.min.js --> create static/js/htmx.min.js -->paste the code
- then apply the local code in your base.html (see base.html)
- ### setup tailwindcss
- go to official tailwindcss and install by tailwindCLI, include daisyui as well
- npx @tailwindcss/cli -i ./contacts/static/styles/main.css -o ./contacts/static/styles/output.css --minify to minify the classes useful for production

# deploy on render

- set up postgres
  - uv add psycopg2-binary
  - uv add dj-database-url
- configure settings.py, override the DATABASES with postgres
- setup static file serving
  - uv add whitenoise[brotli]
  - add whitenoise middleware to settings.py
  - add STATIC_ROOT in settings.py
  - and for best static fiiles compression modify the STORAGES -> staticfiles in settings.py
  - we also need to change
  - SECRET_KEY, DEBUG = True, ALLOWED_HOSTS = [] (go to adding basic security in render docs)
  - build the build script (go to deploying to render section)
  - go to create build script section --> create build.sh file in root folder and paste the code
  - there are 2 ways to deploy define render.yaml(best)/ manually define on render dashboard
  - create render.yaml, paste the code

