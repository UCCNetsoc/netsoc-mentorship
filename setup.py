from setuptools import setup

setup(name='netsoc_mentorship_service',
      version='0.1',
      description='Allows people to sign up to projects lead by mentors, and mentors to submit projects for Netsocs approval',
      url='~',
      author='Netsoc/HassanBaker',
      author_email='~',
      license='open',
      packages=['netsoc_mentorship'],
      zip_safe=False,
      install_requires=['sendgrid', 'flask'])