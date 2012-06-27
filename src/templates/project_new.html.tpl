{% extends "partials/layout.html.tpl" %}
{% block title %}Projects{% endblock %}
{% block name %}New Project{% endblock %}
{% block content %}
    <div class="quote">
        In order to start automating the build we need some information on your little project
        this information include the mythical <a href="docs/build.json">build.json</a> file.
    </div>
    <div class="separator-horizontal"></div>
    <form action="{{ url_for('create_project') }}" enctype="multipart/form-data" method="post" class="form">
        <div class="label">
            <label>Project Name</label>
        </div>
        <div class="input">
            <input name="name" placeholder="eg: colony" />
        </div>
        <div class="label">
            <label>Description</label>
        </div>
        <div class="input">
            <textarea name="description" placeholder="words about the project"></textarea>
        </div>
        <div class="label">
            <label>Build File</label>
        </div>
        <div class="input">
             <a data-name="build_file" class="uploader">Select & Upload the build file</a>
        </div>
        <div class="quote">
            By clicking Submit Project, you agree to our Service Agreement and that you have
            read and understand our Privacy Policy.
        </div>
        <span class="button" data-submit="true">Submit Project</span>
    </form>
{% endblock %}
