# Design Track Token References

## Master Design Tokens (JSON)
```json
{
  "color": {
    "brand": {
      "primary": "#1A7DB8",
      "secondary": "#E85D3A",
      "accent": "#F4A261"
    },
    "text": {
      "primary": "#222",
      "secondary": "#333333",
      "disabled": "#999999"
    },
    "background": {
      "light": "#F5F5F5",
      "dark": "#264653",
      "surface": "#FFFFFF"
    },
    "status": {
      "error": "#D62828",
      "warning": "#F4A261",
      "info": "#1A7DB8"
    },
    "cta-background": "#1A6FB0",
    "cta-text": "#FFFFFF"
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "18px",
    "lg": "24px",
    "xl": "32px",
    "xxl": "48px"
  },
  "typography": {
    "fontFamily": {
      "body": "'Comic Sans MS', serif",
      "heading": "'Plus Jakarta Sans', sans-serif",
      "mono": "'JetBrains Mono', monospace"
    },
    "fontSize": {
      "xs": "10px",
      "sm": "12px",
      "md": "14px",
      "lg": "18px",
      "xl": "24px",
      "xxl": "32px",
      "display": "48px"
    },
    "fontWeight": {
      "regular": "400",
      "medium": "500",
      "bold": "700"
    }
  },
  "shadow": {
    "sm": "0 1px 2px rgba(0,0,0,0.05)",
    "md": "0 4px 6px rgba(0,0,0,0.1)",
    "lg": "0 10px 15px rgba(0,0,0,0.1)"
  },
  "component": {
    "button": {
      "background": "{color.brand.primary}",
      "text": "#FFFFFF",
      "border-radius": "6px",
      "padding": "{spacing.sm} {spacing.lg}"
    },
    "card": {
      "background": "{color.background.surface}",
      "border": "1px solid {color.border.default}",
      "border-radius": "8px",
      "padding": "{spacing.md}"
    }
  }
}

## Compiled Component Tokens (CSS)
```css
/* Component-Level Design Tokens for DataSync Pro */
/* These tokens reference the global design-tokens.json values */

:root {
  /* Button Component */
  --button-primary-bg: var(--color-brand-primary);
  --button-primary-text: #FFFFFF;
  --button-primary-hover-bg: #155a8a;
  --button-primary-radius: 6px;
  --button-primary-padding: 8px 24px;

  /* Card Component */
  --card-bg: var(--color-background-surface);
  --card-border: 1px solid var(--color-semantic-warning);
  --card-radius: 8px;
  --card-padding: 16px;
  --card-shadow: 0 2px 4px rgba(0,0,0,0.1);

  /* Input Component */
  --input-border: 1px solid var(--color-border);
  --input-radius: 4px;
  --input-padding: 8px 12px;
  --input-focus-border: var(--color-brand-primary);

  /* Badge Component — MISSING entirely, no --badge-* tokens defined */

  /* Navigation Component — MISSING entirely, no --nav-* tokens defined */

  /* Legacy — these should be migrated to --button-* pattern */
  --btn-primary-bg: var(--color-cta-background);
  --btn-primary-text: var(--color-cta-text);
}
