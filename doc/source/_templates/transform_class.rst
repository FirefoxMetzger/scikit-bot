{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% block methods %}
   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
   {% if "__call__" in members %}
      __call__
   {% endif %}
   {% for item in methods %}
      {% if not item == "__init__" %}
      ~{{ name }}.{{ item }}
      {% endif %}
   {%- endfor %}
   {% if "__inverse_transform__" in members %}
      __inverse_transform__
   {% endif %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}


   {% if methods %}
   {% if "__call__" in members %}
   .. automethod:: __call__
   {% endif %}
   {% for item in methods %}
   {% if not item == "__init__" %}
   .. automethod:: {{ item }}
   {% endif %}
   {%- endfor %}
   {% if "__inverse_transform__" in members %}
   .. automethod:: __inverse_transform__
   {% endif %}
   {% endif %}
