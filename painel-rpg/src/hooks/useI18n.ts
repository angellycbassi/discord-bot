import { useCallback, useEffect, useState } from 'react';
import ptBR from '../i18n/pt.json';
import enUS from '../i18n/en.json';

type Translations = typeof ptBR;
type Language = 'pt-BR' | 'en-US';

const translations = {
  'pt-BR': ptBR,
  'en-US': enUS,
};

export const useI18n = () => {
  const [language, setLanguage] = useState<Language>('pt-BR');
  const [messages, setMessages] = useState<Translations>(translations[language]);

  useEffect(() => {
    const savedLang = localStorage.getItem('language') as Language;
    if (savedLang && translations[savedLang]) {
      setLanguage(savedLang);
      setMessages(translations[savedLang]);
    }
  }, []);

  const changeLanguage = useCallback((newLanguage: Language) => {
    setLanguage(newLanguage);
    setMessages(translations[newLanguage]);
    localStorage.setItem('language', newLanguage);
  }, []);

  const t = useCallback(
    (key: keyof Translations, params: Record<string, string> = {}) => {
      let message = messages[key] || key;
      Object.entries(params).forEach(([param, value]) => {
        message = message.replace(`{${param}}`, value);
      });
      return message;
    },
    [messages]
  );

  return {
    language,
    changeLanguage,
    t,
  };
};
