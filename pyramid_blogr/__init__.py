from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Deny, Everyone, Authenticated
from pyramid.session import SignedCookieSessionFactory
from models import *

my_s_f = SignedCookieSessionFactory('itsasecret')

class MyFactory(object):
    def __init__(self, request):
        self.__acl__ = [
            (Allow, Everyone, 'view'),
            (Allow, Authenticated,'add')
        ]

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    Base.metadata.create_all()
    
    authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, session_factory=my_s_f, root_factory=MyFactory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_jinja2')

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon') 
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home','/')
    config.add_route('view_blog', '/index') 
    config.add_route('register', '/register')
    config.add_route('view_my', '/my')
    config.add_route('blog_article', '/post/{postid}')
    config.add_route('blog_create','/post')
    config.add_route('login','/login')
    config.add_route('logout','/logout')
    config.add_route('about','/about')
    config.scan()
    return config.make_wsgi_app()