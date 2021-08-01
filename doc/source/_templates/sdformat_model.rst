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

.. currentmodule:: {{ fullname }}

.. rubric:: {{ _("Elements") }}

.. autosummary::
    :template: sdformat_element.rst
    :toctree: sdformat_{{ sdformat_version }}

{% for module_name in modules %}
{% if not module_name.endswith("type") %}
{% set class_path = module_name.split(".")[-1].split("_") | map("capitalize") | join("") %}
{% set class_path = class_path | replace("Shape", "") | replace("State", "") %}
{% if class_path == "Root" %}
{% set class_path = "Sdf" %}
{% endif%}
{% if class_path == "Forcetorque" %}
{% set class_path = "ForceTorque" %}
{% endif%}
    {{ class_path }}
{% endif %}
{% endfor %}
