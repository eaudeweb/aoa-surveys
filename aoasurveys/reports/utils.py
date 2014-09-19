from django.conf import settings


def get_translation(value, language=settings.DEFAULT_LANGUAGE):
    translations = value.split('\n') if value else []
    if len(translations) == len(settings.LOCALIZED_LANGUAGES_ABBR):
        return (
            translations[settings.LOCALIZED_LANGUAGES_ABBR.index(language)] or
            translations[settings.LOCALIZED_LANGUAGES_ABBR
                         .index(settings.DEFAULT_LANGUAGE)]
        )
    return value
