# Code Generation Guide

This document describes how subagents should generate code for each section.

## Subagent Responsibilities

Each subagent receives ONE section and must:
1. Analyze the HTML structure
2. Extract the design system (colors, typography, spacing)
3. Generate a self-contained React/Next.js component
4. Use Tailwind CSS for styling
5. Preserve original image URLs

## Input Data Format

Each subagent receives a chunk JSON:

```json
{
  "id": "section-3",
  "name": "section_3",
  "type": "section",
  "selector": "section.features",
  "rect": {
    "x": 0, "y": 680, "width": 1920, "height": 800
  },
  "styles": {
    "background_color": "rgb(249, 250, 251)",
    "padding": "96px 0px"
  },
  "html": "<section class=\"features\">...</section>",
  "images": [
    {"src": "https://example.com/feature1.svg", "alt": "Feature 1"},
    {"src": "https://example.com/feature2.svg", "alt": "Feature 2"}
  ],
  "links": [
    {"href": "/pricing", "text": "View Pricing"}
  ],
  "estimated_tokens": 2500
}
```

## Component Template

### React/Next.js (Default)

```tsx
// src/components/Section3.tsx

import Image from 'next/image'
import Link from 'next/link'

interface Section3Props {
  className?: string
}

export default function Section3({ className = '' }: Section3Props) {
  return (
    <section
      className={`py-24 bg-gray-50 ${className}`}
      style={{
        // Only use inline styles for values that can't be expressed in Tailwind
      }}
    >
      <div className="container mx-auto px-4">
        {/* Content here */}
      </div>
    </section>
  )
}
```

### Vue 3

```vue
<!-- src/components/Section3.vue -->

<template>
  <section class="py-24 bg-gray-50">
    <div class="container mx-auto px-4">
      <!-- Content here -->
    </div>
  </section>
</template>

<script setup lang="ts">
// Component logic if needed
</script>
```

## Styling Strategy

### Priority Order

1. **Tailwind Utility Classes** (preferred)
   ```tsx
   <div className="flex items-center gap-4 p-6 bg-white rounded-lg shadow-md">
   ```

2. **Tailwind Arbitrary Values** (when exact values matter)
   ```tsx
   <div className="w-[340px] h-[220px] bg-[#1a1a2e]">
   ```

3. **Inline Styles** (only for dynamic or complex values)
   ```tsx
   <div
     className="relative"
     style={{
       backgroundImage: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
     }}
   >
   ```

### Color Mapping

Convert RGB to Tailwind or hex:

| Original | Tailwind | Fallback |
|----------|----------|----------|
| `rgb(59, 130, 246)` | `bg-blue-500` | `bg-[#3b82f6]` |
| `rgb(255, 255, 255)` | `bg-white` | - |
| `rgb(0, 0, 0)` | `bg-black` | - |
| `rgb(249, 250, 251)` | `bg-gray-50` | `bg-[#f9fafb]` |

### Spacing Mapping

| Original | Tailwind |
|----------|----------|
| `16px` | `p-4` or `m-4` |
| `24px` | `p-6` or `m-6` |
| `32px` | `p-8` or `m-8` |
| `64px` | `p-16` or `m-16` |
| `96px` | `p-24` or `m-24` |

## Image Handling

### Keep Original URLs

**CRITICAL**: Use original image URLs directly. The user's localhost can access external images without CORS issues.

```tsx
// CORRECT - Use original URL
<img
  src="https://example.com/hero-image.jpg"
  alt="Hero"
  className="w-full h-auto"
/>

// For Next.js Image component, add domain to next.config.js
<Image
  src="https://example.com/hero-image.jpg"
  alt="Hero"
  width={800}
  height={600}
/>
```

### Image Optimization (Next.js)

If using Next.js Image component, remind user to configure domains:

```js
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',  // Allow all domains
      },
    ],
  },
}
```

## Layout Patterns

### Hero Section
```tsx
<section className="relative min-h-screen flex items-center justify-center">
  <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600" />
  <div className="relative z-10 text-center text-white max-w-4xl mx-auto px-4">
    <h1 className="text-5xl md:text-6xl font-bold mb-6">
      {/* Headline */}
    </h1>
    <p className="text-xl md:text-2xl mb-8 opacity-90">
      {/* Subheadline */}
    </p>
    <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold">
      Get Started
    </button>
  </div>
</section>
```

### Feature Grid
```tsx
<section className="py-24 bg-white">
  <div className="container mx-auto px-4">
    <h2 className="text-4xl font-bold text-center mb-16">Features</h2>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {features.map((feature, i) => (
        <div key={i} className="p-6 bg-gray-50 rounded-xl">
          <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <img src={feature.icon} alt="" className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
          <p className="text-gray-600">{feature.description}</p>
        </div>
      ))}
    </div>
  </div>
</section>
```

### Testimonial Section
```tsx
<section className="py-24 bg-gray-50">
  <div className="container mx-auto px-4">
    <div className="max-w-3xl mx-auto text-center">
      <blockquote className="text-2xl italic text-gray-700 mb-8">
        "Amazing product that transformed our workflow..."
      </blockquote>
      <div className="flex items-center justify-center gap-4">
        <img
          src="https://example.com/avatar.jpg"
          alt="John Doe"
          className="w-12 h-12 rounded-full"
        />
        <div className="text-left">
          <div className="font-semibold">John Doe</div>
          <div className="text-gray-500 text-sm">CEO, Company</div>
        </div>
      </div>
    </div>
  </div>
</section>
```

## Responsive Design

### Breakpoints

| Prefix | Min Width | Usage |
|--------|-----------|-------|
| (none) | 0px | Mobile first |
| `sm:` | 640px | Small tablets |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large screens |

### Common Patterns

```tsx
// Responsive text size
<h1 className="text-3xl md:text-4xl lg:text-5xl">

// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

// Responsive padding
<section className="py-12 md:py-16 lg:py-24">

// Hide on mobile
<div className="hidden md:block">

// Show only on mobile
<div className="block md:hidden">
```

## Animation & Transitions

### Hover Effects
```tsx
<button className="transition-all duration-300 hover:scale-105 hover:shadow-lg">
  Click Me
</button>
```

### Fade In (with Tailwind)
```tsx
<div className="animate-fade-in">
  {/* Content */}
</div>

// Add to tailwind.config.js:
// animation: { 'fade-in': 'fadeIn 0.5s ease-in-out' }
// keyframes: { fadeIn: { '0%': { opacity: 0 }, '100%': { opacity: 1 } } }
```

## Error Handling

### Missing Images
```tsx
<img
  src={imageSrc}
  alt={alt}
  onError={(e) => {
    e.currentTarget.src = '/placeholder.svg'
  }}
/>
```

### Fallback Content
```tsx
{content ? (
  <p>{content}</p>
) : (
  <p className="text-gray-400 italic">No content available</p>
)}
```

## Output Requirements

Each subagent MUST:

1. **Create ONE file**: `src/components/SectionN.tsx`
2. **Export default**: The component must be the default export
3. **Accept className prop**: For parent customization
4. **Be self-contained**: No external state dependencies
5. **Use TypeScript**: With proper interface definitions
6. **Include comments**: For complex logic only

## Quality Checklist

Before completing, verify:

- [ ] Component renders without errors
- [ ] All images use original URLs
- [ ] Responsive on mobile/tablet/desktop
- [ ] Hover states match original
- [ ] Colors match original design
- [ ] Typography (font sizes, weights) matches
- [ ] Spacing (padding, margins, gaps) matches
- [ ] No hardcoded widths that break responsiveness
