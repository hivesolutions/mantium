{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        <a href="{{ url_for('show_project', id = project.id) }}">info</a>
        //
        <a href="{{ url_for('builds', id = project.id) }}">builds</a>
        //
        <a href="{{ url_for('edit_project', id = project.id) }}">edit</a>
        //
        <a href="{{ url_for('delete_project', id = project.id) }}">delete</a>
        //
        <a href="{{ url_for('run_project', id  = project.id) }}">run</a>
    </div>
{% endblock %}
