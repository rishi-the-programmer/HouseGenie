from setup import app,api
from flask import render_template, redirect, request
from api.signin import Signin
from api.register import Register
from functools import wraps
from api.signout import SignOut
from api.services import Services,SpecificService
from api.service_category import ServiceCat
from models.Service import ServiceCategory, Service
from models.ServiceRequest import ServiceRequest
from models.Professional import Professional
from api.service_request import GetRequests, GetSpecificRequest, CloseServiceRequest,BookService, AcceptRejectServiceRequest, AssignServiceRequest, ReviewServiceRequest
from api.professional import ProfessionalAPI, ServiceProfessionals
from helpers.auth_decorators import check_signin

@app.route('/')
@check_signin
def home(signed_in,signin_as,signed_email,signed_id):
    if signin_as=="admin":
        categories=ServiceCategory.query.all()
        services=Service.query.all()
        professionals=Professional.query.filter_by(approved=False).all()
        return render_template('home.html',signed_in=signed_in,signin_as=signin_as,categories=categories,services=services,professionals=professionals)
    elif signin_as=="customer":
        categories=ServiceCategory.query.all()
        return render_template('home.html',signed_in=signed_in,signin_as=signin_as,categories=categories)
    elif signin_as=="professional":
        professional=Professional.query.filter_by(email=signed_email).first()
        return render_template('home.html',signed_in=signed_in,signin_as=signin_as,signed_email=signed_email,professional=professional)
    else:
        return render_template('home.html',signed_in=signed_in,signin_as=signin_as)

@app.route('/signin')
def admin_login():
    return render_template('signin.html')

@app.route('/register/customer')
def customer_register():
    return render_template('customer_register.html')

@app.route('/register/professional')
def professional_register():
    services=Service.query.all()
    return render_template('professional_register.html',services=services)

@app.route('/professional/<int:id>')
@check_signin
def professional(id,signed_in,signin_as,signed_email,signed_id):
    professional=Professional.query.filter_by(id=id).first()
    return render_template('professional.html',professional=professional,signed_in=signed_in,signin_as=signin_as,signed_email=signed_email), 404 if professional is None else 200

@app.route('/service_request/<int:id>')
@check_signin
def service_request(id,signed_in,signin_as,signed_email,signed_id):
    return render_template('service_request.html',signed_in=signed_in,signin_as=signin_as,signed_email=signed_email), 404 if service_request is None else 200

api.add_resource(Signin,'/api/signin')
api.add_resource(Register,'/api/register')
api.add_resource(SignOut,'/api/signout')
api.add_resource(Services,'/api/services','/api/services/<category>')
api.add_resource(SpecificService,'/api/service/<int:id>')
api.add_resource(ServiceCat,'/api/service_category')
api.add_resource(GetRequests,'/api/service_request')
api.add_resource(GetSpecificRequest,'/api/service_request/<int:id>')
api.add_resource(BookService,'/api/service/<int:id>/book','/api/service_request/<int:id>/edit')
api.add_resource(AssignServiceRequest,'/api/service_request/<int:service_request_id>/assign/<int:professional_id>')
api.add_resource(AcceptRejectServiceRequest,'/api/service_request/<int:id>/<reqType>')
api.add_resource(CloseServiceRequest,'/api/service_request/<int:id>/close')
api.add_resource(ReviewServiceRequest,'/api/service_request/<int:id>/rate')
api.add_resource(ProfessionalAPI,'/api/professional/<int:id>/approve')
api.add_resource(ServiceProfessionals,'/api/service/<int:service_id>/professionals/<professionalType>')

if __name__ == '__main__':
    app.run(debug=True)