import autocomplete_light
from models import Match

# This will generate a MatchAutocomplete class
autocomplete_light.register(Match,
    # Just like in ModelAdmin.search_fields
    search_fields=['our_team__long_name', 'our_team__short_name', 'opp_team__name', 'id'],
    attrs={
        # This will set the input placeholder attribute:
        'placeholder': 'Match search...',
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