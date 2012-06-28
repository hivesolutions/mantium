{% extends "partials/layout_project.html.tpl" %}
{% block title %}Projects{% endblock %}
{% block name %}{{ project.name }} :: edit{% endblock %}
{% block content %}
    <form action="{{ url_for('update_project', id = project.id) }}" enctype="multipart/form-data" method="post" class="form">
        <div class="label">
            <label>Project Name</label>
        </div>
        <div class="input">
            <input name="name" value="{{ project.name }}" placeholder="eg: colony" />
        </div>
        <div class="label">
            <label>Description</label>
        </div>
        <div class="input">
            <textarea name="description" placeholder="eg: some words about the project">{{ project.description }}</textarea>
        </div>
        <div class="label">
            <label>Recursion</label>
        </div>
        <div class="recursion-set">
            <input class="recursion" name="days" value="{{ project.recursion.days }}" placeholder="-" /> days
            <input class="recursion" name="hours" value="{{ project.recursion.hours }}" placeholder="-" /> hours
            <input class="recursion" name="minutes" value="{{ project.recursion.minutes }}" placeholder="-" /> minutes
            <input class="recursion" name="seconds" value="{{ project.recursion.seconds }}" placeholder="-" /> seconds
        </div>
        <div class="label">
            <label>Build File</label>
        </div>
        <div class="input">
             <a data-name="build_file" class="uploader">Select & Upload the build file</a>
        </div>
        <span class="button" data-link="{{ url_for('show_project', id = project.id) }}">Cancel</span>
        //
        <span class="button" data-submit="true">Update</span>
    </form>
{% endblock %}
