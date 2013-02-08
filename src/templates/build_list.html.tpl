{% extends "partials/layout_project.html.tpl" %}
{% block title %}Builds{% endblock %}
{% block name %}{{ project.name }} :: builds{% endblock %}
{% block content %}
    <ul>
        {% for build in builds %}
            <li>
                <div class="name">
                    <a href="{{ url_for('show_build', name = project.name, id = build.id) }}"># {{ build.id }}</a>
                </div>
                <div class="description">
                    <span class="{{ build.result_l }}">{{ build.result_l }}</span> on {{ build.start_time_l }}
                </div>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
