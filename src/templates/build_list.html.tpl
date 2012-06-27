{% extends "partials/project_layout.html.tpl" %}
{% block title %}Builds{% endblock %}
{% block name %}{{ project.name }} ::  builds{% endblock %}
{% block content %}
    <ul>
        {% for build in builds %}
            <li>
                <div class="name">
                    <a href="{{ url_for('show_build', id = project.id, build_id = build.id) }}"># {{ build.id }}</a>
                </div>
                <div class="description">
                    <span class="{{ build._result }}">{{ build._result }}</span> on {{ build._start_time }}
                </div>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
