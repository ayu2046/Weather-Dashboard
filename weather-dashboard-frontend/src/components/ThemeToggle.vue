<template>
  <div class="theme-toggle-container">
    <button
      @click="toggleTheme"
      class="theme-toggle"
      :class="{ 'theme-toggle--dark': isDarkMode }"
      :aria-label="`Switch to ${isDarkMode ? 'light' : 'dark'} theme`"
      type="button"
    >
      <div class="theme-toggle__track">
        <div class="theme-toggle__thumb">
          <Sun 
            v-show="!isDarkMode" 
            class="theme-toggle__icon theme-toggle__icon--sun" 
          />
          <Moon 
            v-show="isDarkMode" 
            class="theme-toggle__icon theme-toggle__icon--moon" 
          />
        </div>
      </div>
      <span class="theme-toggle__label">
        {{ isDarkMode ? 'Dark' : 'Light' }} Mode
      </span>
    </button>
  </div>
</template>

<script>
import { useTheme } from '../composables/useTheme'
import { Sun, Moon } from 'lucide-vue-next'

export default {
  name: 'ThemeToggle',
  components: {
    Sun,
    Moon
  },
  setup() {
    const { isDarkMode, toggleTheme } = useTheme()

    return {
      isDarkMode,
      toggleTheme
    }
  }
}
</script>

<style scoped>
.theme-toggle-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.theme-toggle {
  display: flex;
  align-items: center;
  gap: var(--spacing-3, 0.75rem);
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--spacing-2, 0.5rem);
  border-radius: var(--radius-lg, 0.5rem);
  transition: all var(--duration-200, 200ms) var(--timing-ease, ease);
  color: var(--color-text-primary, #0f172a);
  font-family: var(--font-primary, inherit);
  font-size: var(--text-sm, 0.875rem);
  font-weight: var(--font-weight-medium, 500);
}

.theme-toggle:hover {
  background-color: var(--color-surface-secondary, #f8fafc);
  transform: translateY(-1px);
}

.theme-toggle:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-border-focus, #3b82f6);
}

.theme-toggle:active {
  transform: translateY(0);
}

.theme-toggle__track {
  position: relative;
  width: 52px;
  height: 28px;
  background-color: var(--color-neutral-300, #d1d5db);
  border-radius: var(--radius-full, 9999px);
  transition: background-color var(--duration-300, 300ms) var(--timing-ease, ease);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.theme-toggle--dark .theme-toggle__track {
  background-color: var(--color-primary-500, #3b82f6);
}

.theme-toggle__thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 24px;
  height: 24px;
  background-color: var(--color-neutral-0, #ffffff);
  border-radius: var(--radius-full, 9999px);
  transition: all var(--duration-300, 300ms) var(--timing-spring, cubic-bezier(0.68, -0.55, 0.265, 1.55));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  will-change: transform;
}

.theme-toggle--dark .theme-toggle__thumb {
  transform: translateX(24px);
  background-color: var(--color-neutral-900, #111827);
}

.theme-toggle__icon {
  width: 14px;
  height: 14px;
  transition: all var(--duration-200, 200ms) var(--timing-ease, ease);
  opacity: 0;
  transform: scale(0.8);
  color: currentColor;
}

.theme-toggle__icon--sun {
  color: var(--color-warning-500, #f59e0b);
}

.theme-toggle__icon--moon {
  color: var(--color-primary-400, #60a5fa);
}

.theme-toggle:not(.theme-toggle--dark) .theme-toggle__icon--sun,
.theme-toggle--dark .theme-toggle__icon--moon {
  opacity: 1;
  transform: scale(1);
}

.theme-toggle__label {
  white-space: nowrap;
  transition: color var(--duration-200, 200ms) var(--timing-ease, ease);
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .theme-toggle__label {
    display: none;
  }
  
  .theme-toggle {
    padding: var(--spacing-2, 0.5rem);
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .theme-toggle__track {
    border: 2px solid var(--color-border-primary, #e2e8f0);
  }
  
  .theme-toggle__thumb {
    border: 2px solid var(--color-border-secondary, #cbd5e1);
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .theme-toggle,
  .theme-toggle__track,
  .theme-toggle__thumb,
  .theme-toggle__icon {
    transition: none;
  }
}

/* Focus visible support */
.theme-toggle:focus-visible {
  outline: 2px solid var(--color-border-focus, #3b82f6);
  outline-offset: 2px;
}

/* Animation for icon transitions */
@keyframes iconFadeIn {
  from {
    opacity: 0;
    transform: scale(0.8) rotate(-90deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

.theme-toggle__icon--sun,
.theme-toggle__icon--moon {
  animation: iconFadeIn var(--duration-300, 300ms) var(--timing-spring, cubic-bezier(0.68, -0.55, 0.265, 1.55)) forwards;
}
</style>
