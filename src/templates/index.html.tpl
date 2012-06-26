{% extends "layout.html.tpl" %}{% block content %}
    {% if name %}        <h1>Hello {{ name }}!</h1>        <div class="button button-green" data-link="http://www.sapo.pt">Hello World</div>    {% else %}        <h1>Hello World!</h1>    {% endif %}
{% endblock %}
