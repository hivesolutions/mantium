{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        <a href="{{ url_for('show_build', id = project.id, build_id = build.id) }}">info</a>
        //
        <a href="{{ url_for('log_build', id = project.id, build_id = build.id) }}">log</a>
        //
        <a href="{{ url_for('files_build', id = project.id, build_id = build.id, path = '') }}">files</a>
        //
        <a href="{{ url_for('delete_build', id = project.id, build_id = build.id) }}">delete</a>
    </div>
{% endblock %}
