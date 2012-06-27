{% extends "partials/layout.html.tpl" %}
{% block title %}Projects{% endblock %}
{% block name %}{{ project.name }} :: {{ build.id }}{% endblock %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        <a href="{{ url_for('delete_build', id = project.id, build_id = build.id) }}">log</a>
        //
        <a href="{{ url_for('delete_build', id = project.id, build_id = build.id) }}">files</a>
        //
        <a href="{{ url_for('delete_build', id = project.id, build_id = build.id) }}">delete</a>
    </div>
{% endblock %}
{% block content %}
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">result</td>
                <td class="left value {{ build._result }}" width="50%">{{ build._result }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">start time</td>
                <td class="left value" width="50%">{{ build._start_time }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">end time</td>
                <td class="left value" width="50%">{{ build._end_time }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">duration</td>
                <td class="left value" width="50%">{{ build.delta }} seconds</td>
            </tr>
            <tr>
                <td class="right label" width="50%">build size</td>
                <td class="left value" width="50%">{{ build.size|filesizeformat }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">system</td>
                <td class="left value" width="50%">{{ build.system }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
