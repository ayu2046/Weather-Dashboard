import { ref, computed, watch } from 'vue'
import designSystem from '../theme/design-system.json'

// Global theme state
const isDarkMode = ref(false)

// Load theme from localStorage on initialization
const storedTheme = localStorage.getItem('weather-dashboard-theme')
if (storedTheme) {
  isDarkMode.value = storedTheme === 'dark'
} else {
  // Check system preference
  isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
}

export function useTheme() {
  // Computed theme name
  const currentTheme = computed(() => isDarkMode.value ? 'dark' : 'light')

  // Generate CSS variables from design tokens
  const generateCSSVariables = (theme) => {
    const colors = designSystem.colors[theme]
    const typography = designSystem.typography
    const spacing = designSystem.spacing
    const elevation = designSystem.elevation
    const borderRadius = designSystem.borderRadius
    const transitions = designSystem.transitions
    const gradients = designSystem.gradients[theme]

    const variables = {}

    // Color variables
    Object.entries(colors).forEach(([category, values]) => {
      if (typeof values === 'object' && !Array.isArray(values)) {
        Object.entries(values).forEach(([shade, color]) => {
          variables[`--color-${category}-${shade}`] = color
        })
      } else {
        variables[`--color-${category}`] = values
      }
    })

    // Typography variables
    Object.entries(typography.fontFamilies).forEach(([key, value]) => {
      variables[`--font-${key}`] = value
    })

    Object.entries(typography.fontSizes).forEach(([key, value]) => {
      variables[`--text-${key}`] = value
    })

    Object.entries(typography.fontWeights).forEach(([key, value]) => {
      variables[`--font-weight-${key}`] = value
    })

    Object.entries(typography.lineHeights).forEach(([key, value]) => {
      variables[`--line-height-${key}`] = value
    })

    Object.entries(typography.letterSpacings).forEach(([key, value]) => {
      variables[`--letter-spacing-${key}`] = value
    })

    // Spacing variables
    Object.entries(spacing).forEach(([key, value]) => {
      variables[`--spacing-${key}`] = value
    })

    // Elevation variables
    Object.entries(elevation.levels).forEach(([key, value]) => {
      variables[`--shadow-${key}`] = value[theme]
    })

    // Border radius variables
    Object.entries(borderRadius).forEach(([key, value]) => {
      variables[`--radius-${key}`] = value
    })

    // Transition variables
    Object.entries(transitions.duration).forEach(([key, value]) => {
      variables[`--duration-${key}`] = value
    })

    Object.entries(transitions.timing).forEach(([key, value]) => {
      variables[`--timing-${key}`] = value
    })

    // Gradient variables
    Object.entries(gradients).forEach(([category, values]) => {
      if (typeof values === 'object' && !Array.isArray(values)) {
        Object.entries(values).forEach(([key, gradient]) => {
          if (typeof gradient === 'object') {
            Object.entries(gradient).forEach(([subKey, subGradient]) => {
              variables[`--gradient-${category}-${key}-${subKey}`] = subGradient
            })
          } else {
            variables[`--gradient-${category}-${key}`] = gradient
          }
        })
      } else {
        variables[`--gradient-${category}`] = values
      }
    })

    return variables
  }

  // Apply CSS variables to the document root
  const applyCSSVariables = () => {
    const variables = generateCSSVariables(currentTheme.value)
    const root = document.documentElement
    
    Object.entries(variables).forEach(([property, value]) => {
      root.style.setProperty(property, value)
    })

    // Set theme attribute for conditional styling
    root.setAttribute('data-theme', currentTheme.value)
    
    // Update body class for legacy styling
    document.body.classList.toggle('dark', isDarkMode.value)
    document.body.classList.toggle('light', !isDarkMode.value)
  }

  // Toggle theme function
  const toggleTheme = () => {
    isDarkMode.value = !isDarkMode.value
  }

  // Set specific theme
  const setTheme = (theme) => {
    isDarkMode.value = theme === 'dark'
  }

  // Watch for theme changes and apply them
  watch(currentTheme, (newTheme) => {
    localStorage.setItem('weather-dashboard-theme', newTheme)
    applyCSSVariables()
  }, { immediate: true })

  // Listen for system theme changes
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  const handleSystemThemeChange = (e) => {
    if (!localStorage.getItem('weather-dashboard-theme')) {
      isDarkMode.value = e.matches
    }
  }

  mediaQuery.addEventListener('change', handleSystemThemeChange)

  return {
    isDarkMode,
    currentTheme,
    toggleTheme,
    setTheme,
    applyCSSVariables
  }
}
