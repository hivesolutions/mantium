{% extends "partials/layout.html.tpl" %}
{% block title %}Projects{% endblock %}
{% block name %}Projects{% endblock %}
{% block content %}
    <ul>
        {% for project in projects %}
            <li><a href="{{ url_for('show_project', id = project)  }}">{{ project }}</a></li>
        {% endfor %}
    </ul>
{% endblock %}
