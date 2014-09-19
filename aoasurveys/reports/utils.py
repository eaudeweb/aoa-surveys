from django.conf import settings


def get_translation(value, language=settings.DEFAULT_LANGUAGE):
    translations = value.split('\n') if value else []
    if len(translations) == 2:
        return translations[settings.LOCALIZED_LANGUAGES_ABBR.index(language)]
    else:
        return value
