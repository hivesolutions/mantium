{% extends "partials/layout_build.html.tpl" %}
{% block title %}Projects{% endblock %}
{% block name %}{{ project.name }} :: {{ build.id }}{% endblock %}
{% block content %}
    <ul>
        {% for file in files %}
            <li>
                <a href="{{ url_for('files_build', id = project.id, build_id = build.id, path = path + file + '/') }}">{{ file }}</a>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
