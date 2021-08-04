{% set sdformat_version =  name[0] + name[1] + "." + name[2:] %}
{% set title =  "SDFormat " + sdformat_version + " Bindings" %}

.. py:module:: {{fullname}}

{{ title | underline}}

.. warning::
    If you want to use these bindings explicitly, you need to import them
    first::

        import ropy.ignition.sdformat.bindings.{{name}} as {{name}}

Ropy's SDFormat bindings are realized as a set of dataclasses. Each class
corresponds to a unique element found within SDFormat XML and has an attribute
for every attribute and child of the corresponding SDFormat element. Names
generally match the names used within SDFormat; however, are adapted to python
convention where needed.

.. currentmodule:: {{ fullname.split(".")[:-1] | join(".") }}

.. rubric:: {{ _("Elements") }}

.. autosummary::
    :template: sdformat_element.rst
    :toctree: sdformat_{{ sdformat_version }}

{% for module_name in modules %}
{% set class_path = module_name.split(".")[-1] %}
    {{ name }}.{{ class_path }}.{{ class_path.capitalize() }}
{% if class_path == "state" %}
{% if not sdf_version not in ["v1.0", "v1.2"] %}
    {{ name }}.{{ class_path }}.Model
{% endif %}
{% endif %}
{% endfor %}
