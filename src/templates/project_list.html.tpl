{% extends "partials/layout.html.tpl" %}
{% block title %}Projects{% endblock %}
{% block name %}Projects{% endblock %}
{% block content %}
    <ul>
        {% for project in projects %}
            <li>
                <div class="name">
                    <a href="{{ url_for('show_project', id = project.id) }}">{{ project.name }}</a>
                </div>
                <div class="description">
                    {{ project.description }}
                </div>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
