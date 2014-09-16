from django.conf import settings


def get_translation(value, language):
    translations = value.split('\n') if value else []
    if len(translations) == 2:
        return translations[settings.LOCALIZED_LANGUAGES.index(language)]
    else:
        return value