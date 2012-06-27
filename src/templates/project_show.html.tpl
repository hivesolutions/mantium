{% extends "partials/layout.html.tpl" %}
{% block title %}Projects{% endblock %}
{% block name %}{{ project.name }}{% endblock %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        <a href="{{ url_for('new_project') }}">builds</a>
        //
        <a href="{{ url_for('edit_project', id = project.id) }}">edit</a>
        //
        <a href="{{ url_for('delete_project', id  = project.id) }}">delete</a>
        //
        <a href="{{ url_for('run_project', id  = project.id) }}">run</a>
    </div>
{% endblock %}
{% block content %}
    <div class="quote">{{ project.description }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">status</td>
                <td class="left value" width="50%">success</td>
            </tr>
            <tr>
                <td class="right label" width="50%">next run</td>
                <td class="left value" width="50%">12 Jun 15:40</td>
            </tr>
            <tr>
                <td class="right label" width="50%">build time</td>
                <td class="left value" width="50%">12 minutes 4 seconds</td>
            </tr>
            <tr>
                <td class="right label" width="50%">build count</td>
                <td class="left value" width="50%">43 builds</td>
            </tr>
            <tr>
                <td class="right label" width="50%">build file</td>
                <td class="left value" width="50%"><a href="#">build.json</a></td>
            </tr>
        </tbody>
    </table>
{% endblock %}
