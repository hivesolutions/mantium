{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Automium - {% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body class="ux">
    <div id="header">
        {% block header %}
            <h1>{% block name %}{% endblock %}</h1>
            <div class="links">
                <a href="{{ url_for('index') }}">home</a>
                //
                <a href="{{ url_for('projects') }}">projects</a>
                //
                <a href="{{ url_for('projects') }}/new">new project</a>
                //
                <a href="{{ url_for('status') }}">status</a>
            </div>
        {% endblock %}
    </div>
    <div id="content">{% block content %}{% endblock %}</div>
    {% include "partials/footer.html.tpl" %}
</body>
{% include "partials/end_doctype.html.tpl" %}
