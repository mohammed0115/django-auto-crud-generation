from textwrap import dedent


def generate_templates(facade):
    model_lower = facade.model_name

    return {
        "list.html": dedent(f"""
        {{% extends "base.html" %}}
        {{% block content %}}
        <h2>{model_lower.title()} List</h2>

        <form method="get">
            <input type="text" name="search" placeholder="Search..." class="form-control mb-2">
            <button type="submit" class="btn btn-primary">Search</button>
        </form>

        <table class="table mt-3">
            <thead>
                <tr>
                    {{% for field in objects.model._meta.fields %}}
                        <th>{{{{ field.name }}}}</th>
                    {{% endfor %}}
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {{% for obj in objects %}}
                <tr>
                    {{% for field in obj._meta.fields %}}
                        <td>{{{{ obj|attr:field.name }}}}</td>
                    {{% endfor %}}
                    <td>
                        <a href="{{{{ obj.id }}}}/update/" class="btn btn-sm btn-warning">Edit</a>
                        <a href="{{{{ obj.id }}}}/delete/" class="btn btn-sm btn-danger">Delete</a>
                    </td>
                </tr>
                {{% endfor %}}
            </tbody>
        </table>

        {{% endblock %}}
        """),

        "form.html": dedent("""
        {% extends "base.html" %}
        {% block content %}
        <h2>Form</h2>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-success">Save</button>
        </form>
        {% endblock %}
        """),

        "confirm_delete.html": dedent("""
        {% extends "base.html" %}
        {% block content %}
        <h2>Confirm Delete</h2>
        <form method="post">
            {% csrf_token %}
            <p>Are you sure you want to delete this item?</p>
            <button type="submit" class="btn btn-danger">Yes, delete</button>
        </form>
        {% endblock %}
        """),
    }
