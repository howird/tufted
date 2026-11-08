// Opt into SVG rendering with `show math.equation: tufted.math-svg`.
#let math-svg(it) = {
  if target() != "html" {
    it
  } else if it.block {
    html.figure(class: "math-svg", role: "math", html.frame(it))
  } else {
    html.span(class: "math-svg", role: "math", html.frame(it))
  }
}

#let template-math(content) = {
  set math.equation(numbering: "(1)")

  show math.equation: it => {
    if target() == "html" and it.block and it.numbering != none {
      // Native MathML preserves the equation's anchor, but omits its number.
      html.div(class: "math-equation", {
        it
        html.div(class: "math-number", context numbering(
          it.numbering,
          ..counter(math.equation).at(it.location()),
        ))
      })
    } else {
      it
    }
  }

  content
}
