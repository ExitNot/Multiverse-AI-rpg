import json
import os
from typing import Dict, Any, Optional
import logging as log


class Locale:
    _instance = None
    _lang: str = "en"
    _data: Dict[str, Any] = {}
    _supported_languages = ["en", "uk", "ru", "cs"]

    def __new__(cls, lang: str = "en"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, lang: str = "en") -> None:
        self.log = log.getLogger(__name__)
        if lang != self._lang:
            self.set_language(lang)

    @classmethod
    def set_language(cls, lang: str) -> None:
        """
        Set the language and load corresponding locale file
        
        Args:
            lang: Language code to set
            
        Raises:
            ValueError: If language is not supported
            FileNotFoundError: If locale file doesn't exist
        """
        if lang not in cls._supported_languages:
            raise ValueError(f"Language {lang} is not supported. Supported languages: {', '.join(cls._supported_languages)}")
        
        locale_path = f'locales/{lang}.json'
        if not os.path.exists(locale_path):
            raise FileNotFoundError(f"Locale file not found: {locale_path}")
            
        cls._lang = lang
        with open(locale_path, 'r', encoding='utf-8') as file:
            cls._data = json.load(file)
            
        if cls._instance:
            cls._instance.log.info(f'Switched locale to: {locale_path}')

    def get(self, key: str, default: Optional[str] = None) -> str:
        """
        Get localized string by key
        
        Args:
            key: Localization key
            default: Default value if key not found
            
        Returns:
            Localized string or default value
        """
        try:
            return self._data[key]
        except KeyError:
            self.log.warning(f"Missing localization key: {key}")
            return default or key

    def format(self, key: str, **kwargs) -> str:
        """
        Get localized string and format it with provided arguments
        
        Args:
            key: Localization key
            **kwargs: Format arguments
            
        Returns:
            Formatted localized string
        """
        template = self.get(key)
        try:
            return template.format(**kwargs)
        except KeyError as e:
            self.log.error(f"Missing format argument {e} for key {key}")
            return template

    @property
    def current_language(self) -> str:
        """Get current language code"""
        return self._lang

    @property
    def supported_languages(self) -> list:
        """Get list of supported languages"""
        return self._supported_languages.copy()
