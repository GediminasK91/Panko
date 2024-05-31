from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password
        )

        error_message = self.validate_customer(customer)

        if not error_message:
            customer.password = make_password(customer.password)
            customer.is_active = False
            customer.register()
            self.send_activation_email(request, customer)
            messages.success(request, 'Registration successful. A confirmation email has been sent to your email address.')
            return redirect('home')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validate_customer(self, customer):
        validations = {
            "First Name is required.": not customer.first_name,
            "First Name must be 4 characters long or more.": len(customer.first_name) < 4,
            "Last Name is required.": not customer.last_name,
            "Last Name must be 4 characters long or more.": len(customer.last_name) < 4,
            "Phone Number is required.": not customer.phone,
            "Phone Number must be 10 characters long.": len(customer.phone) < 10,
            "Password must be 6 characters long.": len(customer.password) < 6,
            "Email must be 5 characters long.": len(customer.email) < 5,
            "Email Address is already registered.": customer.isExists()
        }

        for error_message, condition in validations.items():
            if condition:
                return error_message

        return None

    def send_activation_email(self, request, customer):
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('store/acc_active_email.html', {  # Ensure the correct path
            'customer': customer,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(customer.pk)),
            'token': default_token_generator.make_token(customer),
        })
        email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, [customer.email])
        email.send()

class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            customer = Customer.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
            customer = None
        
        if customer is not None and default_token_generator.check_token(customer, token):
            customer.is_active = True
            customer.save()
            return HttpResponse('Your account has been activated successfully!')
        else:
            return HttpResponse('Activation link is invalid!')
