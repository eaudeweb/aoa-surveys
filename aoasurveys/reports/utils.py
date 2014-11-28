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


def set_translation(obj, attr, value, language=settings.DEFAULT_LANGUAGE):
    db_obj = obj.__class__._default_manager.get(pk=obj.pk)
    languages = settings.LOCALIZED_LANGUAGES_ABBR
    translations = getattr(db_obj, attr).split('\n')
    translations += [''] * (len(languages) - len(translations))
    translations[languages.index(language)] = value
    setattr(obj, attr, '\n'.join(translations))
