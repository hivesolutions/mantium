{% extends "partials/layout.html.tpl" %}
{% block title %}Home{% endblock %}
{% block content %}
    <form action="{{ url_for('login') }}" method="post" class="form">
        <input name="username" />
        <input name="password" type="password" />
        <button type="button" type="submit">Login</button>
    </form>
{% endblock %}
