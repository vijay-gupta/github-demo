# Github
This repo is to give you an demonstration on git commands and how we can use it.
{
  "url": "https://example.com",
  "results": {
    "violations": [
      {
        "id": "color-contrast",
        "impact": "serious",
        "description": "Elements must have sufficient color contrast",
        "help": "Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds",
        "helpUrl": "https://dequeuniversity.com/rules/axe/4.11/color-contrast?application=axeAPI",
        "tags": ["wcag2aa", "wcag143"],
        "nodes": [
          {
            "target": ["#submitBtn"],
            "html": "<button id=\"submitBtn\" style=\"color:#777; background:#fff\">Submit</button>",
            "failureSummary": "Fix any of the following:\n  Element has insufficient color contrast of 2.3 (foreground color: #777777, background color: #ffffff, font size: 14.0pt, font weight: normal). Expected contrast ratio of 4.5:1"
          }
        ]
      }
    ],
    "passes": [
      {
        "id": "aria-allowed-attr",
        "impact": null,
        "description": "ARIA attributes are allowed for an element's role",
        "help": "Ensures ARIA attributes are allowed for an element's role",
        "helpUrl": "https://dequeuniversity.com/rules/axe/4.11/aria-allowed-attr?application=axeAPI",
        "tags": ["wcag2a", "wcag412"],
        "nodes": [
          {
            "target": ["#main"],
            "html": "<main id=\"main\" role=\"main\"></main>"
          }
        ]
      }
    ],
    "incomplete": [],
    "inapplicable": [],
    "timestamp": "2025-01-01T12:00:00.000Z",
    "testEngine": { "name": "axe-core", "version": "4.11.1" },
    "testEnvironment": { "userAgent": "Mozilla/5.0 ...", "windowWidth": 1280, "windowHeight": 720 }
  }
}
