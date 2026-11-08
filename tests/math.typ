#import "../src/tufted.typ"
#show: tufted.tufted-web.with(title: "Math regression")

Inline $x^2 + 1$.

$ a &= b + c \ &= d $ <native-first>

See @native-first and @native-last.

#math.equation(block: true, numbering: none)[$ e = f $]

#context [
  #set math.equation(numbering: "[i]")
  $ g = h $ <custom-number>
  See @custom-number.
]

#[
  #show math.equation: tufted.math-svg
  Inline SVG $alpha + beta$.
  $ x = y $ <svg-equation>
  See @svg-equation.
]

$ z = 0 $ <native-last>
