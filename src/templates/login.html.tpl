{% extends "layout.html.tpl" %}
{% block title %}Home{% endblock %}
{% block content %}
    <form action="login" method="post" class="form">
        <input class="text-field" name="username" />
        <div class="button button-green" data-submit="true">Submit</div>
    </form>
{% endblock %}
