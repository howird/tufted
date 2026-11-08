# Tufted

A static website template built using Typst's experimental HTML export. Requires Typst 0.15.0 or newer and basic `make`.

![Tufted website](assets/devices.webp)

## Installation & Usage

Initialize the template from the Typst package registry:

```shell
typst init @preview/tufted:0.1.1
```

To build the website, run:

```shell
make html
```

Explore the `content/` folder for examples.

## Mathematics

Equations use native MathML by default, so they inherit the page's text color in
both light and dark mode. Numbered display equations have right-hand numbers
(default: `(1)`) and equation references link to their anchors. Custom numbering
patterns and `numbering: none` are supported.

For math that HTML export does not support, or when exact Typst layout is needed
(for example, custom `number-align`), opt into SVG rendering. After the template's
show rule, apply this rule to the whole page:

```typst
#show: template
#show math.equation: tufted.math-svg
```

Or limit the fallback to a single equation or group:

```typst
#[
  #show math.equation: tufted.math-svg
  $ integral_0^infinity e^(-x) dif x = 1 $ <integral>
]
See @integral.
```

The fallback supports inline and display math and preserves Typst's SVG equation
numbers. SVG math retains the legacy size and dark-mode inversion; native MathML
is not inverted. MathML appearance depends on the browser and available math fonts.

## Links

- [tufted.vsheg.com](https://tufted.vsheg.com) — live demo and docs of the latest stable version
- [dev.tufted.vsheg.com](https://dev.tufted.vsheg.com) — current dev version
- [Repository on GitHub](https://github.com/vsheg/tufted) — source code, issues, and contributions
- [Typst Universe](https://typst.app/universe/package/tufted) — template page
- [Tufte CSS](https://edwardtufte.github.io/tufte-css/) — used for styling, loaded automatically from a CDN

## License

The source code is available on [GitHub](https://github.com/vsheg/tufted) under the [MIT License](https://github.com/vsheg/tufted/blob/main/LICENSE). The template in the `template/` directory uses the more permissive [MIT-0](https://opensource.org/licenses/MIT-0) license.
