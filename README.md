# Target price project

Documentation and implementation of target price project

### Documentation

* [Documentation in pdf format](blob/master/Django/prototype/pdf/api.pdf)
* [Graphical representation of database in pdf format](blob/master/Django/prototype/database/beta_database_model.pdf)

### Implementation

* [Front-end](blob/master/Django/prototype/prototype)
* [Back-end](blob/master/model)

### Deployment

* Full deployment of app (virtualenv with all dependencies, clean database)

  $ fab setup

* Small deployment of app (just a code from git to current virtualenv)
  
  $ fab small_deploy

Still a lot of bugs and conflicts, work in progress version

### Dependencies

* django==1.4.3
* django-piston
* django-apikey
* gunicorn
* psycopg2
* pyyaml
