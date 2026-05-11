import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { DEFAULT_LANGUAGE } from "./config";
import { normalizeLocale, setActiveMessages } from "./index";

const LocaleContext = createContext();

const loadMessages = async (locale) => {
  switch (locale) {
    case "en":
      return (await import("../locales/en.json")).default;
    case "fr":
    default:
      return (await import("../locales/fr.json")).default;
  }
};

export function LocaleProvider({ children }) {
  const stored =
    typeof window !== "undefined"
      ? window.localStorage.getItem("quickt.locale")
      : null;
  const [locale, setLocaleState] = useState(normalizeLocale(stored));
  const [messages, setMessages] = useState(null);

  useEffect(() => {
    let cancelled = false;
    loadMessages(locale).then((msgs) => {
      if (!cancelled) {
        setMessages(msgs);
        setActiveMessages(msgs);
      }
    });
    return () => { cancelled = true; };
  }, [locale]);

  const changeLocale = useCallback((next) => {
    const normalized = normalizeLocale(next);
    setLocaleState(normalized);
    if (typeof window !== "undefined") {
      window.localStorage.setItem("quickt.locale", normalized);
    }
  }, []);

  if (!messages) {
    return null;
  }

  return (
    <LocaleContext.Provider value={{ locale, changeLocale }}>
      {children}
    </LocaleContext.Provider>
  );
}

export const useLocale = () => useContext(LocaleContext);
