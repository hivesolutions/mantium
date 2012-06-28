{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "info" %}
            <a href="{{ url_for('show_project', id = project.id) }}" class="active">info</a>
        {% else %}
            <a href="{{ url_for('show_project', id = project.id) }}">info</a>
        {% endif %}
        //
        {% if sub_link == "builds" %}
            <a href="{{ url_for('builds', id = project.id) }}" class="active">builds</a>
        {% else %}
            <a href="{{ url_for('builds', id = project.id) }}">builds</a>
        {% endif %}
        //
        {% if sub_link == "delete" %}
            <a href="{{ url_for('run_project', id  = project.id) }}" class="active">run</a>
        {% else %}
            <a href="{{ url_for('run_project', id  = project.id) }}">run</a>
        {% endif %}
        //
        {% if sub_link == "edit" %}
            <a href="{{ url_for('edit_project', id = project.id) }}" class="active">edit</a>
        {% else %}
            <a href="{{ url_for('edit_project', id = project.id) }}">edit</a>
        {% endif %}
        //
        {% if sub_link == "delete" %}
            <a href="{{ url_for('delete_project', id = project.id) }}" class="active">delete</a>
        {% else %}
            <a href="{{ url_for('delete_project', id = project.id) }}">delete</a>
        {% endif %}
    </div>
{% endblock %}
