{% extends "partials/layout.html.tpl" %}
{% block title %}About{% endblock %}
{% block name %}About{% endblock %}
{% block content %}
    <div class="quote">
        The complete project was developed by the <a href="http://hive.pt">Hive Solutions</a><br />
        developement team using only spare time.
    </div>
    <div class="separator-horizontal"></div>
    <div class="quote">
        Automium currently licensed under the much permissive<br />
        <strong>GNU General Public License (GPL), Version 3</strong>
        and the<br/>
        current repository is hosted at <a href="https://github.com/hivesolutions/automium_web">github</a>.
    </div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">uptime</td>
                <td class="left value" width="50%">12 seconds</td>
            </tr>
            <tr>
                <td class="right label" width="50%">size</td>
                <td class="left value" width="50%">123 MBytes</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
