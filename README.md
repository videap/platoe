# Capstone

This application called **Plato** is an old idea that got me to start developing. This is the first version, with lots of enhancements yet to be made. It is a work-in-progress that will be released soon.

The main idea is to connect people who need ideas with people who are creative. So, the users can buy and sell ideas very fast. The name is a "tribute" to the **World of Ideas Theory**, by Plato.

I believe this project is distinct because of the security concerns to handle sensitive data (ideas) and the payments integrations (Stripe). Some users pay, some users receive, and their capacities are handled by different "accept terms". There is a 2-layer API, one presented to the front end, and other to integrate with stripe only using data fetched from the database. Also, the user model is very robust, with protection against brute force attacks, password validation and reset options (configured with secure hashes to be sent by email), uniqueness restrictions and capacity to update user information.  


# Principles

By definition, an idea cannot be "shown" to someone before payment, otherwise the product is delivered with no payment. So the website has stripe integration that confirms payments through webkooks. There is a 2-Layer API, one for the front-end, and other for the server to handle financial operations with stripe (not accessible by clients). The information available to the client-side is very controlled.

The front-end is mostly designed with React. Lots of Classes are very alike, but they are different elements because in the future they will become very different.

Some of important features are almost ready, such as password change, webhooks, file handling, but require email servers, storage devices, public endpoints, certificates, so they are not complete yet. 

## How to Run

### Settings
Depending on the environment to run Plato, this is changes on the settings.py file in the main directory for Django. There is a file for each setting, calles dev-settings.py, test-settings.py and prod-settings.py. When starting the project, this should be defined.

To deploy your environments, please check the "DeployGuides" folder and read specific documentation.

