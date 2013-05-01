# Target price project

Documentation and implementation of target price project

### Documentation

* [Documentation in pdf format](Django/prototype/pdf/api.pdf)
* [Graphical representation of database in pdf format](Django/prototype/database/beta_database_model.pdf)

### Implementation

* [Front-end](Django/prototype)
* [Crawler API](Django/crawler)
* [Daily Crawler API](crawler_daily)
* [Yahoo stock prices crawler](stock_prices_crawler)
* [Calculations model](model)

### Deployment

* Full deployment of public (Django part)

  $ fab public_setup

* Full deployment of private (model, crawlers)

  $ fab private_setup

* Public page update

  $ fab django_prototype_update


### Dependencies

Individual for every implementation