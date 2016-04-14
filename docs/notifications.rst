=============
Notifications
=============

Configuration
=============

To use email notifications, you must add ``'simple_forums.notifications'`` to INSTALLED_APPS. Don't forget to run your database migrations after doing that.

The other requirement for notifications is to have your email settings correctly configured. The crucial settings are EMAIL_HOST and EMAIL_PORT. For more information, refer to the `django documentation`_.

Templates
=========

To include notifications-specific items in your templates, you can use the variables provided by simple forums' context processor (if installed). Example::

    # my_app/my_template.html

    {% if notifications_installed %}
        {{ notification_form }}
    {% endif %}


.. _django documentation: https://docs.djangoproject.com/en/1.9/ref/settings/#email-backend