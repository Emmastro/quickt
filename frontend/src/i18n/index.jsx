import {
  DEFAULT_LANGUAGE,
  SUPPORTED_LANGUAGE_CODES,
} from "./config";

let currentLocale =
  (typeof window !== "undefined" && window.localStorage.getItem("quickt.locale")) ||
  DEFAULT_LANGUAGE;

export const normalizeLocale = (locale) => {
  if (!locale) return DEFAULT_LANGUAGE;
  const normalized = String(locale).toLowerCase().replace("-", "_").split(",")[0].trim();
  if (SUPPORTED_LANGUAGE_CODES.has(normalized)) return normalized;
  const shortCode = normalized.split("_")[0];
  if (SUPPORTED_LANGUAGE_CODES.has(shortCode)) return shortCode;
  return DEFAULT_LANGUAGE;
};

export const getLocale = () => normalizeLocale(currentLocale);
export const getSupportedLanguages = () => import("./config").then(m => m.SUPPORTED_LANGUAGES);

export const setLocale = (locale) => {
  currentLocale = normalizeLocale(locale);
  if (typeof window !== "undefined") {
    window.localStorage.setItem("quickt.locale", currentLocale);
    window.dispatchEvent(new CustomEvent("quickt:locale-change", { detail: currentLocale }));
  }
  return currentLocale;
};

let _activeMessages = {};
export const setActiveMessages = (msgs) => { _activeMessages = msgs; };

const formatMessage = (message, values = {}) =>
  message.replace(/\{(\w+)\}/g, (_, token) =>
    Object.prototype.hasOwnProperty.call(values, token) ? String(values[token]) : `{${token}}`
  );

export const t = (key, options = {}) => {
  const message = Object.prototype.hasOwnProperty.call(_activeMessages, key) ? _activeMessages[key] : key;
  return formatMessage(message, options.values);
};
