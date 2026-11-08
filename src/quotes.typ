// Block quotes: the quoted words in a `<blockquote>`, and the attribution,
// which is not part of the quotation, in a `<figcaption>` beside it, the two
// wrapped in a `<figure>`, as the HTML standard recommends.
#let template-quotes(content) = {
  show quote.where(block: true): it => {
    if target() != "html" { return it }
    let body = html.blockquote(it.body)
    if it.attribution == none { return body }
    html.figure(class: "quote", {
      body
      html.figcaption([— ] + html.cite(it.attribution))
    })
  }
  content
}
