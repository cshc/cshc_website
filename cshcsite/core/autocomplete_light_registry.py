import autocomplete_light
from models import CshcUser

# This will generate a CshcUserAutocomplete class
autocomplete_light.register(CshcUser,
    # Just like in ModelAdmin.search_fields
    search_fields=['first_name', 'last_name', 'email'],
    attrs={
        # This will set the input placeholder attribute:
        'placeholder': 'User search...',
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery
        'data-autocomplete-minimum-characters': 1,
    },
    # This will set the data-widget-maximum-values attribute on the
    # widget container element, and will be set to
    # yourlabs.Widget.maximumValues (jQuery handles the naming
    # conversion).
    widget_attrs={
        'data-widget-maximum-values': 4,
        # Enable modern-style widget !
        'class': 'modern-style',
    },
)