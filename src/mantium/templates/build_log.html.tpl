{% extends "partials/layout_build_w.html.tpl" %}
{% block title %}Projects{% endblock %}
{% block name %}{{ project.name }} :: {{ build.id }}{% endblock %}
{% block content %}
    <pre>{{ log }}</pre>
{% endblock %}
