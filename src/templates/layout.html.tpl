<!DOCTYPE html>
<html lang="en">
<head>
    {% block head %}
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" type="text/css" href="http://hivesolutions.github.com/uxf/bin/css/ux-min.css" />
        <link rel="stylesheet" type="text/css" href="http://hivesolutions.github.com/uxf/styles/omni/css/ux.css" />
        <link rel="stylesheet" href="{{ url_for('static', filename='css/layout.css') }}" />
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
        <script type="text/javascript" src="http://hivesolutions.github.com/uxf/bin/js/ux-min.js"></script>
        <script type="text/javascript" src="{{ url_for('static', filename='js/main.js') }}"></script>
        <title>Automium - {% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body class="ux omni-style">
    <div id="content">{% block content %}{% endblock %}</div>
    <div id="footer">
        {% block footer %}
            &copy; Copyright 2010 by <a class="link link-blue" href="http://www.sapo.pt">you</a>.
        {% endblock %}
    </div>
</body>
</html>
