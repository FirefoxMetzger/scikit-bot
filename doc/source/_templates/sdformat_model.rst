{{ fullname | escape | underline}}

{% set sdformat_version =  objname[0] + objname[1] + "." + objname[2:] %}

This are the SDFormat bindings for SDFormat {{ sdformat_version }}. Here, you
fill find a dataclass for each element that can occur inside a valid SDF. When
you load SDF via :func:`ropy.ignition.sdformat.loads` ropy will return a tree of
instances of the classes documented here. 

.. note::
    The entire module and it's documentation are auto-generated. As such, the
    documentation may be imperfect at times. You may also wish to refer to the
    `SDFormat spec <http://sdformat.org/spec>`_ for further details on the
    format.

.. currentmodule:: {{ fullname }}

Elements
--------

.. autosummary::
    :template: sdformat_element.rst
    :toctree:

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
 
.. automodule:: {{ fullname }}
 
    {% block attributes %}
    {% if attributes %}
    .. rubric:: {{ _('Module Attributes') }}
 
    .. autosummary::

    {% for item in attributes %}
       {{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}
 
    {% block functions %}
    {% if functions %}
    .. rubric:: {{ _('Functions') }}
 
    .. autosummary::

    {% for item in functions %}
       {{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}
 
    {% block classes %}
    {% if classes %}
    .. rubric:: {{ _('Classes') }}
 
    .. autosummary::

    {% for item in classes %}
        {{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}
 
    {% block exceptions %}
    {% if exceptions %}
    .. rubric:: {{ _('Exceptions') }}
 
    .. autosummary::

    {% for item in exceptions %}
       {{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}
